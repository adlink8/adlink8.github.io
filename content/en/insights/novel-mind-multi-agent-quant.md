+++
title = '630K Events Deep Dive: Quantifying Multi-Agent Collaborative Engineering in novel-mind'
date = 2026-08-17T10:00:00Z
draft = false
ShowToc = true
TocOpen = true
categories = ['insights']
tags = ['Multi-Agent', 'Architecture', 'Telemetry', 'GSD', 'Quantitative Engineering']
projects = ['novel-mind']
description = 'From 420 sessions, 630K canonical events, and 17K automated executions: a deep telemetry breakdown of multi-agent collaborative engineering.'
+++

When personal software engineering fully embraces AI, the development paradigm shifts from "human writing code with AI completion" to "human driving architecture and invariant contracts, while specialized multi-agent teams autonomously orchestrate and execute closed-loop delivery."

<!--more-->

## 1. Why Full-Stack Telemetry Matters

During the two-month build of `novel-mind` (a long-text narrative RAG platform for Chinese novels), the project moved far beyond one-off prompt experiments. We established an end-to-end **Dialogue and Event Telemetry SSOT** (`agent_conversations.sqlite`).

Analyzing 420 canonical sessions and 630,323 high-fidelity execution events allows us to quantify human-AI leverage and identify the true velocity multipliers in modern engineering.

---

## 2. Telemetry Highlights (The 1 : 7.3 Leverage Ratio)

- **Input Density**: User prompts averaged **1,332 characters per turn**, focusing strictly on architectural constraints, boundary conditions, and acceptance criteria rather than trivial conversational chatter.
- **Amplification Factor**: Each structured prompt triggered an average of **7.3 dialogue turns** and over **18 discrete automated tool actions** (reading, reasoning, editing, terminal testing, and Git commits).

---

## 3. The Heterogeneous Multi-Agent Matrix

| Agent Client | Share | Specialization |
| :--- | :--- | :--- |
| **OpenAI Codex** | **48.8%** (205 sessions) | Core backend APIs, Alembic migrations, TDD slices, and strict read-only audits |
| **Grok** | **20.7%** (87 sessions) | Narrative hierarchy algorithms (L0–L4) and 13-task parallel ideation |
| **ZCode** | **17.6%** (74 sessions) | Local system integration and high-throughput GSD batch execution |
| **Claude (Worktrees)** | **5.0%** (21 sessions) | Multi-branch parallel refactoring across 8 isolated worktrees |
| **Workbuddy (Kimi)** | **7.9%** (33 sessions) | Cross-source context ingestion and documentation aggregation |

---

## 4. Engineering Velocity: Terminal Autonomy Over Plain Code Completion

The event logs reveal **17,274 automated terminal executions** compared to **3,738 direct code edits**. This confirms that the primary value driver of agentic development is **autonomous verification feedback loops**: writing code, executing automated test suites, interpreting stack traces, self-correcting, and committing directly to Git.
