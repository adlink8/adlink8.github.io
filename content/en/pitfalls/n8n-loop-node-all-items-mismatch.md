+++
title = 'n8n Workflow Pitfall: Resolving All Items vs Each Item Mismatches in Loop Nodes'
date = 2026-03-01T15:20:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['pitfalls']
tags = ['n8n', 'Workflow', 'Data-Flow', 'Troubleshooting', 'DevOps']
projects = ['devops-roadmap']
description = 'Debugging data context mismatches in n8n workflows where downstream batch nodes reject item streams from upstream loops.'
+++

When designing complex multi-step automated workflows, connecting loop iteration logic directly into downstream batch storage or export nodes often triggers execution context mismatch errors. This post explains n8n batch semantics and how to structure loop aggregations correctly.

<!--more-->

---

## 1. Problem Description

In an AI-driven text summarization workflow in n8n, an upstream node fetched an array of technical documents. A `Loop Over Items` node iterated over each item, calling an LLM endpoint for processing. The final step was intended to batch-insert all synthesized summaries into a PostgreSQL database.

However, the final node failed with the error: **"This operation can only be executed on All Items, but the previous node passed an Each Item stream"**, halting the pipeline and dropping earlier items.

## 2. Environment

- **Orchestration Tool**: n8n (Self-Hosted on Docker)
- **Workflow Topology**: `HTTP Request` $\to$ `Loop Over Items` $\to$ `Code Node` $\to$ `Storage Node`
- **Data Payload**: JSON array containing 10+ documents

## 3. Error Message (Raw Output)

```text
NodeExecutionError: Invalid input data format
This operation can only be executed on 'All Items', but the previous node passed an 'Each Item' stream.
Current context: iteration loop_index=9, remaining=0. Upstream node closed without aggregating batch outputs.
```

## 4. Root Cause

1. **n8n's Dual Execution State Model**:
   - **All Items**: The pipeline processes data as a unified array in a single execution turn (required by batch INSERT nodes).
   - **Each Item**: The stream splits into discrete elements, each carrying its own `$itemIndex` iteration context.
2. **Incorrect Loop Circuit Topology**:
   - A `Loop Over Items` node provides two output ports: `loop` (for inner iterations) and `done` (fired when all iterations conclude).
   - Wiring the last step of the inner loop directly to a downstream batch node triggers that downstream node on every iteration with only a single item, violating batch constraints.
3. **Missing Re-Aggregation**:
   - Items exiting a loop stream must be explicitly re-aggregated into an array before batch consumption.

---

## 5. Solution

### Step 1: Properly Close the Loop Circuit

Ensure the iteration body routes back to the loop node's input, and only proceed downstream via the `done` port:

```
[Fetch Data] ──► [Loop Over Items] ──(loop)──► [LLM Node] ──► [Format Code] ──┐
                        │                                                     │
                        │ ◄───────────────────────────────────────────────────┘
                        │
                     (done)
                        ▼
            [Aggregate / Item Lists] ──► [Batch Database Storage]
```

### Step 2: Introduce an `Aggregate` Node on `done`

Place an `Item Lists -> Aggregate Items` node immediately following the `done` branch:
- **Aggregate Option**: Select `All items into a single list`
- **Fields to Include**: Specify keys to preserve (`title`, `summary`, `timestamp`)

This guarantees that downstream database nodes receive a clean, single-turn array.

---

## 6. Prevention

- **Verify Port Contexts**: Before wiring nodes, confirm whether the output is an item stream (`Each Item`) or an array (`All Items`).
- **Test with Mock Subsets**: When debugging complex loops, configure `Limit: 2` on upstream queries to verify batch boundaries before opening up full workloads.

---

## 7. References

- [n8n Docs: Looping in Workflows](https://docs.n8n.io/workflows/loops/)
- [n8n Docs: Data Aggregation & Item Lists](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.itemlists/)
