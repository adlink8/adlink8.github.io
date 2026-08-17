# 内容写作指南

这个博客怎么写文章、每个分类写什么、聚合页怎么聚合。配合 `AGENTS.md`（技术约束）使用。

## 总览

- 双语：英文在 `content/en/`（根路径 `/`），中文在 `content/zh/`（`/zh/` 前缀）。**任何一边新增内容，另一边要有对应版本**（或有意识地决定跳过）。
- 五个文章分类（section）：`daily`（时间线）、`pitfalls`（实验笔记）、`insights`（深度解析）、`reflections`（复盘）、`project-logs`（项目日志）。
- 新建文章**不要用 `hugo new`**（双语 contentDir 下有 bug），用脚本：

```bash
./scripts/new-post.sh daily my-first-post        # 英文，草稿
./scripts/new-post.sh zh daily my-first-post     # 中文，草稿
```

脚本会按 `archetypes/<category>.md` 模板生成文件，`draft = true`，写完改成 `draft = false` 才会发布。

## 通用 frontmatter 规范

每篇文章头部（TOML，`+++` 包裹）：

```toml
title = '文章标题'
date = 2026-08-17T10:00:00Z
draft = false                    # 发布前必须改 false
ShowToc = true                   # 显示右侧浮动目录
TocOpen = true
categories = ['daily']           # 脚本已按分类填好，别改
tags = ['linux', 'docker']       # 自由标签，出现在标签聚合页
projects = ['novel-mind']        # 关键！挂到项目聚合页，见下文
description = '一句话描述'        # SEO/分享卡片用
```

正文第一屏规则（**每篇都要**）：

1. 开头一段 1–2 句的导语 —— 它会同时成为首页/列表页的摘要；
2. 紧跟一行 `<!--more-->` —— 摘要到此为止，后面是正文。

漏了 `<!--more-->` 首页摘要会变成一大坨，漏了导语摘要会是空的。

## 五个分类怎么写

### 📅 daily —— 时间线（每日进展）

- **定位**：给自己看的每日工作日志，短平快，当天的事当天记。
- **特殊性**：`/daily/` 页面右侧有**年月日时间轴**（自动按日期聚合，≥1350px 宽屏显示），所以日期必须准确。
- **结构**（archetype 已给好）：Summary → What I Did Today（checklist）→ Challenges Faced → Resources Used → Next Steps。
- **要点**：宁可写 5 行真话，不写 500 字流水账；遇到的坑如果值得展开，移到 `pitfalls` 单独成文，daily 里留一句链接。

### 🛠️ pitfalls —— 实验笔记（排障记录）

- **定位**：一个具体问题 → 根因 → 解法的完整闭环。求职时这是最硬的证据：展示你解决问题的过程。
- **结构**：Problem Description → Environment（OS/版本/上下文）→ Error Message（原文贴进代码块）→ Root Cause → Solution（分步，命令用 ```bash 代码块）→ Prevention → References。
- **要点**：错误信息**贴原文**；根因写清楚"为什么"而不只是"怎么修"；Prevention 是加分项，别省。

### 💡 insights —— 深度解析（架构思考）

- **定位**：概念/架构的深入拆解，展示理解深度。频率低、质量高。
- **结构**：Overview → Why It Matters → Core Concepts → Architecture Diagram（ASCII 图放代码块）→ 可自由延伸。
- **要点**：每篇只讲透一个主题；和你做过的项目挂钩（`projects` 挂上对应 slug），"我用这个思想做了 X"比纯理论有说服力。

### 🔄 reflections —— 复盘（阶段回顾）

- **定位**：周期性回顾（周/月/里程碑结束），元认知展示。
- **结构**：Period Overview → Goals vs Reality（表格）→ What Went Well / What Could Improve → Lessons Learned（Technical / Personal 分开）→ Action Items → Next Period Focus。
- **要点**：Goals vs Reality 表格要诚实，没达成写没达成及原因；Action Items 必须可执行（下周能勾选的那种）。

### 📁 project-logs —— 项目日志（构建进度）

- **定位**：某个具体项目的构建过程记录，**必须**挂 `projects = ['<slug>']`，让它出现在项目聚合页。
- **结构**：Project Overview + Status → Goals → Tech Stack → Progress Log（按周/会话追加）→ Current Status → Next Steps。
- **要点**：一个项目可以有多篇日志（里程碑式推进），都挂同一个 slug；项目完结时在最后一篇写清验收结果。

## 聚合页怎么聚合

### 项目聚合页 `/project/<slug>/`（核心机制）

**聚合规则**（`layouts/_default/list.html`）：凡是 frontmatter 里 `projects` 包含该 slug 的文章，**不管在哪个分类**，全部自动汇聚到这个页面，按日期排列。存在 ≠ 集成：只建聚合页没文章挂上去就是空页。

**新建一个项目聚合页**（双语各建一份）：

```bash
content/en/project/<slug>/_index.md
content/zh/project/<slug>/_index.md
```

内容模板：

```toml
+++
title = 'NovelMind — 长文本 RAG 平台'
description = '一句话：这个项目是什么、做到了什么程度。'
date = 2026-08-17
layout = 'list'
+++

<p class="resume-stack"><code>Python</code> <code>FastAPI</code></p>

时间跨度 · 关键数据（会话数/事件数/token 等硬指标）
```

**把文章挂进项目**：文章 frontmatter 加 `projects = ['<slug>']`（数组，可挂多个）。不要在别处手动建 per-project 目录，路由只靠这一个机制。

**Slug 命名**：小写连字符，与 GitHub 仓库名一致（`novel-mind`、`t5ai-codex-quota`、`devops-roadmap`）。

### 首页

- 文章流：自动收录 `mainSections` 五个分类的最新文章（frontmatter 加 `hiddenInHomeList = true` 可排除）。
- 顶部个人卡片：`hugo.toml` 里 `languages.<lang>.params.homeInfoParams.Content`（Markdown），双语各一份。
- "精选项目"卡片：来自 `data/projects.yaml`，按语言键控，改项目要去那里改。

### 分类列表页 `/daily/` 等

- 每个分类根目录的 `_index.md` 提供标题和一句介绍（如 `content/zh/daily/_index.md`）。
- `/daily/` 额外有右侧年月日时间轴，全自动，无需维护。

### 归档 `/archives/`、标签 `/tags/`、分类 `/categories/`

- 全自动（PaperMod 内置 archives 布局 + taxonomy），`tags`/`categories` 写对就自动归组，无维护成本。

## 固定页面怎么维护

| 页面 | 文件 | 维护方式 |
|------|------|----------|
| 项目 `/projects/` | `content/<lang>/projects.md` | **手动**：每个项目一个 `<div class="project-card">` HTML 块（标题/链接/技术栈 code 标签/要点列表），照抄现有卡片改 |
| 项目聚合 `/project/<slug>/` | `content/<lang>/project/<slug>/_index.md` | 建一次，之后靠文章 `projects` 自动聚合 |
| 近况 `/now/` | `content/<lang>/now.md` | 手动，每月/焦点变化时更新，记得改"最后更新"月份 |
| 统计 `/stats/` | `content/<lang>/stats.md` | **全自动**（`{{< blogstats >}}` shortcode 构建时算：文章数/字数/活跃天数/连续天数），页面文字可改，数字不用管 |
| 简历 `/resume/` | `content/<lang>/resume.md` | 手动，`layout = 'resume'` 白纸样式（永远浅色、可打印 A4）；工作经历和教育经历是求职核心，及时更新 |
| 搜索 `/search/` | `content/<lang>/search.md` | 全自动，不用动 |
| 归档 `/archives/` | `content/<lang>/archives.md` | 全自动，不用动 |
| 404 | `layouts/404.html` + i18n `nf_*` | 不用动 |

固定页面的双语规则同文章：改一边记得改另一边。

## 发布检查清单

1. `draft = false`，导语 + `<!--more-->` + `description` 齐全；
2. 属于某个项目的文章：`projects = ['<slug>']` 已挂；
3. 双语版本都建了（或明确不发双语）；
4. `hugo --minify` 本地构建无 ERROR；
5. 浏览器里明暗两个主题各看一眼（`http://127.0.0.1:1313` 和 `/zh/`）；
6. push 后 `gh run list --limit 1` 确认 Actions 绿。
