+++
title = '项目'
description = '我设计并交付的系统 —— 从 IoT 固件到长文本 RAG 平台。'
+++

这里是我设计并交付的部分系统。架构决策、技术选型与验收标准都由我主导；AI 加速实现，但不替代判断。

<div class="project-card">
<div class="project-head">
<h3>novel-mind — 长文本 RAG 平台</h3>
<a class="project-link" href="https://github.com/adlink8">GitHub →</a>
</div>
<p class="project-stack"><code>Python</code> <code>FastAPI</code> <code>Next.js</code> <code>PostgreSQL</code> <code>ChromaDB</code> <code>Ollama</code></p>
<ul>
<li>面向中文长文本的完整 RAG 流水线：分块 → 向量化 → 向量存储 → 本地大模型生成</li>
<li>评估驱动迭代：固定测试集 + Recall@K / MRR / 忠实度指标 —— 每一次检索改动都有数据支撑，而不是凭感觉</li>
<li>阶段化管理开发（GSD），配套 pytest 回归测试</li>
</ul>
</div>

<div class="project-card">
<div class="project-head">
<h3>t5ai-codex-quota — IoT 设备监视器</h3>
<a class="project-link" href="https://github.com/adlink8">GitHub →</a>
</div>
<p class="project-stack"><code>C</code> <code>TuyaOpen SDK</code> <code>LVGL</code> <code>MQTT</code> <code>Mosquitto</code> <code>HTTP</code></p>
<ul>
<li>运行在涂鸦 T5AI-Board（480×320 LCD）上的 LVGL 固件应用，实时展示 PC 端数据</li>
<li>双通道架构：PC 桥接服务 → MQTT broker → 开发板为主链路，HTTP 轮询兜底</li>
<li>可复现的 WSL 固件构建、烧录与回归测试；修复了中文字形渲染与串口烧录问题</li>
</ul>
</div>

<div class="project-card">
<div class="project-head">
<h3>个人数据基础设施</h3>
<a class="project-link" href="https://github.com/adlink8">GitHub →</a>
</div>
<p class="project-stack"><code>Python</code> <code>SQLite</code> <code>Chroma</code> <code>MCP</code> <code>REST</code> <code>CLI</code></p>
<ul>
<li>多源数据流水线：SQLite + 向量库中管理 11k+ 事件、44k+ 实体、40k+ 知识单元</li>
<li>通过 CLI / REST / MCP 三种接口对外服务，7×24 运行，作为其他系统的证据层</li>
<li>版本化索引快照：构建 → 校验 → 激活 → 可回滚</li>
</ul>
</div>

## 当前 DevOps 路线图

| 里程碑 | 重点 | 技术栈 |
|-----------|-------|-------|
| 1 | Linux 内核与系统调用 —— 核心指标采集器 | Linux, Python |
| 2 | 容器化 —— 应用打包 | Docker |
| 3 | 多云部署 | Terraform, AWS, DigitalOcean |
| 4 | 可观测性 | Prometheus, Grafana |

构建进度记录在[项目日志](/zh/project-logs/)。
