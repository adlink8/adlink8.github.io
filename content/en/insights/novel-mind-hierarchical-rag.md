+++
title = 'Hierarchical Narrative Memory: From Layer-by-Layer RAG to L0-L4 Bidirectional Retrieval'
date = 2026-07-15T09:11:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['insights']
tags = ['RAG', 'Architecture', 'Hierarchy']
projects = ['novel-mind']
description = 'From "LLMs build up layer by layer" to a complete bidirectional L0-L4 hierarchical narrative memory system.'
+++

From one naive intuition — "large models make progress layer by layer, so we can do RAG layer by layer too" — reasoned out to a complete hierarchical narrative memory architecture.

<!--more-->

## Overview

A novel RAG system cannot dump 100,000 characters into a vector store in one go. Content must be layered by narrative scale, with each layer storing information at a different granularity.

## Core Design

```
L0 source-text evidence → L1 scene facts → L2 chapter state → L3 volume/story phase → L4 whole-book world model
```

Analysis induces bottom-up; querying retrieves top-down.

## Node Data Contract

Every node stores deltas rather than just summaries: character_state_changes, relationship_changes, new_clues, resolved_clues, timeline_events, world_state_changes. Plus version, hash, confidence, parent-child links, and references back to source-text evidence.

## Preventing Error Amplification

- Source-text evidence is always the final authority
- High-level conclusions must be traceable back to the source text
- Any single failed layer can be rebuilt independently
- Retrieval must ultimately return leaf-layer citations to the source text

## Cost Control

- When source text and layer checksums agree, reuse the lower-layer assets
- Flip the active pointer only after a new version passes validation
- Re-run against the source text only the chapters that are missing or disqualified
