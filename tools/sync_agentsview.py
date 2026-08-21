#!/usr/bin/env python3
"""Regenerate data/ai_activity.json from the local AgentsView SQLite database.

Read-only against ~/.agentsview/sessions.db; writes one file in the repo.
Counting semantics (verified against the originally published numbers):
  - window: current calendar year to date, starting on the Monday on/before Jan 1
  - messages: all rows grouped by UTC date of timestamp (empty timestamps skipped)
  - sessions: deleted_at IS NULL grouped by UTC date of started_at (subagents included)
  - level thresholds: <50 -> 1, <300 -> 2, <1000 -> 3, else 4

Exit codes: 0 = data unchanged, 2 = data regenerated (content differs).
"""

import json
import sqlite3
import sys
from datetime import date, timedelta
from pathlib import Path
from statistics import median

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "data" / "ai_activity.json"
DEFAULT_DB = Path.home() / ".agentsview" / "sessions.db"


def open_db(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        sys.exit(f"AgentsView database not found: {db_path}")
    return sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)


def month_label(y: int, m: int, first_of_year: bool) -> tuple[str, str]:
    months_en = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    if first_of_year:
        return f"{y}年 {m}月", f"{months_en[m - 1]} '{y % 100:02d}"
    return f"{m}月", months_en[m - 1]


def level_for(messages: int) -> int:
    if messages <= 0:
        return 0
    if messages < 50:
        return 1
    if messages < 300:
        return 2
    if messages < 1000:
        return 3
    return 4


def compute_streaks(active: set[date], end: date) -> tuple[int, int]:
    """Longest run of consecutive active days; current run ending at end_date."""
    if not active:
        return 0, 0
    longest = cur = 0
    d = start = min(active)
    while d <= end:
        cur = cur + 1 if d in active else 0
        longest = max(longest, cur)
        d += timedelta(days=1)
    current = 0
    d = end
    if d not in active:  # grace: today may not have started yet
        d -= timedelta(days=1)
    while d in active:
        current += 1
        d -= timedelta(days=1)
    return longest, current


def main() -> None:
    db_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DB
    con = open_db(db_path)
    cur = con.cursor()

    end = date.today()
    # year-to-date grid: from the Monday on/before Jan 1 through the current week
    jan1 = date(end.year, 1, 1)
    start = jan1 - timedelta(days=jan1.weekday())

    start_s, end_s = start.isoformat(), end.isoformat()

    messages_by_day = dict(cur.execute(
        "SELECT substr(timestamp,1,10), COUNT(*) FROM messages "
        "WHERE timestamp != '' AND substr(timestamp,1,10) BETWEEN ? AND ? "
        "GROUP BY 1", (start_s, end_s)))
    sessions_by_day = dict(cur.execute(
        "SELECT substr(started_at,1,10), COUNT(*) FROM sessions "
        "WHERE deleted_at IS NULL AND started_at != '' "
        "AND substr(started_at,1,10) BETWEEN ? AND ? GROUP BY 1",
        (start_s, end_s)))

    weeks, months = [], []
    seen_months = set()
    total_days = 0
    for week_index in range((end - start).days // 7 + 1):
        days = []
        for day_i in range(7):
            d = start + timedelta(days=week_index * 7 + day_i)
            is_future = d > end
            msgs = 0 if is_future else messages_by_day.get(d.isoformat(), 0)
            sess = 0 if is_future else sessions_by_day.get(d.isoformat(), 0)
            days.append({
                "date": d.isoformat(), "year": d.year, "month": d.month,
                "day": d.day, "weekday": d.weekday(),
                "messages": msgs, "sessions": sess,
                "level": level_for(msgs), "is_future": is_future,
            })
            if d <= end:
                total_days += 1
                key = (d.year, d.month)
                if key not in seen_months:
                    seen_months.add(key)
                    # label current-year months only; the pre-Jan 1 stub column stays unlabeled
                    if d.year == end.year:
                        name_zh, name_en = month_label(d.year, d.month, d.month == 1)
                        months.append({"name_zh": name_zh, "name_en": name_en,
                                       "week_col": week_index})
        weeks.append({"week_index": week_index, "days": days})

    total_messages = sum(messages_by_day.values())
    total_sessions = sum(sessions_by_day.values())
    active_days = len(messages_by_day)

    session_rows = cur.execute(
        "SELECT message_count, health_grade, health_score, outcome FROM sessions "
        "WHERE deleted_at IS NULL AND started_at != '' "
        "AND substr(started_at,1,10) BETWEEN ? AND ?",
        (start_s, end_s)).fetchall()
    con.close()

    counts = [r[0] or 0 for r in session_rows]
    grades_counter = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    scores, completed = [], 0
    for _, grade, score, outcome in session_rows:
        if grade in grades_counter:
            grades_counter[grade] += 1
        if score is not None:
            scores.append(score)
        if outcome == "completed":
            completed += 1
    graded = sum(grades_counter.values())

    longest_streak, current_streak = compute_streaks(
        {date.fromisoformat(k) for k in messages_by_day}, end)
    health = {
        "avg_session_messages": round(total_messages / total_sessions, 1) if total_sessions else 0,
        "median_session_messages": int(round(median(counts))) if counts else 0,
        "completion_rate": round(completed * 100 / total_sessions) if total_sessions else 0,
        "healthy_ratio": round((grades_counter["A"] + grades_counter["B"]) * 100 / graded) if graded else 0,
        "avg_health_score": round(sum(scores) / len(scores)) if scores else 0,
        "longest_streak": longest_streak,
        "current_streak": current_streak,
        "grades": grades_counter,
    }

    data = {
        "summary": {
            "active_days": active_days,
            "total_messages": total_messages,
            "total_sessions": total_sessions,
            "start_date": start_s,
            "end_date": end_s,
            "max_daily_messages": max(messages_by_day.values(), default=0),
            "weeks_count": len(weeks),
            "window_days": total_days,
            "health": health,
        },
        "months": months,
        "weeks": weeks,
    }

    rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    old = OUT_PATH.read_text(encoding="utf-8") if OUT_PATH.exists() else ""
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(rendered, encoding="utf-8", newline="\n")

    if rendered == old:
        print(f"unchanged: {OUT_PATH}")
        return
    print(f"updated: {OUT_PATH}  "
          f"(messages={total_messages}, sessions={total_sessions}, "
          f"active_days={active_days}, peak={data['summary']['max_daily_messages']})")
    sys.exit(2)


if __name__ == "__main__":
    main()
