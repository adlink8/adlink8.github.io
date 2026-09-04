+++
title = '2026-02-20 研发日志：AI-Factory 容器化编排首跑与三层分工确立'
date = 2026-02-20T23:15:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['daily']
tags = ['Docker', 'n8n', 'AI-Workflow', 'DevOps']
projects = ['devops-roadmap']
description = '2026-02-20 记录：AI-Factory 自动化工场首次在 Docker Compose 下启动成功，并确立战略-研发-资产化三站式协作架构。'
+++

今天在 Docker Compose 下成功跑通了自动化系统 `AI-Factory` 的核心节点，排查解决了 Task Broker 报错，并正式确立了三站式流水线架构。

<!--more-->

### 今日工作内容 (What I Did Today)

- [x] 编写 `docker-compose.yml` 并在 WSL 2 中拉起 n8n 核心编排容器；
- [x] 排查定位 n8n 容器缺少 Python 运行时导致的 Task Broker 启动异常；
- [x] 构建派生 Dockerfile，注入 Python 3 运行时，使任务状态机恢复绿色；
- [x] 在团队架构讨论中正式提出“战略指挥部 - 工程研发部 - 品牌资产化部”三层分工模型。

### 关键挑战与心得 (Challenges & Insights)

- **容器排障必须看原生输出**：使用 `docker logs --tail 50` 快速捕获到了 Alpine 镜像裁剪导致 Python 缺失的铁证，避免了无休止的外部猜疑。
- **阶段性成果必须独立落盘**：长链条自动化如果某一步失败，必须支持单节点成果保存与人工介入。

### 涉及工具与资源 (Tools Used)

- `Docker Compose`
- `n8n`
- `WSL 2`
- `Alpine Linux`

### 下一步行动 (Next Steps)

- [ ] 撰写一份详尽的 Python Task Runner 缺失排障笔记（沉淀至 `pitfalls`）；
- [ ] 细化三站式流水线的数据接口契约（沉淀至 `insights`）。
