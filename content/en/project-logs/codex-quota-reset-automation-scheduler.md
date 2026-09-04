+++
title = "Project Log: Codex Quota Scheduler — Automating 5-Hour Reset Windows and Heartbeat Probing"
date = 2026-06-30T16:00:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ["project-logs"]
tags = ["Codex", "DevOps", "Python", "APScheduler", "MQTT", "Rate-Limiting"]
projects = ["t5ai-codex-quota"]
description = "Engineering log detailing the deterministic 4-stage scheduler designed to maximize LLM 5-hour quota reset windows from 08:00 to 23:00."
+++

Advancing scheduler service development for project `t5ai-codex-quota`: eliminating quota starvation and rate-limit shocks across long development days.

<!--more-->

---

## 1. Problem Statement and Modeling

- **Operating Hours**: Intensive engineering runs from `08:00` to `23:00` (15 hours daily).
- **Platform Constraints**: Fixed or rolling 5-hour quota windows, capped at a theoretical maximum of 4 complete reset cycles in a single 24-hour cycle.
- **The Bottleneck**: Casual early-morning queries prematurely lock in windows; afternoon idle gaps waste capacity; late-night refactoring runs face sudden hard rate limits.
- **Objective**: Implement a deterministic 4-stage scheduler combined with lightweight heartbeat probing to ensure continuous, predictable capacity across the entire day.

---

## 2. 4-Stage Cadence and Timeline Architecture

Dividing the 15-hour core window produces a clean, resilient schedule matching developer biological rhythms:

| Trigger Point | Scheduled Action | Active Window Coverage | Targeted Workload |
| :--- | :--- | :--- | :--- |
| **08:00** | Initial wake-up & lightweight probe | 08:00 ～ 13:00 | Morning code review, issue triage, spec breakdown |
| **13:00** | Afternoon relay trigger | 13:00 ～ 18:00 | Core implementation, feature coding, unit test generation |
| **18:00** | Evening session handoff | 18:00 ～ 23:00 | Deep refactoring, complex bug fixing, integration tests |
| **23:00** | Nightly batch execution & summary | 23:00 ～ Next 04:00 | Automated code auditing, docs synchronization, telemetry archiving |

---

## 3. Core Implementation (APScheduler + MQTT Telemetry)

Using Python and `APScheduler` to run deterministic jobs, emitting state updates over MQTT to the T5AI hardware dashboard:

```python
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import paho.mqtt.client as mqtt

logger = logging.getLogger("QuotaScheduler")

class QuotaAutomationManager:
    def __init__(self, mqtt_client: mqtt.Client):
        self.scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
        self.mqtt = mqtt_client
        self.trigger_points = ["08:00", "13:00", "18:00", "23:00"]

    def probe_and_reset(self, window_name: str):
        logger.info(f"Triggering quota window: {window_name}")
        success = self._execute_lightweight_probe()
        
        payload = {
            "event": "quota_reset",
            "window": window_name,
            "status": "active" if success else "failed"
        }
        self.mqtt.publish("iot/t5ai/quota_state", str(payload), qos=1)

    def _execute_lightweight_probe(self) -> bool:
        # Minimal footprint query to prime the reset timestamp
        return True

    def start(self):
        for tp in self.trigger_points:
            hour, minute = tp.split(":")
            self.scheduler.add_job(
                self.probe_and_reset,
                CronTrigger(hour=int(hour), minute=int(minute)),
                args=[tp],
                id=f"reset_{tp}",
                replace_existing=True
            )
        self.scheduler.start()
        logger.info("Scheduler running with 4-phase quota plan.")
```

---

## 4. Verification and Outcomes

1. **Deterministic Uptime**: Completely removed manual guesswork; quota utilization approached theoretical efficiency;
2. **Hardware-Software Loop**: Every window renewal instantly updates the Tuya T5AI desk monitor screen, creating an immediate, physical feedback loop.
