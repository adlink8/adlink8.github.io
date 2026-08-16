# CODEBUDDY.md

This file provides guidance to CodeBuddy Code when working with code in this repository.

## Project Overview

This is a Hugo static site blog documenting a DevOps and Infrastructure as Code learning journey. The site uses the PaperMod theme and deploys automatically to GitHub Pages via GitHub Actions.

## Common Commands

```bash
# Start local development server
hugo server -D --port 1313
# Or use the convenience script
./scripts/start.sh

# Create a new post (use hyphens, not spaces)
# Bilingual: language is the first argument (en default, zh for Chinese)
./scripts/new-post.sh <category> <filename>      # English post
./scripts/new-post.sh zh <category> <filename>   # Chinese post

# Build for production
hugo --minify

# Launch GUI blog manager
python tools/blog_manager.py
```

## Content Categories

The site is bilingual: English content lives in `content/en/` (served at `/`), Chinese in `content/zh/` (served at `/zh/`). Posts are organized into 5 categories, each with its own archetype template:

| Category | Directory | Purpose |
|----------|-----------|---------|
| daily | `content/<lang>/daily/` | Timeline/Daily progress logs |
| pitfalls | `content/<lang>/pitfalls/` | Lab Notes/Troubleshooting |
| insights | `content/<lang>/insights/` | Architecture & deep dives |
| reflections | `content/<lang>/reflections/` | Retrospectives |
| project-logs | `content/<lang>/project-logs/` | Build progress logs |

Standalone pages: `projects.md` (showcase), `now.md` (current focus), `stats.md` (build-time stats via the `blogstats` shortcode), `archives.md`, `search.md` — each exists in both language trees.

## Architecture

```
├── archetypes/          # Post templates per category (defines frontmatter structure)
├── content/en/          # English posts & pages (served at /)
├── content/zh/          # Chinese posts & pages (served at /zh/)
├── i18n/                # Custom UI strings (en.yaml, zh.yaml), merged with theme's
├── layouts/             # Custom Hugo layouts (overrides theme defaults)
├── themes/PaperMod/     # Hugo theme (git submodule - do not edit directly)
├── static/image/        # Static assets (images, etc.)
├── scripts/             # Shell scripts (start.sh, new-post.sh, watchdog.sh)
├── tools/               # Python tools and Windows launch files
├── docs/                # Project documentation
├── hugo.toml            # Hugo configuration (multilingual: languages.en / languages.zh)
├── public/              # Generated site (gitignored)
└── .github/workflows/   # GitHub Actions auto-deployment (+ weekly scheduled rebuild)
```

**Key points:**
- Theme is a git submodule in `themes/PaperMod/` - do not edit directly
- Custom layouts in `layouts/` override theme defaults
- Build output goes to `public/` (gitignored, generated on deploy)
- Deployment is automatic via GitHub Actions on push to `main`

## Frontmatter Structure

All posts use TOML frontmatter with `+++` delimiters:

```toml
+++
title = 'Post Title'
date = '2024-01-15T10:00:00+08:00'
draft = true
ShowToc = true
TocOpen = true
categories = ['category-name']
tags = ['tag1', 'tag2']
+++
```

## Development Workflow

1. Create post using `./scripts/new-post.sh <category> <filename>` or `hugo new`
2. Run `hugo server -D` to preview locally at http://localhost:1313
3. Edit the Markdown file in `content/<category>/`
4. Set `draft = false` when ready to publish
5. Commit and push - GitHub Actions handles deployment automatically

## GUI Blog Manager

`tools/blog_manager.py` is a Python/Tkinter GUI tool with features:
- Create/delete posts via form interface
- Start/stop Hugo server
- Git operations (add, commit, push)
- Deploy to GitHub

Launch with `python tools/blog_manager.py`.
