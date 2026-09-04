+++
title = "2026-03-03 研发日志：代码审查方案优化"
date = 2026-03-03T12:41:02+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['daily']
tags = ["Gemini Apps", "Cursor", "数据分析", "GPT-5", "工业"]
projects = ["devops-roadmap"]
description = "2026-03-03 记录：共涉及 10 次操作，重点开展 代码审查方案优化 相关工程实施与协同。"
+++

本日聚焦于 代码审查方案优化，通过 Cursor、GPT-5、Gemini Apps 等工具协同推进，累计记录 10 次工程与调试事件。

<!--more-->

### 今日工作内容 (What I Did Today)

- [x] 代码审查方案优化
- [x] 你是一个资深的程序员 (Engineer)。 请根据以下提供的【需求背景】，编写出完整的核心代码。 【需求背景】： 请注意：如果上述内容是一段详细的战略蓝图，请严格按蓝图实现；如果只是一句简短的口语化指令（如“帮我写个ESP32代码”），请发挥你的专业知识，自动补全最优的架构和逻辑，直接给出完整的代码实现。要求代码带有清晰的注释。 现在有严重的问题，研发室不能看到 审查员返回的建议，所以一直重复生成 AI自动流
- [x] 这一步不就是一直获取开头的数据嘛开头主要还是一直收不到反馈，看截图 AI自动流
- [x] 所以说是我的数据太多了把n8n干爆了，具体怎么设置保命措辞 并且能流畅运行 AI自动流
- [x] services: n8n: image: n8nio/n8n:latest user: "root" restart: always ports: - "5678:5678" environment: - N8N_HOST=localhost - N8N_PORT=5678 - N8N_PROTOCOL=http - NODE_ENV=production # 🔑 极重要：这是你的加密密钥，用于保护你的 API Key 等敏感信息 # 建议随机生成一段 32 位字符串 - N8N_ENCRYPTION_KEY=my_secret_key_2026_8845h # 🚀 针对 AI 节点的内存优化 - NODE_OPTIONS=--max-old-space-size=4096 - N8N_RESTRICT_FILE_ACCESS_TO=/output - N8N_USER_FOLDER=/home/node volumes: - D:/ADLINK/DockerData/n8n:/home/node/.n8n - D:/ADLINK/Docker_projects/output:/ou
- [x] 截图分别是每次的检查内容，反而越检查越改错误越多，这样代码永远通过不了，第四张截图现在研发员能够看到审查员的反馈意见并进行修改，第三次审查直接通过就行吧，审查目的是尽可能减少错误而不是完美百分百 达到百分之80 剩下的在vccode里配合coilot进行细致性代码，但是又有个问题代码是有一点问题的那根据代码出的教程岂不是会带偏导致错误教学，怎么解决 AI自动流

### 关键收获与技术思考 (Key Insights & Challenges)

- **协同效率**：在 2026-03-03 期间，重点借助 Cursor 完成关键逻辑梳理与调试验证。
- **工程细节**：累计交互 10 次，涉及 工业 / 业务应用、数据分析 / 数据处理、编程 / 调试 / 开发。

### 涉及工具与服务 (Tools & Services)

- `Cursor`
- `GPT-5`
- `Gemini Apps`

### 下一步行动 (Next Steps)

- [ ] 继续跟进当前模块的边界用例与持续集成验证
- [ ] 将本次排障经验与代码变动同步沉淀至相关文档
