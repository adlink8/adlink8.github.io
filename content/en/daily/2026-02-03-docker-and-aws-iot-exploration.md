+++
title = '2026-02-03 Dev Log: Containerizing Notes with Docker & AWS IoT Exploration'
date = 2026-02-03T23:50:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['daily']
tags = ['Docker', 'AWS', 'IoT', 'DevOps']
projects = ['devops-roadmap']
description = '2026-02-03 milestone: successfully deployed the first local containerized notes service on Docker and established a simulated edge-to-AWS telemetry loop.'
+++

Took the initial steps toward local-first containerization and IoT cloud integration: launched a notes container with Docker and verified simulated edge telemetry into AWS via Python.

<!--more-->

### What I Did Today

- [x] Deployed and persisted a local self-hosted note-taking container using Docker;
- [x] Configured SSH and virtual networking to a local Linux VM via FinalShell;
- [x] Authored a Python `requests` script to simulate edge hardware sensors, streaming telemetry into a local database;
- [x] Reviewed AWS SAA certification roadmaps to map engineering boundaries across IoT and cloud operations.

### Challenges & Insights

- **Ready-Made Images vs Configuration Mastery**: Pulling public images is straightforward, but mastering container networking, port binds, and volumes requires authoring Dockerfiles from scratch.
- **Moving Beyond Script Copying**: Resolved to verify every CLI flag against official documentation instead of passively copying generated commands.

### Tools & Resources Used

- `Docker Desktop`
- `FinalShell`
- `Ubuntu VM`
- `Python requests`

### Next Steps

- [ ] Align learning milestones with official DevOps roadmap standards;
- [ ] Migrate sensor simulation from simple HTTP POSTs to persistent MQTT pub/sub streams.
