+++
title = '简历'
layout = 'resume'
description = 'Li Shuo Yan — DevOps 工程师简历'
+++

<div class="resume-head">
<h1>Li Shuo Yan</h1>
<p class="resume-role">DevOps 工程师 — CI/CD、容器化与云基础设施</p>
<p class="resume-contact">
<a href="https://github.com/adlink8">github.com/adlink8</a> ·
<a href="mailto:2448366060l@email.com">2448366060l@email.com</a> ·
<a href="https://shuoyan.me">shuoyan.me</a>
</p>
</div>

## 个人概述

交付能跑起来的系统，而不是教程复现的 DevOps 工程师：**3 个已交付项目**，个人数据流水线日均接入 **11k+ 事件**、在管 **40k+ 知识单元**，7×24 运行。以阶段化方式与 AI 协作——规划 → 执行 → 验证 → 审计——验收标准由我制定，回归测试不通过不叫完成。

## 项目经历

### novel-mind — 长文本 RAG 平台
<p class="resume-stack"><code>Python</code> <code>FastAPI</code> <code>Next.js</code> <code>PostgreSQL</code> <code>ChromaDB</code> <code>Ollama</code></p>

- 构建面向中文长文本的完整 RAG 流水线：分块 → 向量化 → 向量存储 → 本地大模型生成
- 评估驱动迭代：固定测试集 + Recall@K / MRR / 忠实度指标，每一次检索改动都有数据支撑
- 阶段化管理开发（GSD），每个阶段以 pytest 回归套件作为验收门禁

### t5ai-codex-quota — IoT 设备监视器
<p class="resume-stack"><code>C</code> <code>TuyaOpen SDK</code> <code>LVGL</code> <code>MQTT</code> <code>Mosquitto</code> <code>HTTP</code></p>

- 交付运行在涂鸦 T5AI-Board（480×320 LCD）上的 LVGL 固件应用，实时展示 PC 端数据
- 设计双通道架构：PC 桥接服务 → MQTT broker → 开发板为主链路，HTTP 轮询自动兜底
- 实现 WSL 下可复现的固件构建、烧录与回归测试；修复中文字形渲染与串口烧录故障

### 个人数据基础设施
<p class="resume-stack"><code>Python</code> <code>SQLite</code> <code>Chroma</code> <code>MCP</code> <code>REST</code> <code>CLI</code></p>

- 运营多源数据流水线：SQLite + 向量库中管理 **11k+ 事件、44k+ 实体、40k+ 知识单元**
- 通过 CLI / REST / MCP 三种接口 7×24 对外服务，作为其他系统的证据层
- 版本化索引快照：构建 → 校验 → 激活 → 可回滚

## 技能

- **系统**：Linux 内核、系统调用、进程指标、WSL 工具链
- **语言**：Python、C、Bash、JavaScript/TypeScript
- **交付**：Docker、GitHub Actions CI/CD、Terraform（学习中）、AWS 与 DigitalOcean（路线图）
- **可观测性**：Prometheus / Grafana（路线图里程碑 4）
- **方法论**：评估驱动开发、阶段化 AI 协作（GSD）、测试门禁交付

## 语言

- 中文 — 母语
- 英语 — 读写流利，口语可交流

## 工作经历

<!-- TODO: 填写你的工作经历，格式如下
### 公司名称 — 职位 <span class="resume-meta">起止时间</span>
- 一句话量化成果
-->

## 教育经历

<!-- TODO: 填写你的教育经历，格式如下
### 学校名称 — 专业 <span class="resume-meta">起止时间</span>
-->
