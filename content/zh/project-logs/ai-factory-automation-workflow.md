+++
title = '项目日志：AI-Factory 本地自动化流水线搭建与容器化实践'
date = 2026-02-20T22:30:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['project-logs']
tags = ['Docker', 'n8n', 'DevOps', '自动化', '流水线']
projects = ['devops-roadmap']
description = '记录 AI-Factory 项目从零在 Docker 中拉起 n8n、打通 Python 脚本执行、并连接 LLM API 的全流程构建进度。'
+++

启动本地 AI 自动化流水线系统 `AI-Factory`，目标是将分散的脚本执行与大模型 API 交互整合为可视化、可追溯且具备自愈能力的事件驱动架构。

<!--more-->

---

## 1. 项目概览与当前状态 (Project Overview & Status)

- **项目名称**：`AI-Factory`
- **项目定位**：基于本地 Docker 运行的事件驱动自动化工场，连接上游战略规划、中游代码测试与下游知识沉淀。
- **当前状态**：🟡 **核心容器启动，任务流验证中 (In Progress)**

---

## 2. 核心目标 (Goals)

1. 在本地 Windows + WSL 2 环境下通过 Docker Compose 一键启动完整的 n8n 自动化基础设施；
2. 解决官方镜像缺失 Python 环境导致的 Task Broker 报错；
3. 打通 Webhook $\to$ LLM 格式转换 $\to$ 本地文件落盘的闭环数据流；
4. 实现各节点执行状态的独立存储与人工干预审查机制。

---

## 3. 技术栈 (Tech Stack)

<p class="resume-stack">
  <code>Docker Compose</code> <code>WSL 2</code> <code>n8n</code> <code>Python 3.12</code> <code>FastAPI</code> <code>Git</code>
</p>

---

## 4. 进度追踪 (Progress Log)

### 阶段一：基础编排与环境封装 (2026-02-20)
- [x] 编写 `docker-compose.yml`，定义 n8n 服务与本地卷持久化映射（`./n8n_data:/home/node/.n8n`）；
- [x] 遇到容器内部 Python Task Runner 缺失报错（`Failed to start Python task runner in internal mode`）；
- [x] 编写定制 Dockerfile，在 Alpine 镜像内注入 `python3`、`py3-pip` 与编译工具链，成功使 Task Broker 变绿就绪；
- [x] 映射 5678 端口并完成初次 Web UI 初始化配置。

### 阶段二：节点连接与数据流调试 (2026-02-22 ~ 02-23)
- [x] 搭建第一个完整的 JSON 数据清洗流；
- [x] 解决表达式模式（Expression Mode）与字面量模式（Fixed Mode）在数据类型解析上的混淆；
- [x] 明确为什么在大模型处理前需要将原始 Markdown 文本进行清洗剥离，避免无效 Token 消耗。

---

## 5. 当前阶段交付成果 (Current Deliverables)

- 完整的本地部署配置文件与容器自愈脚本，存放在 `D:\ADLINK\DockerWorkspace\AI-Factory`；
- 跑通从 HTTP 触发到 Python 数据处理的基线节点；
- 沉淀了一份针对 n8n Task Runner 报错的排障指南（见 [`/pitfalls/n8n-docker-python-task-runner-missing/`](/zh/pitfalls/n8n-docker-python-task-runner-missing/)）。

---

## 6. 下一步计划 (Next Steps)

- [ ] 接入多模型 API 聚合调度，支持按任务复杂度在轻量模型与推理模型之间自动路由；
- [ ] 完善错误重试机制与企业微信 / 邮件告警通知；
- [ ] 将稳定跑通的业务节点剥离为独立微服务。
