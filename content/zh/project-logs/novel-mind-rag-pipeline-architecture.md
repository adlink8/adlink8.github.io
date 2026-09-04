+++
title = "项目日志：Novel-Mind 中文长文本分块与 RAG 检索管线搭建"
date = 2026-06-06T10:15:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ["project-logs"]
tags = ["Novel-Mind", "RAG", "FastAPI", "ChromaDB", "Ollama", "Python"]
projects = ["novel-mind"]
description = "记录面向中文长篇小说与复杂叙事文本的 RAG 检索流水线搭建，涵盖重叠滑动窗口分块、向量化评测与本地推理服务集成。"
+++

推进项目 `novel-mind` 的长文本检索流水线核心架构搭建：解决超长中文上下文中情节线索跳跃、传统定长切块语义碎片化的问题。

<!--more-->

---

## 1. 项目背景与当前阶段 (Context & Milestone)

- **项目标识**：`novel-mind`
- **核心定位**：面向数十万字中文长篇文本的本地化 RAG（检索增强生成）系统，基于 FastAPI、ChromaDB 与 Ollama 提供高保真叙事检索。
- **当前阶段**：🟢 **分块切片算法与 ChromaDB 向量索引管线完成，评测基线跑通**

在传统通用 RAG 系统中，简单的按字符或标点定长切块（如每 500 字强制切断）会导致长篇小说中的伏笔、人物关系与跨段落因果链条被硬生生切碎。当后续通过 Top-K 检索召回时，模型往往获得断章取义的上下文片段，引发不可控的叙事幻觉。

---

## 2. 核心架构设计 (Architecture Design)

系统整体采用本地化离线构建 + 在线低延迟检索的分层架构：

```text
[原始小说文本] 
      │
      ▼
[分层清洗器 (章节/对话/旁白)] 
      │
      ▼
[重叠语义窗口切片器 (Window Size=800, Overlap=200)] 
      │
      ▼
[BGE-M3 / 本地向量模型 (Ollama/PyTorch)] 
      │
      ▼
[ChromaDB 向量持久化与元数据层] 
      │
  [检索阶段]
      │
      ▼
[混合检索 (Dense Vector + BM25 Sparse)] 
      │
      ▼
[FastAPI 接口服务 (异步非阻塞)]
```

---

## 3. 关键实现：长文本重叠切片与元数据保留

针对中文小说文本的特殊结构，设计了包含章节层级与段落边界感知的滑动窗口切片器：

```python
from typing import List, Dict

class NovelChunker:
    def __init__(self, chunk_size: int = 800, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_paragraphs(self, text: str) -> List[str]:
        raw_paras = text.split("\n")
        return [p.strip() for p in raw_paras if p.strip()]

    def build_sliding_chunks(self, paragraphs: List[str], chapter_id: str) -> List[Dict]:
        chunks = []
        current_chunk = []
        current_len = 0
        chunk_index = 0

        for para in paragraphs:
            para_len = len(para)
            if current_len + para_len > self.chunk_size and current_chunk:
                combined_text = "\n".join(current_chunk)
                chunks.append({
                    "chunk_id": f"{chapter_id}_{chunk_index:04d}",
                    "chapter": chapter_id,
                    "text": combined_text,
                    "char_count": current_len
                })
                chunk_index += 1
                
                # 保持 overlap 语义回溯
                stride_tokens = 0
                retained = []
                for p in reversed(current_chunk):
                    if stride_tokens + len(p) <= self.overlap:
                        retained.insert(0, p)
                        stride_tokens += len(p)
                    else:
                        break
                current_chunk = retained
                current_len = sum(len(p) for p in current_chunk)

            current_chunk.append(para)
            current_len += para_len

        if current_chunk:
            chunks.append({
                "chunk_id": f"{chapter_id}_{chunk_index:04d}",
                "chapter": chapter_id,
                "text": "\n".join(current_chunk),
                "char_count": current_len
            })
        return chunks
```

---

## 4. 阶段评测与后续任务 (Next Steps)

1. **召回率评测 (Recall@K)**：构建第一批涵盖 50 个复杂跨章节线索的测试问答对，作为检索迭代的自动化 Benchmark；
2. **重排序机制 (Reranker)**：计划引入本地部署的 Cross-Encoder 模型（如 BGE-Reranker-Large），过滤 Top-20 召回中语义漂移的无关段落；
3. **接口接入**：将 ChromaDB 查询流水线封装为标准 FastAPI REST 接口，支持 Web 前端与桌面端交互。
