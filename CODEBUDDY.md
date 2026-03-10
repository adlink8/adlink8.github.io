# CODEBUDDY.md

This file provides guidance to CodeBuddy Code when working with code in this repository.

## Project Overview

This is a Hugo static site blog documenting a DevOps and Infrastructure as Code learning journey. The site uses the PaperMod theme and deploys automatically to GitHub Pages via GitHub Actions.

## Common Commands

```bash
# Start local development server
hugo server -D --port 1313
# Or use the convenience script
./start.sh

# Create a new post (use hyphens, not spaces)
hugo new <category>/<filename>.md
# Or use the convenience script
./new-post.sh <category> <filename>

# Build for production
hugo --minify

# Launch GUI blog manager
python blog_manager.py
```

## Content Categories

Posts are organized into 5 categories, each with its own archetype template:

| Category | Directory | Purpose |
|----------|-----------|---------|
| daily | `content/daily/` | Timeline/Daily progress logs |
| pitfalls | `content/pitfalls/` | Lab Notes/Troubleshooting |
| insights | `content/insights/` | Architecture & deep dives |
| reflections | `content/reflections/` | Retrospectives |
| project-logs | `content/project-logs/` | Build progress logs |

## Architecture

```
├── archetypes/          # Post templates per category (defines frontmatter structure)
├── content/             # All blog posts (Markdown with TOML frontmatter)
├── layouts/             # Custom Hugo layouts (overrides theme defaults)
├── themes/PaperMod/     # Hugo theme (git submodule - do not edit directly)
├── static/image/        # Static assets (images, etc.)
├── hugo.toml            # Hugo configuration
├── public/              # Generated site (gitignored)
└── .github/workflows/   # GitHub Actions auto-deployment
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

1. Create post using `./new-post.sh <category> <filename>` or `hugo new`
2. Run `hugo server -D` to preview locally at http://localhost:1313
3. Edit the Markdown file in `content/<category>/`
4. Set `draft = false` when ready to publish
5. Commit and push - GitHub Actions handles deployment automatically

## GUI Blog Manager

`blog_manager.py` is a Python/Tkinter GUI tool with features:
- Create/delete posts via form interface
- Start/stop Hugo server
- Git operations (add, commit, push)
- Deploy to GitHub

Launch with `python blog_manager.py`.
