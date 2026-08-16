# AGENTS.md

Guidance for AI agents working on this repository.

## What this is

A bilingual (English/Chinese) personal blog + engineering portfolio. Hugo (extended) + PaperMod theme, deployed to GitHub Pages by GitHub Actions on every push to `main`. No build step beyond `hugo --minify`; no tests; no package manager.

## Commands

```bash
hugo server -D --port 1313     # local preview (drafts included), en at /, zh at /zh/
hugo --minify                  # production build — must pass before every commit
./scripts/new-post.sh <category> <file>      # new English post
./scripts/new-post.sh zh <category> <file>   # new Chinese post
python tools/generate_og.py    # regenerate the OG share card after avatar/tagline changes
```

Categories: `daily`, `pitfalls`, `insights`, `reflections`, `project-logs`.

## Architecture

```
content/en/ + content/zh/   # posts and pages, mirrored per language
content/<lang>/project/<slug>/_index.md   # project hubs (see below)
archetypes/                 # per-category post templates
i18n/en.yaml, i18n/zh.yaml  # custom UI strings (merged with theme's)
layouts/                    # theme overrides — never edit themes/PaperMod (submodule)
layouts/_default/resume.html   # clean print-ready resume sheet — always light, no sky/animations
assets/css/extended/custom.css   # ALL custom styling, numbered sections
data/projects.yaml          # featured-project cards, keyed by language
static/image/               # avatar, og-cover.png
hugo.toml                   # config; menus & homeInfoParams exist PER LANGUAGE
```

## Constraints — the rules that bite

**Theme.** Never edit `themes/PaperMod/`. Override via `layouts/` partials/templates and `assets/css/extended/custom.css` (loaded last). New CSS goes in a new numbered section matching the existing style.

**Bilingual parity.** Any content, menu, i18n string, or page added in one language needs its counterpart in the other, or a conscious decision to skip. Menus and `homeInfoParams` live under `languages.en` / `languages.zh` in `hugo.toml` — edit both. Hardcoded strings in templates are forbidden: use `i18n` keys + `relLangURL`.

**`hugo new` is broken here.** With per-language `contentDir`, it always writes into the default language tree. Use `scripts/new-post.sh`, which instantiates archetypes manually.

**`layouts/partials/footer.html` shadows the theme footer.** PaperMod's theme-toggle handler lived there, so our override re-implements it (section 0 of the inline script). Removing it silently breaks dark/light switching. All site-wide JS lives in this one file.

**`post-single` stays solid.** Never apply `backdrop-filter`/glass to `.post-single` — it creates a containing block that breaks the fixed floating TOC, and long-form text needs a solid surface. Glass is only the selector list in custom.css section 27.

**Sky background is CSS-only** (no images, no WebGL). Theme-conditional via `[data-theme="dark"|"light"]` selectors. Every animation must have a `prefers-reduced-motion` fallback and `aria-hidden` markup.

**Easter eggs.** All eggs live in footer.html JS sections 12–13 + custom.css sections 32–33: Konami (↑↑↓↓←→←→BA), moon/sun click, Oct 25 golden Scorpius, typed words (`starry`/`scorpio`/`rocket`), logo ×5 disco, late-night toast, copy toast, mouse-circle gesture, rare (~4%) Van Gogh "Starry Night" (dark only), 404 lost meteor. Toast text is bilingual via the `isZh` lang check in JS — keep both strings when editing.

**Frontmatter.** TOML (`+++`). Every post needs a lead paragraph followed by `<!--more-->` (it becomes the home excerpt) and a `description`. Set `projects = ['<slug>']` to attach a post to a project hub; hubs at `/project/<slug>/` auto-aggregate across sections — do not create per-project directories anywhere else.

**Deploy.** Push to `main` triggers the full pipeline (build → link check → deploy). The lychee link check is intentionally non-blocking. There is no staging; `hugo --minify` locally is the gate.

**Housekeeping.** `public/`, `resources/`, `.hugo_build.lock` are gitignored — never commit, and never delete them while `hugo server` is running (stale-cache 404s follow).

## Definition of done

A change is complete when: `hugo --minify` builds with no errors, both `/` and `/zh/` render the change correctly in light AND dark themes (verify in a browser, screenshots preferred), and bilingual strings exist for any new UI text.
