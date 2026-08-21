+++
title = 'Playwright Acceptance Deadlock: Browser Automation Failing Repeatedly on Windows'
date = 2026-08-12T00:00:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['pitfalls']
tags = ['Playwright', 'Windows', 'Acceptance']
projects = ['novel-mind']
description = 'Playwright browser automation repeatedly failed to install/launch or timed out on Windows.'
+++

Playwright-driven UI acceptance kept failing; it was eventually force-terminated and replaced with evidence-based acceptance.

<!--more-->

## Problem Description

Playwright powered the automated frontend UI acceptance checks. During the 08-12 full audit, it repeatedly failed to install/launch or timed out.

## Root Cause

On Windows, the browser binaries Playwright depends on carry multiple layers of uncertainty: install paths, system permissions, and network downloads. High-concurrency subagent environments amplified all of it.

## Solution

```
用户指令："立即停止所有浏览器/测试等待。不要再尝试安装或启动新浏览器。有 UI 证据就报告，没有就如实说。"
```

(The verbatim operator instruction that broke the loop: "Immediately stop all browser/test waits. Do not attempt to install or launch another browser. Report UI evidence if you have it; if not, say so honestly.")

Force termination; switched to code-level verification (grep + diff) plus screenshot evidence instead.

## Prevention

- UI automation should not depend on locally installed browsers
- Set hard timeout caps and fall back the moment they trip
- Separate acceptance criteria into "must run green" versus "evidence is enough"
