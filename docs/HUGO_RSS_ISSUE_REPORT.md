# Incident Report: Hugo Build Failure (RSS Generation)

## Date
2026-03-10

## Issue Description
The GitHub Actions deployment pipeline failed during the `hugo --minify` build step.

### Error Log
```text
ERROR error building site: render: [en v1.0.0 guest] failed to render pages: render of "/" failed: "/home/runner/work/adlink8.github.io/adlink8.github.io/themes/PaperMod/layouts/_default/rss.xml:10:11": execute of template failed: template: rss.xml:10:11: executing "rss.xml" at <site>: can't evaluate field Author in type interface {}
```

## Root Cause
The `PaperMod` theme's RSS template (`layouts/_default/rss.xml`) attempts to access `site.Author`, a configuration field that was deprecated and removed in recent Hugo versions (v0.120.0+).

The build environment uses `hugo-version: latest` (resolved to v0.157.0), which no longer supports the legacy `Author` field in `hugo.toml`, causing the template execution to crash when generating the RSS feed.

## Resolution
Updated `hugo.toml` to use the modern `params.author` configuration structure, which is compatible with the current RSS template logic.

### Changes Made
Modified `hugo.toml`:

```toml
# Before
[params]
    env = "production"
    ShowCodeCopyButtons = true

# After
[params]
    env = "production"
    author = "Li Shuo Yan"  # Added this field
    ShowCodeCopyButtons = true
```

## Verification
1. The `rss.xml` template logic checks for `site.Params.author` first.
2. By defining `author` under `[params]`, the template successfully retrieves the author name and bypasses the code path that tries to access the non-existent `site.Author`.
