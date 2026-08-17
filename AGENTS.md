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

**Frontmatter.** TOML (`+++`). Every post needs a lead paragraph followed by `<!--more-->` (it becomes the home excerpt) and a `description`. Set `projects = ['<slug>']` to attach a post to a project hub; hubs at `/project/<slug>/` auto-aggregate across sections — do not create per-project directories anywhere else.

**Deploy.** Push to `main` triggers the full pipeline (build → link check → deploy). The lychee link check is intentionally non-blocking. There is no staging; `hugo --minify` locally is the gate.

**Housekeeping.** `public/`, `resources/`, `.hugo_build.lock` are gitignored — never commit, and never delete them while `hugo server` is running (stale-cache 404s follow).

## Frontend — design constraints

**Panel-less.** The sky IS the page background. Big surfaces (`.post-single`, `.post-entry`, `.first-entry.home-info`, `.featured-card`, `.project-card`, `.stat-card`, mobile `.toc`) stay fully transparent — no background, border, or shadow (custom.css §27). List rhythm comes from hairline dashed dividers; hover shifts the divider to accent, never a shadow. Glass (`--glass-bg` + `backdrop-filter`) is reserved for tiny elements like tag chips. `.post-single` never gets `backdrop-filter`/`filter`/`transform` — it creates a containing block that breaks the fixed floating TOC inside it.

**Two themes, one design.** Any visual change ships for both `[data-theme="dark"]` and `[data-theme="light"]`, verified on both `/` and `/zh/`. Default theme is light; state lives in `data-theme` on `<html>` + localStorage `pref-theme`. Accent is purple (`--accent`); theme colors come from PaperMod's CSS vars (`--primary`, `--secondary`, `--entry`, `--border`, `--theme`) via `color-mix`, never hardcoded hex for themed surfaces.

**The sky is CSS-only** — no images, no WebGL (custom.css §26, markup in footer.html). Dark: 60s moon-phase cycle (crescent → full → blood-moon eclipse; the shadow disc `.moon::before` needs `z-index: 2` or the opaque moon disc hides the phases), ~36 JS-generated meteors, two twinkling star layers. Light: sun-ray cones with sway, 7 clouds, mist bands, and a 50/50 blue/white sky split by a wavy `clip-path` border. The Scorpius constellation (§30) stays hidden by default — only the Oct 25 birthday egg (gold) or the typed word `scorpio` reveals it. The starry-night canvas is the single sanctioned exception to CSS-only.

**Motion discipline.** Animate `transform` and `opacity` only. Every animation has a `prefers-reduced-motion` fallback and decorative markup is `aria-hidden`. Pointer effects (card tilt, avatar parallax) are gated behind `pointer: fine` so touch devices skip them.

**One JS file, no dependencies.** All site-wide JS lives in the numbered inline script in `layouts/partials/footer.html`; no frameworks, no npm. Toast text is bilingual via the `isZh` lang check — always keep both strings.

**Easter eggs** (footer.html JS §12–13, custom.css §32–33): Konami `↑↑↓↓←→←→BA`, moon/sun click, typed words `starry`/`scorpio`, logo ×5 disco, late-night toast, copy toast, ~4% dark-mode Van Gogh starry night, 404 lost meteor. Eggs respect `prefers-reduced-motion` and never interfere with normal reading.

**Resume exception.** `/resume/` is always light, no sky, no animations, print-ready A4 (`layouts/_default/resume.html` + §31). Panel-less and sky rules do not apply there.

## Definition of done

A change is complete when: `hugo --minify` builds with no errors, both `/` and `/zh/` render the change correctly in light AND dark themes (verify in a browser, screenshots preferred), and bilingual strings exist for any new UI text.
