+++
title = 'n8n 工作流踩坑：Loop 循环节点与 All Items 状态不匹配排错'
date = 2026-03-01T15:20:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['pitfalls']
tags = ['n8n', '工作流', '数据流', '排障', 'DevOps']
projects = ['devops-roadmap']
description = '排查 n8n 工作流中关于“最后一个节点提示只能用于 all items，但节点处于 each item 状态”的数据流断裂错误与数据聚合解法。'
+++

在设计多节点链式自动工作流时，当把循环迭代逻辑连接至下游存储或聚合节点时，频繁遭遇“数据上下文维度不匹配”导致的死循环或报错。本文梳理 n8n 批处理上下文的底层逻辑与修复要点。

<!--more-->

---

## 1. 问题描述 (Problem Description)

在 `AI-Factory` 工作流中，设计了一个循环处理多篇技术摘要的流水线：前置节点通过 API 批量抓取数据，中间节点使用 Loop 逐条送入 LLM 模型提取关键点，最后一步试图将结果批量打包写入数据库。

然而工作流在最后一个节点中断，报错提示：**“该节点操作只能接收 All Items 模式，但输入数据当前处于 Each Item 上下文”**，导致后续流程无法继续执行或输出结果仅保留了最后一条。

## 2. 复现环境 (Environment)

- **工具平台**：n8n (Self-Hosted on Docker)
- **主要节点**：`HTTP Request` $\to$ `Loop Over Items` (Split in Batches) $\to$ `Code Node` $\to$ `Postgres / Local Storage`
- **数据结构**：包含 10+ 篇技术文档的 JSON 数组

## 3. 报错现象 (Error Message)

UI 节点提示与控制台错误：

```text
NodeExecutionError: Invalid input data format
This operation can only be executed on 'All Items', but the previous node passed an 'Each Item' stream.
Current context: iteration loop_index=9, remaining=0. Upstream node closed without aggregating batch outputs.
```

## 4. 根本原因 (Root Cause)

1. **n8n 的数据流二元模型**：
   - **All Items 状态**：数据作为一组完整的数组流转，下游节点一次性处理所有条目（例如批量数据库 INSERT）。
   - **Each Item 状态**：进入 Loop 循环或开启了逐条触发，数据被拆解为单条独立流转，每条数据拥有独立的执行索引（`$itemIndex`）。
2. **错误的汇聚闭环连线**：
   - Loop 节点的输出有两个端口：`loop (循环体)` 和 `done (循环结束)`。
   - 错误的做法是将循环体内部的最后一个处理节点直接连向下游存储节点，导致下游节点在每一次循环中都被触发一次，且仅接收到单条数据；而下游存储节点配置的又是“批量模式”，从而引发类型断言冲突。
3. **缺少聚合归一中间节点**：
   - 在循环结束后，必须通过聚合（Aggregate / Item Lists）将 Each Item 重新折叠打包为 All Items。

---

## 5. 解决方案 (Solution)

### 步骤 1：正确连接 Loop 节点的两个输出端

确保数据流闭环：
- 循环体内部节点处理完成后，必须回连到 `Loop Over Items` 节点的输入端（完成一次迭代）。
- 只有当循环彻底结束触发 `done` 端口时，才进入下一阶段：

```
[批量数据获取] ──► [Loop Over Items] ──(loop)──► [LLM 处理] ──► [Code 格式化] ──┐
                         │                                                       │
                         │ ◄─────────────────────────────────────────────────────┘
                         │
                      (done)
                         ▼
             [Aggregate / Item Lists] ──► [下游批量存储 / 导出]
```

### 步骤 2：在 `done` 端口后引入 `Aggregate` 节点

在 `done` 之后添加一个 `Aggregate`（或 `Item Lists -> Aggregate Items`）节点：
- **Aggregate By**：选择 `All Items into a single list`
- **Fields to Include**：指定需要保留的字段（如 `title`, `summary`, `timestamp`）

这样可将多轮迭代产生的分散输出，安全转换为标准 JSON 数组传递给数据库。

---

## 6. 防范措施 (Prevention)

- **理解状态而非盲目拖拽**：在 n8n 中，每次连线前必须清楚当前端口输出的是“数组（All Items）”还是“流（Each Item）”。
- **利用 Mock 数据测试小样本**：在调试复杂 Loop 逻辑时，在首个节点配置 `Limit: 2`，先观察两轮迭代的输入输出结构，确认聚合无误后再开放全量数据。

---

## 7. 参考资料 (References)

- [n8n Docs: Looping in n8n workflows](https://docs.n8n.io/workflows/loops/)
- [n8n Docs: Item Lists & Data Aggregation](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.itemlists/)
