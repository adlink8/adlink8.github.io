+++
title = 'NovelMind — 中文长文本 RAG 平台'
description = '多 Agent 深度协同研发中文长文本 RAG 平台的完整量化档案。'
date = 2026-08-17
layout = 'list'
+++

<p class="resume-stack"><code>Python</code> <code>FastAPI</code> <code>Next.js</code> <code>PostgreSQL</code> <code>ChromaDB</code> <code>Claude Worktrees</code> <code>OpenAI Codex</code> <code>Grok</code> <code>ZCode</code></p>

面向中文长文本（小说）的分层 RAG 平台，包含分层叙事记忆系统（L0–L4）、多源分析管线、对话式检索和 Electron 客户端。从 2026-06-06 至 2026-08-15（历时 2 个多月），深度调动 5 类 AI Agent 进行协同研发与全量重构。

<!--more-->

### 📊 全周期研发量化底座 (SSOT Telemetry)

| 核心指标 | 量化数值 | 研发含义 |
| :--- | :--- | :--- |
| **标准协同会话** | **420 场** (按工作区精准归属) | 覆盖架构设计、原型验证、模块拆分、测试驱动与多分支重构 |
| **细粒度保真事件** | **630,323 个事件** (`ce_events`) | 包含模型推理链、工具调用、结果反馈、Token 计量等全量轨迹 |
| **交互轮次与字符量** | **27,690 轮** / **1,607.7 万字符** | 用户 Prompt 3,203 轮（均长 1,332 字），AI 生成 23,318 轮 |
| **人机交互杠杆比** | **1 : 7.3** (轮次放大倍数) | 用户每次系统级架构输入，驱动 AI 平均执行 7.3 轮复杂操作 |
| **模型深度推理** | **126,245 次** (Reasoning) | 在生成代码与执行操作前进行算法推导与边界判断 |
| **自动化终端执行** | **17,274 次** (Exec / Bash) | 自动化依赖安装、测试运行、服务启停与 Git 提交 |
| **代码精准重构** | **3,738 次** (Edit / Write) | 接口收口、类型重构、巨型文件拆分与 TDD 落地 |
| **代码库版本迭代** | **621 次 Git 提交** (`novel-mind-new`) | 采用 Claude Code Worktrees 8 组子代理多分支并行交付 |

### 🤖 多 Agent 协同研发矩阵

| Agent 客户端 | 承接会话数 | 占比 | 核心分工与产出 |
| :--- | :--- | :--- | :--- |
| **Codex (OpenAI CLI)** | **205 场** | **48.8%** | 核心架构、后端 API、Alembic 迁移、TDD 垂直切片与全面只读审计 |
| **Grok** | **87 场** | **20.7%** | 故事层级重构、规划审查与 13 任务并行创意推演 |
| **ZCode** | **74 场** | **17.6%** | 本地集成、GSD Executor 大规模批处理与自动化调试 |
| **Workbuddy (Kimi)** | **33 场** | **7.9%** | 多源数据接入与跨模块上下文组织 |
| **Claude (Worktrees)** | **21 场** | **5.0%** | `novel-mind-new` 多 Worktree 子代理并行重构、契约测试与边界定义 |