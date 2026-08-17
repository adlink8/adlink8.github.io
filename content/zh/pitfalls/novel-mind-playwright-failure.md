+++
title = 'Playwright 验收卡死：浏览器自动化在 Windows 上的反复失败'
date = 2026-08-12T00:00:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['pitfalls']
tags = ['Playwright', 'Windows', '验收']
projects = ['novel-mind']
description = 'Playwright 浏览器自动化在 Windows 上反复安装/启动失败或超时。'
+++

Playwright 浏览器自动化验收反复失败，最终被强制终止并改用证据化验收。

<!--more-->

## Problem Description

Playwright 用于前端 UI 自动化验收。08-12 全面审计阶段反复安装/启动失败或超时。

## Root Cause

Windows 环境下 Playwright 依赖的浏览器二进制文件安装路径、系统权限、网络下载存在多层不确定性。高并发子代理环境下加剧。

## Solution

```
用户指令："立即停止所有浏览器/测试等待。不要再尝试安装或启动新浏览器。有 UI 证据就报告，没有就如实说。"
```

强制终止，改用代码级验证（grep + diff）+ 截图证据。

## Prevention

- UI 自动化不应依赖本地浏览器安装
- 设置超时上限，超时即 fallback
- 区分"必须跑通"和"有证据即可"的验收标准
