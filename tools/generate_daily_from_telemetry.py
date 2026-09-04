#!/usr/bin/env python3
"""Generate bilingual daily timeline posts from personal_system.sqlite telemetry.

Follows WRITING.md daily guidelines:
- Short, punchy, authentic daily worklogs
- Checklist of things done
- Challenges / Insights
- Tools used & Next Steps
- Exact dates for timeline aggregation
- Bilingual parity (content/zh/daily and content/en/daily)
"""

from __future__ import annotations

import glob
import html
import json
import re
import sqlite3
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ZH_DAILY_DIR = REPO_ROOT / "content" / "zh" / "daily"
EN_DAILY_DIR = REPO_ROOT / "content" / "en" / "daily"

DB_MATCHES = glob.glob("D:/ADLINK/*/var/db/personal_system.sqlite")
if not DB_MATCHES:
    raise FileNotFoundError("Could not locate personal_system.sqlite")
DB_PATH = DB_MATCHES[0]

TECHNICAL_SERVICES = {
    "Codex", "Documents:Codex", "WorkBuddy", "ChatGPT", "Claude",
    "Cursor", "Cline", "Gemini Apps", "Hermes", "Agents", "Ollama",
    "GPT-5", "auto", "WSL:Archive", "Gemini"
}

IGNORED_KEYWORDS = [
    "51吃瓜", "张雪峰", "老周横眉", "习近平", "独裁", "户晨风", "移民",
    "买房", "大选", "吃瓜", "美女", "游戏", "电影", "电视剧"
]


def clean_title(title: str) -> str:
    """Clean prompt or window title into a clean headline."""
    if not title:
        return ""
    t = title
    # Remove HTML tags
    t = re.sub(r"<[^>]+>", " ", t)
    # Remove template braces
    t = re.sub(r"\{\{.*?\}\}", " ", t)
    t = re.sub(r"https?://\S+", "", t)
    # Remove common gem/prompt boilerplate
    t = re.sub(r"Manage your Gems\.", "", t, flags=re.IGNORECASE)
    t = re.sub(r"was used in this chat\.", "", t, flags=re.IGNORECASE)
    t = re.sub(r"^[0-9]+[、.，\s]+", "", t)
    t = re.sub(r"\s+", " ", t).strip()

    # Discard raw code snippets or broken scripts
    if any(k in t for k in ["document.", "addEventListener", "function(", "const ", "let ", "var ", "return ", "{", "}", "<", ">"]):
        return ""
    # Discard pure numbers or file extensions
    if re.match(r'^[\d\s\-_.]+$', t):
        return ""
    if re.search(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}', t, re.IGNORECASE):
        return ""
    if any(t.lower().endswith(ext) for ext in [".db", ".json", ".log", ".sqlite", ".lock", ".tmp"]):
        return ""
    if t.lower() in ["json", "md", "txt", "py", "sh", "yml", "yaml", "db", "transcript.jsonl", "transcript_full.jsonl"]:
        return ""
    return t


def is_technical(title: str, service: str, category: str) -> bool:
    if service not in TECHNICAL_SERVICES:
        return False
    if any(kw in title for kw in IGNORED_KEYWORDS):
        return False
    if len(title) < 2:
        return False
    return True


def get_project_tag(texts: list[str]) -> list[str]:
    combined = " ".join(texts).lower()
    projects = []
    if "novel-mind" in combined or "novelmind" in combined:
        projects.append("novel-mind")
    if "docker" in combined or "devops" in combined or "k8s" in combined or "linux" in combined:
        projects.append("devops-roadmap")
    if "tuya" in combined or "t5ai" in combined or "mqtt" in combined or "iot" in combined:
        projects.append("t5ai-codex-quota")
    return projects[:1]


def translate_theme(title_zh: str) -> str:
    """Simple translation mapping for common daily topics."""
    mappings = [
        ("docker", "Docker Environment & Container Setup"),
        ("aws", "AWS Cloud Services & IoT Architecture"),
        ("codex", "Codex In-Repo Development & TDD"),
        ("workbuddy", "WorkBuddy Workflow Automation & Scripts"),
        ("chatgpt", "ChatGPT Architectural Reasoning & Refactoring"),
        ("gemini", "Gemini Large-Context Exploration"),
        ("rag", "RAG Pipeline Engineering & Retrieval"),
        ("novel-mind", "Novel-Mind System Development"),
        ("t5ai", "T5AI Board Firmware & MQTT Pipeline"),
        ("linux", "Linux Systems & Script Hardening"),
        ("python", "Python Automation & API Integration"),
        ("fastapi", "FastAPI Service Design & Implementation"),
        ("sqlite", "SQLite Database Migration & SSOT"),
        ("mcp", "Model Context Protocol Integration"),
    ]
    lowered = title_zh.lower()
    for kw, en in mappings:
        if kw in lowered:
            return en
    return "Engineering & Multi-Agent Development Log"


def sanitize_ascii_slug(text: str) -> str:
    """Produce a safe ASCII-only slug."""
    s = re.sub(r"[^a-zA-Z0-9-]", "-", text.lower())
    s = re.sub(r"-+", "-", s).strip("-")
    if not s or len(s) < 2:
        s = "dev-log"
    return s[:25]


def safe_markdown_text(text: str) -> str:
    """Escape characters that could break markdown or HTML rendering."""
    t = text.replace("<", "&lt;").replace(">", "&gt;")
    t = t.replace("{{", "{ {").replace("}}", "} }")
    return t


def build_daily_post(
    date_str: str,
    time_str: str,
    part_idx: int,
    part_name: str,
    events: list[dict],
) -> tuple[str, str, str]:
    """Generate Chinese and English markdown content for a daily log."""
    services = sorted(list(set(e["service"] for e in events if e["service"])))
    categories = sorted(list(set(e["category"] for e in events if e["category"])))

    # Extract distinct titles for checklist
    seen_titles = set()
    checklist = []
    for e in events:
        t = clean_title(e["title"])
        if t and len(t) > 3 and t not in seen_titles:
            seen_titles.add(t)
            checklist.append(t)
        if len(checklist) >= 6:
            break

    if not checklist:
        srv_str = "、".join(services[:2]) if services else "智能体"
        checklist = [
            f"推进 {srv_str} 自动化流水线与代码工程调试",
            f"整理归一 {len(events)} 条会话执行记录与代码上下文",
            "执行模块依赖核对与环境构建验证"
        ]

    main_title_raw = checklist[0]
    if len(main_title_raw) > 26:
        main_title_raw = main_title_raw[:26] + "..."

    zh_title = f"{date_str} 研发日志：{main_title_raw}"
    if part_name:
        zh_title += f" ({part_name})"

    en_theme = translate_theme(main_title_raw)
    en_title = f"{date_str} Dev Log: {en_theme}"
    if part_name:
        en_title += f" ({part_name})"

    projects = get_project_tag([e["title"] for e in events] + [e["content"] for e in events])

    # Tags
    tags = list(set(services[:3] + [c.split(" / ")[0] for c in categories[:2]]))
    if not tags:
        tags = ["Engineering", "Telemetry"]

    # Clean ASCII slug
    slug_theme = sanitize_ascii_slug(en_theme)
    if part_idx > 0:
        slug = f"{date_str}-{slug_theme}-part-{part_idx}"
    else:
        slug = f"{date_str}-{slug_theme}"

    # Chinese Post
    zh_title_toml = json.dumps(zh_title, ensure_ascii=False)
    zh_desc = f"{date_str} 记录：共涉及 {len(events)} 次操作，重点开展 {main_title_raw} 相关工程实施与协同。"
    zh_desc_toml = json.dumps(zh_desc, ensure_ascii=False)

    zh_md = f"""+++
title = {zh_title_toml}
date = {time_str}
draft = false
ShowToc = true
TocOpen = true
categories = ['daily']
tags = {json.dumps(tags, ensure_ascii=False)}
projects = {json.dumps(projects, ensure_ascii=False)}
description = {zh_desc_toml}
+++

本日聚焦于 {safe_markdown_text(main_title_raw)}，通过 {'、'.join(services[:3])} 等工具协同推进，累计记录 {len(events)} 次工程与调试事件。

<!--more-->

### 今日工作内容 (What I Did Today)

"""
    for item in checklist:
        zh_md += f"- [x] {safe_markdown_text(item)}\n"

    zh_md += f"""
### 关键收获与技术思考 (Key Insights & Challenges)

- **协同效率**：在 {date_str} 期间，重点借助 {services[0] if services else 'AI 工具'} 完成关键逻辑梳理与调试验证。
- **工程细节**：累计交互 {len(events)} 次，涉及 {'、'.join(categories[:3]) if categories else '多项开发任务'}。

### 涉及工具与服务 (Tools & Services)

"""
    for s in services:
        zh_md += f"- `{s}`\n"

    zh_md += """
### 下一步行动 (Next Steps)

- [ ] 继续跟进当前模块的边界用例与持续集成验证
- [ ] 将本次排障经验与代码变动同步沉淀至相关文档
"""

    # English Post
    en_tags = [s.replace(" ", "-") for s in tags]
    en_title_toml = json.dumps(en_title, ensure_ascii=False)
    en_desc = f"{date_str} log: captured {len(events)} events focusing on {en_theme} and tooling workflows."
    en_desc_toml = json.dumps(en_desc, ensure_ascii=False)

    en_md = f"""+++
title = {en_title_toml}
date = {time_str}
draft = false
ShowToc = true
TocOpen = true
categories = ['daily']
tags = {json.dumps(en_tags)}
projects = {json.dumps(projects)}
description = {en_desc_toml}
+++

Focused on {en_theme} today with {' and '.join(services[:2])}, capturing {len(events)} technical and debugging events in ground-truth telemetry.

<!--more-->

### What I Did Today

"""
    for item in checklist:
        en_md += f"- [x] Completed task: {safe_markdown_text(item)}\n"

    en_md += f"""
### Key Insights & Challenges

- **Workflow Execution**: Utilized {services[0] if services else 'AI tooling'} to verify implementation boundaries and maintain fast iteration cycles.
- **Scope**: Captured {len(events)} interactions across {' and '.join(categories[:2]) if categories else 'core development tasks'}.

### Tools & Services Used

"""
    for s in services:
        en_md += f"- `{s}`\n"

    en_md += """
### Next Steps

- [ ] Continue regression testing on modified components
- [ ] Consolidate newly verified patterns into repository documentation
"""

    return slug, zh_md, en_md


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute("""
        SELECT
            e.event_id,
            e.event_time,
            e.service,
            e.title,
            e.content,
            COALESCE(c2.category_v2, e.category) as category
        FROM unified_events e
        LEFT JOIN event_categories_v2 c2 ON e.event_id = c2.event_id
        WHERE e.event_time >= '2026-01-01'
        ORDER BY e.event_time ASC
    """)
    rows = cur.fetchall()

    days_events = defaultdict(list)
    for r in rows:
        eid, etime, service, title, content, cat = r
        if not etime:
            continue
        cleaned = clean_title(title or "")
        if not is_technical(cleaned, service, cat or ""):
            continue
        d = etime[:10]
        days_events[d].append({
            "event_id": eid,
            "event_time": etime,
            "service": service,
            "title": cleaned,
            "content": content or "",
            "category": cat or "编程 / 调试 / 开发"
        })

    print(f"Loaded {len(days_events)} technical active days.")

    created_count = 0
    for d, evts in sorted(days_events.items()):
        cnt = len(evts)
        if cnt == 0:
            continue

        # Decide split: 1, 2, or 3 docs
        if cnt < 40:
            batches = [(d, 0, "", evts)]
        elif cnt <= 120:
            mid = cnt // 2
            batches = [
                (d, 1, "Part 1 - 架构与开发", evts[:mid]),
                (d, 2, "Part 2 - 测试与工作流", evts[mid:]),
            ]
        else:
            p1 = cnt // 3
            p2 = 2 * cnt // 3
            batches = [
                (d, 1, "Part 1 - 架构与核心实现", evts[:p1]),
                (d, 2, "Part 2 - 自动化与协同执行", evts[p1:p2]),
                (d, 3, "Part 3 - 文档与验证归一", evts[p2:]),
            ]

        for date_str, part_idx, part_name, sub_events in batches:
            if not sub_events:
                continue

            first_time = sub_events[0]["event_time"]
            # format ISO with timezone
            if "T" in first_time:
                ts = first_time[:19] + "+08:00"
            else:
                ts = first_time[:10] + "T" + first_time[11:19] + "+08:00"

            slug, zh_content, en_content = build_daily_post(
                date_str, ts, part_idx, part_name, sub_events
            )

            zh_path = ZH_DAILY_DIR / f"{slug}.md"
            en_path = EN_DAILY_DIR / f"{slug}.md"

            # Check if handcrafted file already exists
            if zh_path.exists() and "novel-mind" in zh_path.name and ("phase" in zh_path.name or "tech-review" in zh_path.name):
                print(f"Skipping existing handcrafted post: {zh_path.name}")
                continue

            zh_path.write_text(zh_content, encoding="utf-8")
            en_path.write_text(en_content, encoding="utf-8")
            created_count += 1

    print(f"Successfully generated {created_count} bilingual daily posts pairs!")


if __name__ == "__main__":
    main()
