+++
title = 'Resume'
layout = 'resume'
description = 'Li Shuo Yan — DevOps & AI Engineer resume'
+++

<div class="resume-head">
<h1>Li Shuo Yan</h1>
<p class="resume-role">DevOps &amp; AI Engineer — CI/CD, Cloud Infrastructure &amp; RAG/LLM Systems</p>
<p class="resume-intent">Seeking: AI Application / RAG Engineering Internship · Tech Support | Suzhou / Wuxi / Shenzhen | Class of 2027</p>
<p class="resume-contact">
<a href="https://github.com/adlink8">github.com/adlink8</a> ·
<a href="mailto:2448366060l@gmail.com">2448366060l@gmail.com</a>
</p>
</div>

## Summary

DevOps &amp; AI engineer who ships working systems, not tutorial replicas: **3 delivered projects**, a personal data pipeline ingesting **11k+ events** and managing **40k+ knowledge units**, running 7×24. I also ship AI applications: a long-text RAG platform for Chinese, where every retrieval iteration is driven by Recall@K / MRR / faithfulness metrics. I work stage-managed with AI — plan → execute → verify → audit — with acceptance criteria I own and regression tests that must pass before anything is called done.

## Projects

### novel-mind — Long-text RAG Platform
<p class="resume-stack"><code>Python</code> <code>FastAPI</code> <code>Next.js</code> <code>PostgreSQL</code> <code>ChromaDB</code> <code>Ollama</code></p>

- Built the full RAG pipeline for long Chinese text: chunking → embedding → vector store → local LLM generation
- Ran evaluation-driven iteration with a fixed test set — Recall@K / MRR / faithfulness metrics behind every retrieval change, no guessing
- Managed development in staged phases (GSD) with pytest regression suites as phase gates

### t5ai-codex-quota — IoT Device Monitor
<p class="resume-stack"><code>C</code> <code>TuyaOpen SDK</code> <code>LVGL</code> <code>MQTT</code> <code>Mosquitto</code> <code>HTTP</code></p>

- Shipped an LVGL firmware app on Tuya T5AI-Board (480×320 LCD) displaying live data from PC
- Designed dual-channel delivery: PC bridge → MQTT broker → board as primary path, HTTP polling as automatic fallback
- Made firmware builds reproducible on WSL with flashing and regression tests; fixed CJK glyph rendering and serial flashing failures

### Personal Data Infrastructure
<p class="resume-stack"><code>Python</code> <code>SQLite</code> <code>Chroma</code> <code>MCP</code> <code>REST</code> <code>CLI</code></p>

- Operate a multi-source data pipeline holding **11k+ events, 44k+ entities, 40k+ knowledge units** in SQLite + vector store
- Serve it over CLI / REST / MCP interfaces, 7×24, as the evidence layer for my other systems
- Versioned index snapshots: build → validate → activate → rollback

## Skills

- **Systems**: Linux internals, system calls, process metrics, WSL toolchains
- **Languages**: Python, C, Bash, JavaScript/TypeScript
- **AI Engineering**: RAG pipelines (chunking/embedding/retrieval/generation), ChromaDB vector stores, local inference with Ollama, LLM evaluation (Recall@K / MRR / faithfulness), MCP integration
- **Delivery**: Docker, GitHub Actions CI/CD, Terraform (learning), AWS & DigitalOcean (roadmap)
- **Observability**: Prometheus / Grafana (roadmap milestone 4)
- **Practices**: evaluation-driven development, staged AI-assisted engineering (GSD), test-gated delivery

## Languages

- Mandarin — Native
- English — Fluent reading & writing; conversational speaking

## Competition & Early Practice

### Jiangsu Province IoT Skills Competition — Networking Track <span class="resume-meta">2024 · Award-winning entry</span>

- Designed and deployed the LAN topology; configured the gateway and pulled data from the cloud platform API
- Isolated a VLAN connectivity fault via packet captures (trunk-port misconfiguration); 100% system integration pass rate

### AWS IoT Data Pipeline (ESP32 → MQTT → AWS)

- Dockerized an MQTT gateway on Ubuntu; device telemetry routed by AWS IoT Core rules to S3
- Root-caused frequent device dropouts from MQTT logs (keepalive misconfiguration), lifting uptime from 85% to 99%

## Education

### Changzhou University — Computer Science &amp; Technology, B.Eng. <span class="resume-meta">Graduating June 2027</span>

- Track: systems &amp; networking → cloud native → AI application engineering; roadmap and progress on the [projects page](/projects/)
