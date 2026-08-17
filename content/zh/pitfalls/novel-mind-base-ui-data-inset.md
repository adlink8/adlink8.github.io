+++
title = 'base-ui 的 data-inset 样式陷阱'
date = 2026-07-18T04:47:00+08:00
draft = false
ShowToc = true
TocOpen = true
categories = ['pitfalls']
tags = ['base-ui', 'CSS', '前端']
projects = ['novel-mind']
description = 'menu 不 emit data-inset 属性，是 recipe 自己设置的，依赖 DOM data 属性写样式踩空。'
+++

base-ui 的 Menu 组件不 emit data-inset 属性，CSS 选择器匹配不到，样式踩空。

<!--more-->

## Problem Description

期望通过 data-inset 属性控制菜单项缩进。CSS 选择器依赖 [data-inset]。

## Root Cause

base-ui Menu 不 emit data-inset。是 Radix DropdownMenuLabel/Item recipe 层自己设置的。直接用 base-ui Menu 时，data-inset 不存在。

## Solution

确认组件链路：base-ui → Radix recipe → 自定义 data 属性。样式必须跟随 recipe 层约定。

## Prevention

使用 base-ui 前确认组件 API surface；文档化组件属性契约。
