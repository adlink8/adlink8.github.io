+++
title = 'Projects'
description = 'Things I have designed and built — from IoT firmware to long-text RAG platforms.'
+++

A selection of systems I designed and shipped. Architecture decisions, tech selection and acceptance criteria are mine; AI accelerates implementation, it doesn't replace judgment.

<div class="project-card">
<div class="project-head">
<h3>novel-mind — Long-text RAG Platform</h3>
<a class="project-link" href="https://github.com/adlink8">GitHub →</a>
</div>
<p class="project-stack"><code>Python</code> <code>FastAPI</code> <code>Next.js</code> <code>PostgreSQL</code> <code>ChromaDB</code> <code>Ollama</code></p>
<ul>
<li>Full RAG pipeline for long Chinese text: chunking → embedding → vector store → local LLM generation</li>
<li>Evaluation-driven iteration: fixed test set + Recall@K / MRR / faithfulness metrics — every retrieval change is measured, not guessed</li>
<li>Stage-managed development (GSD) with pytest regression suites</li>
</ul>
</div>

<div class="project-card">
<div class="project-head">
<h3>t5ai-codex-quota — IoT Device Monitor</h3>
<a class="project-link" href="https://github.com/adlink8">GitHub →</a>
</div>
<p class="project-stack"><code>C</code> <code>TuyaOpen SDK</code> <code>LVGL</code> <code>MQTT</code> <code>Mosquitto</code> <code>HTTP</code></p>
<ul>
<li>LVGL firmware app on Tuya T5AI-Board (480×320 LCD) displaying live data from PC</li>
<li>Dual-channel architecture: PC bridge server → MQTT broker → board as primary, HTTP polling as fallback</li>
<li>Reproducible WSL firmware build, flashing and regression tests; fixed CJK glyph rendering and serial flashing issues</li>
</ul>
</div>

<div class="project-card">
<div class="project-head">
<h3>Personal Data Infrastructure</h3>
<a class="project-link" href="https://github.com/adlink8">GitHub →</a>
</div>
<p class="project-stack"><code>Python</code> <code>SQLite</code> <code>Chroma</code> <code>MCP</code> <code>REST</code> <code>CLI</code></p>
<ul>
<li>Multi-source data pipeline: 11k+ events, 44k+ entities, 40k+ knowledge units in SQLite + vector store</li>
<li>Served over CLI / REST / MCP interfaces, running 7×24 as the evidence layer for my other systems</li>
<li>Versioned index snapshots: build → validate → activate → rollback</li>
</ul>
</div>

## Current DevOps Roadmap

| Milestone | Focus | Stack |
|-----------|-------|-------|
| 1 | Linux internals & system calls — core metrics collector | Linux, Python |
| 2 | Containerization — package the app | Docker |
| 3 | Multi-cloud deployment | Terraform, AWS, DigitalOcean |
| 4 | Observability | Prometheus, Grafana |

Build progress is logged in [Project Logs](/project-logs/).
