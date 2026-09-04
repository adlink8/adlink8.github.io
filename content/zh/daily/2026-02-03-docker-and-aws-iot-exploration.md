+++
title = '2026-02-03 研发日志：Docker 笔记容器初部署与 AWS IoT 链路探索'
date = 2026-02-03T23:50:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['daily']
tags = ['Docker', 'AWS', 'IoT', 'DevOps']
projects = ['devops-roadmap']
description = '2026-02-03 记录：成功通过 Docker 部署第一个本地自托管笔记容器，打通虚拟网关与 AWS IoT 模拟链路。'
+++

今天迈出了自托管容器化与云端物联的第一步：用 Docker 跑起了笔记服务，并通过 Python 脚本验证了从虚拟机模拟网关到 AWS 的数据上报。

<!--more-->

### 今日工作内容 (What I Did Today)

- [x] 用 Docker 在本地成功拉起并持久化一个笔记容器，体验镜像部署的便捷性；
- [x] 使用 FinalShell 远程连接本地 Linux 虚拟机，配置虚拟网络环境；
- [x] 编写 Python `requests` 脚本模拟硬件传感器，向虚拟机本地数据库入库温湿度数据；
- [x] 查阅 AWS SAA 备考指南，梳理 IoT 架构师与系统运维工程师的核心技能边界。

### 关键挑战与心得 (Challenges & Insights)

- **直接拉镜像 vs 自建配置**：拉取现成镜像虽然快，但要真正理解容器网络、端口映射与卷挂载，必须亲手编写 Dockerfile 和 Compose 文件。
- **避免只做“代码搬运工”**：过去习惯复制 AI 给的指令，从今天起每一个参数都要对照官方文档理解其生效机理。

### 涉及工具与资源 (Tools Used)

- `Docker Desktop`
- `FinalShell`
- `Ubuntu VM`
- `Python requests`

### 下一步行动 (Next Steps)

- [ ] 对照 roadmap.sh 系统梳理 DevOps 与 Linux 底层学习规划；
- [ ] 探索通过 MQTT 协议替代简单的 HTTP 请求进行长连接通信。
