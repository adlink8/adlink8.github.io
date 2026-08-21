+++
title = 'NovelMind — Chinese Long-Text RAG Platform'
description = 'Full telemetry and multi-agent collaborative engineering records for the NovelMind long-text RAG platform.'
date = 2026-08-17
layout = 'list'
+++

<p class="resume-stack"><code>Python</code> <code>FastAPI</code> <code>Next.js</code> <code>PostgreSQL</code> <code>ChromaDB</code> <code>Claude Worktrees</code> <code>OpenAI Codex</code> <code>Grok</code> <code>ZCode</code></p>

A hierarchical narrative memory and long-text RAG platform built for Chinese novels, featuring L0–L4 memory tiers, multi-source analytics pipelines, conversational search, and an Electron desktop app. Developed from 2026-06-06 to 2026-08-15 across 5 specialized AI agents.

<!--more-->

### 📊 Full Engineering Telemetry (SSOT Database)

| Key Metric | Quantified Value | Engineering Meaning |
| :--- | :--- | :--- |
| **Canonical Sessions** | **420 sessions** (workspace bound) | Architecture design, prototyping, refactoring, TDD, and multi-branch execution |
| **Canonical Events** | **630,323 events** (`ce_events`) | High-fidelity traces: reasoning chains, tool calls, tool results, usage metrics |
| **Turns & Volume** | **27,690 turns** / **16.07M chars** | User Prompts: 3,203 (avg 1,332 chars/turn); AI responses: 23,318 turns |
| **Human-AI Leverage Ratio** | **1 : 7.3** (Turn amplification) | Each architectural user input triggered 7.3 turns of autonomous agent execution |
| **Deep Reasoning Cycles** | **126,245 cycles** (Reasoning) | Mathematical and algorithmic deduction prior to code generation |
| **Terminal Automations** | **17,274 runs** (Exec / Bash) | Automated dependency installation, test suites, server control, and Git ops |
| **Precision Edits** | **3,738 edits** (Edit / Write) | Schema migrations, type refactorings, large-file modularization, and TDD |
| **Repository Versioning** | **621 Git commits** (`novel-mind-new`) | Autonomous delivery orchestrated across 8 Claude Code Worktree subagents |

### 🤖 Multi-Agent R&D Matrix

| Agent Client | Sessions | Share | Core Role & Engineering Deliverables |
| :--- | :--- | :--- | :--- |
| **Codex (OpenAI CLI)** | **205** | **48.8%** | Core architecture, backend APIs, Alembic migrations, TDD slices, and read-only audit |
| **Grok** | **87** | **20.7%** | Narrative hierarchy rebuild, planning review, and 13-task concurrent ideation |
| **ZCode** | **74** | **17.6%** | Local system integration, GSD executor batch runs, and automated debugging |
| **Workbuddy (Kimi)** | **33** | **7.9%** | Multi-source context ingestion and cross-module organization |
| **Claude (Worktrees)** | **21** | **5.0%** | `novel-mind-new` multi-worktree parallel refactor, contract tests, and boundary gates |
