+++
title = 'Project Log: Building the Tuya T5AI MQTT Telemetry & Quota Monitor'
date = 2026-06-06T15:30:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['project-logs']
tags = ['Tuya', 'T5AI', 'LVGL', 'MQTT', 'C', 'Embedded']
projects = ['t5ai-codex-quota']
description = 'Developing custom LVGL firmware on the Tuya T5AI development board with dual-channel PC -> MQTT -> Board telemetry and HTTP polling fallback.'
+++

Advancing firmware engineering on `t5ai-codex-quota`: transforming a Tuya T5AI development board into a hardware telemetry and quota monitor for local multi-agent systems.

<!--more-->

---

## 1. Project Overview & Current Status

- **Project Name**: `t5ai-codex-quota`
- **Scope**: Embedded desktop telemetry monitor running custom LVGL firmware on Tuya T5AI, receiving metrics via dual channels (PC $\to$ MQTT $\to$ Board, with HTTP polling fallback).
- **Current Status**: 🟢 **Dual-Channel Messaging Operational, UI Calibration In Progress**

---

## 2. Goals

1. Establish a reproducible cross-compilation pipeline using TuyaOpen SDK under WSL 2;
2. Render high-framerate, low-footprint dashboards in LVGL 8.x displaying token consumption, active agents, and latency;
3. Implement a persistent MQTT subscriber with automatic fallback to HTTP polling during broker disconnections;
4. Guarantee lock-free execution across FreeRTOS tasks under strict RAM constraints.

---

## 3. Tech Stack

<p class="resume-stack">
  <code>C</code> <code>TuyaOpen SDK</code> <code>LVGL 8.3</code> <code>FreeRTOS</code> <code>MQTT</code> <code>WSL 2</code>
</p>

---

## 4. Progress Log

### Phase 1: Toolchain Setup & Display Bring-Up (Late May 2026)
- [x] Cloned official TuyaOpen SDK in WSL 2, resolving missing header paths;
- [x] Compiled valid binary artifacts and flashed target boards via `flash_download_tool`;
- [x] Initialized the onboard LCD, achieving stable 30+ FPS on baseline LVGL widgets.

### Phase 2: MQTT Integration & Telemetry Deserialization (2026-06-06)
- [x] Integrated with local EMQX and public brokers, defining a compact JSON telemetry schema:
  ```json
  {
    "device_id": "t5ai_desk_01",
    "codex_quota": 84.5,
    "active_agents": 4,
    "status": "healthy"
  }
  ```
- [x] Mitigated message loss during reconnects by staging payloads in a FreeRTOS ring buffer;
- [x] Authored a Python hardware mock harness to publish load metrics, verifying end-to-end rendering latency < 150ms.

---

## 5. Current Deliverables

- Reproducible C firmware source in `D:\ADLINK\Myproject\TuYa`;
- Reliable QoS 1 message ingestion over Wi-Fi;
- Fully interactive LVGL dashboard with color-coded operational health indicators.

---

## 6. Next Steps

- [ ] Execute automated failure-injection tests for HTTP polling fallback;
- [ ] Implement ambient low-power sleep modes to extinguish backlights overnight;
- [ ] Enclose hardware in a custom 3D-printed enclosure with LiPo battery management.
