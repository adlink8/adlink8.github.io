+++
title = "Project Log: Novel-Mind Long-Text Chunking and RAG Pipeline Setup"
date = 2026-06-06T10:15:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ["project-logs"]
tags = ["Novel-Mind", "RAG", "FastAPI", "ChromaDB", "Ollama", "Python"]
projects = ["novel-mind"]
description = "Milestone log on building the RAG retrieval pipeline for long-form Chinese narratives, featuring overlapping sliding-window chunking, evaluation benchmarks, and local inference integration."
+++

Advancing core architecture for project `novel-mind`: tackling semantic fragmentation and narrative plot jumps in long Chinese contexts.

<!--more-->

---

## 1. Context and Current Milestone

- **Project Identifier**: `novel-mind`
- **Core Position**: Localized RAG (Retrieval-Augmented Generation) system tailored for 100k+ word Chinese fiction, delivering high-fidelity narrative recall via FastAPI, ChromaDB, and Ollama.
- **Current Milestone**: 🟢 **Chunking engine and ChromaDB vector indexing operational; baseline benchmark established**

In generic RAG pipelines, naive character-based or fixed-token slicing (e.g., cutting strictly at 500 characters) tears apart character relationships, foreshadowing, and cross-paragraph causal threads. Retrieving Top-K chunks out of context causes severe narrative hallucination.

---

## 2. Architecture Overview

The system adopts an offline index construction + online low-latency retrieval architecture:

```text
[Raw Fiction Text]
      │
      ▼
[Hierarchical Cleaner (Chapters / Dialogues / Narration)]
      │
      ▼
[Overlapping Semantic Window Chunker (Size=800, Overlap=200)]
      │
      ▼
[BGE-M3 / Local Embedding Model (Ollama / PyTorch)]
      │
      ▼
[ChromaDB Vector Store & Metadata Store]
      │
  [Online Retrieval Stage]
      │
      ▼
[Hybrid Retrieval (Dense Vector + BM25 Sparse)]
      │
      ▼
[FastAPI REST Service (Async Non-blocking)]
```

---

## 3. Key Implementation: Semantic Sliding Window with Metadata Retention

A sliding chunker preserving paragraph integrity and chapter lineage:

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
                
                # Backtrack for overlap
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

## 4. Evaluation and Next Steps

1. **Recall Evaluation (Recall@K)**: Construct 50 multi-hop narrative query-ground truth pairs to serve as an automated evaluation benchmark;
2. **Cross-Encoder Reranker**: Deploy a local cross-encoder model to re-score Top-20 dense candidates, filtering out drifted noise;
3. **API Integration**: Expose standard REST endpoints over FastAPI for client-side consumption.
