+++
title = '项目日志：基于涂鸦 T5AI 开发板的 MQTT 双通道额度监视器固件构建'
date = 2026-06-06T15:30:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['project-logs']
tags = ['Tuya', 'T5AI', 'LVGL', 'MQTT', 'C', '嵌入式']
projects = ['t5ai-codex-quota']
description = '记录在涂鸦 T5AI-Board 上开发 LVGL 固件、打通 PC → MQTT → 开发板双通道通信与 HTTP 轮询兜底机制的工程里程碑。'
+++

推进项目 `t5ai-codex-quota` 的核心固件研发：将一块涂鸦 T5AI 开发板改造为桌面级 AI 额度与自动化流水线运行状态监视器。

<!--more-->

---

## 1. 项目概览与当前状态 (Project Overview & Status)

- **项目名称**：`t5ai-codex-quota`
- **项目定位**：运行在涂鸦 T5AI-Board 上的嵌入式硬件监视器，通过双通道（PC $\to$ MQTT $\to$ 开发板，带 HTTP 轮询兜底）实时呈现多智能体调用额度与服务健康度。
- **当前状态**：🟢 **双通道协议跑通，UI 交互联调中 (Milestone Reached)**

---

## 2. 核心目标 (Goals)

1. 在 WSL 2 环境下配置 TuyaOpen SDK 与可复现的交叉编译工具链；
2. 基于 LVGL 8.x 绘制高帧率、低内存占用的仪表盘界面（展示 Token 消耗、活跃 Agent 数与网络延迟）；
3. 实现 MQTT 主通道长连接，并引入 HTTP 轮询机制作为弱网断线时的自动兜底；
4. 杜绝固件死锁，在内存紧张的嵌入式芯片上实现双线程安全消费。

---

## 3. 技术栈 (Tech Stack)

<p class="resume-stack">
  <code>C</code> <code>TuyaOpen SDK</code> <code>LVGL 8.3</code> <code>FreeRTOS</code> <code>MQTT</code> <code>WSL 2</code>
</p>

---

## 4. 进度追踪 (Progress Log)

### 阶段一：交叉编译与环境跑通 (2026-05 下旬)
- [x] 在 WSL 2 中拉取官方 TuyaOpen SDK，排查编译头文件缺失问题；
- [x] 成功编译出目标镜像并通过串口烧录工具（flash_download_tool）刷入 T5AI 板卡；
- [x] 点亮板载 LCD 屏幕，运行 LVGL 基础 Demo 帧率稳定在 30+ FPS。

### 阶段二：MQTT 通信与协议解析 (2026-06-06)
- [x] 对接本地 EMQX / 公网 MQTT Broker，设计紧凑的 JSON 数据上报 Schema：
  ```json
  {
    "device_id": "t5ai_desk_01",
    "codex_quota": 84.5,
    "active_agents": 4,
    "status": "healthy"
  }
  ```
- [x] 解决网络重连时的状态丢失问题，引入 FreeRTOS 环形队列暂存遥测数据；
- [x] 编写 Python 模拟器持续向 MQTT 主题发布测试数据，验证板卡端解析与 UI 刷新延迟 < 150ms。

---

## 5. 当前阶段交付成果 (Current Deliverables)

- 可稳定复现编译的固件工程，存放在 `D:\ADLINK\Myproject\TuYa`；
- 跑通基于 MQTT QoS 1 的高可靠消息订阅；
- 仪表盘已能动态展示各项遥测数值，支持红/黄/绿健康状态指示灯。

---

## 6. 下一步计划 (Next Steps)

- [ ] 完成 HTTP 轮询兜底逻辑的无缝切换测试；
- [ ] 增加低功耗定时休眠模式，夜晚自动关闭屏幕背光；
- [ ] 设计并在 3D 打印外壳中装配电池与电源管理模块。
