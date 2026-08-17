+++
title = '分层叙事记忆架构：从 RAG 一层一层到 L0-L4 双向检索'
date = 2026-07-15T09:11:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['insights']
tags = ['RAG', '架构', '分层']
projects = ['novel-mind']
description = '从"大模型是一层一层过来的"到完整的 L0-L4 双向分层叙事记忆系统。'
+++

从一个朴素直觉——"大模型是一层一层过来的，我们也可以 RAG 一层一层"——推理出完整的分层叙事记忆架构。

<!--more-->

## Overview

小说 RAG 不能把 10 万字一股脑丢进向量库。需要按叙事尺度分层，每层存储不同粒度的信息。

## 核心设计

```
L0 原文证据 → L1 场景事实 → L2 章节状态 → L3 卷/故事阶段 → L4 全书世界模型
```

分析时自下而上归纳，查询时自上而下检索。

## 节点数据契约

每个节点存储"变化量"而非只存摘要：character_state_changes、relationship_changes、new_clues、resolved_clues、timeline_events、world_state_changes。版本、哈希、置信度、父子关系、原文证据引用。

## 错误放大防范

- 原文证据永远是最终权威
- 高层结论必须可追溯原文
- 某一层失败可单独重建
- 检索最终必须返回叶子层原文引用

## 成本控制

- 原文与层级 checksum 一致则复用底层资产
- 新版本验证通过后切换 active pointer
- 仅缺失或不合格的章节回原文重跑
