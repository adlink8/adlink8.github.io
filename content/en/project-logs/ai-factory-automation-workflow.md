+++
title = 'Project Log: Bootstrapping the AI-Factory Local Automation Pipeline'
date = 2026-02-20T22:30:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['project-logs']
tags = ['Docker', 'n8n', 'DevOps', 'Automation', 'Pipelines']
projects = ['devops-roadmap']
description = 'Engineering build log for AI-Factory: setting up containerized n8n on Docker, wiring Python execution runtimes, and integrating LLM API endpoints.'
+++

Initiated `AI-Factory`, an event-driven automation platform built on local Docker infrastructure, designed to unify exploratory scripting and LLM API calls into a observable, self-healing pipeline.

<!--more-->

---

## 1. Project Overview & Current Status

- **Project Name**: `AI-Factory`
- **Scope**: A local-first, event-driven orchestration engine bridging strategic planning, midstream code execution, and downstream knowledge persistence.
- **Current Status**: 🟡 **Core Containers Online, Flow Validation In Progress**

---

## 2. Goals

1. Spin up an integrated n8n automation runtime via Docker Compose on Windows + WSL 2;
2. Resolve upstream Task Broker crashes caused by missing Python 3 interpreters;
3. Establish an end-to-end flow: Webhook $\to$ JSON sanitization $\to$ LLM generation $\to$ atomic disk persistence;
4. Enforce isolated checkpoint storage and human approval gates across pipeline stages.

---

## 3. Tech Stack

<p class="resume-stack">
  <code>Docker Compose</code> <code>WSL 2</code> <code>n8n</code> <code>Python 3.12</code> <code>FastAPI</code> <code>Git</code>
</p>

---

## 4. Progress Log

### Phase 1: Environment Orchestration (2026-02-20)
- [x] Configured `docker-compose.yml`, mounting local volumes for persistent n8n state (`./n8n_data:/home/node/.n8n`);
- [x] Diagnosed internal mode Task Broker crash (`Failed to start Python task runner in internal mode`);
- [x] Authored a custom Dockerfile layering `python3` and `py3-pip` onto Alpine, restoring Task Broker health;
- [x] Bound port 5678 and verified web console connectivity.

### Phase 2: Flow Wiring & Context Debugging (2026-02-22 to 02-23)
- [x] Built the initial data sanitization pipeline;
- [x] Clarified expression evaluation differences between Fixed and Expression modes;
- [x] Implemented pre-prompt Markdown text stripping to prevent token bloat during batch inferences.

---

## 5. Current Deliverables

- Reproducible Compose specs and container configurations in `D:\ADLINK\DockerWorkspace\AI-Factory`;
- Validated baseline pipelines executing HTTP-triggered Python scripts;
- Published a diagnostic runbook for containerized task runners (see [`/pitfalls/n8n-docker-python-task-runner-missing/`](/pitfalls/n8n-docker-python-task-runner-missing/)).

---

## 6. Next Steps

- [ ] Implement multi-model routing to balance lightweight and reasoning models based on prompt complexity;
- [ ] Wire up webhook alerting to mobile channels;
- [ ] Extract compute-intensive transformations into standalone microservices.
