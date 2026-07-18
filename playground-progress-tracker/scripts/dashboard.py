#!/usr/bin/env python3
"""
Dashboard - playground-progress-tracker
Discovers all playground projects via glob, renders single/all-project
ASCII dashboards, gives a state-driven recommendation, and regenerates
the top-level programming-playground/README.md index.
Stdlib only - no third-party dependencies (no PyYAML).
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

PLAYGROUND_ROOT = Path.home() / "programming-playground"
IDLE_DAYS_THRESHOLD = 14


def log(msg):
    print(f"[*] {msg}")


def discover_projects(root):
    projects = []
    for progress_file in sorted(root.glob("*/*/progress.json")):
        try:
            data = json.loads(progress_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        projects.append((progress_file.parent, data))
    return projects


def find_project(root, tech_slug):
    tech, _, slug = tech_slug.partition("/")
    project_dir = root / tech / slug
    progress_path = project_dir / "progress.json"
    if not progress_path.exists():
        raise SystemExit(f"[!] Proyek '{tech_slug}' tidak ditemukan di {root}")
    return project_dir, json.loads(progress_path.read_text(encoding="utf-8"))


def milestone_counts(milestones):
    counts = {"completed": 0, "in_progress": 0, "needs_revisit": 0, "not_started": 0, "skipped": 0}
    for m in milestones:
        counts[m["status"]] = counts.get(m["status"], 0) + 1
    return counts


def progress_bar(done, total, width=10):
    if total == 0:
        return "[" + ("_" * width) + "] 0%"
    filled = round(done / total * width)
    pct = round(done / total * 100)
    return "[" + ("#" * filled) + ("_" * (width - filled)) + f"] {pct}%"


def format_minutes(total_minutes):
    hours, minutes = divmod(total_minutes, 60)
    return f"{hours} jam {minutes} menit"


def extract_why_now(roadmap_path, milestone_id):
    if not roadmap_path.exists():
        return ""
    text = roadmap_path.read_text(encoding="utf-8")
    block_match = re.search(
        rf"- id: {re.escape(milestone_id)}\n(?:.*\n)*?    why_now: >\n((?:\s{{6}}.*\n?)*)",
        text,
    )
    if not block_match:
        return ""
    lines = [line.strip() for line in block_match.group(1).splitlines() if line.strip()]
    return " ".join(lines)


def next_milestone(milestones):
    for m in milestones:
        if m["status"] in ("in_progress", "not_started"):
            done_ids = {x["id"] for x in milestones if x["status"] == "completed"}
            if m["status"] == "in_progress" or all(p in done_ids for p in m.get("prerequisites", [])):
                return m
    return None


def cmd_show(args, root):
    project_dir, data = find_project(root, args.project)
    proj = data["project"]
    milestones = data["milestones"]
    counts = milestone_counts(milestones)
    total = len(milestones)
    bar = progress_bar(counts["completed"], total)
    nxt = next_milestone(milestones)

    width = 62
    print("+" + "=" * width + "+")
    title_line = f"Dashboard Belajar: {proj['title']} ({proj['tech']})"
    print("|  " + title_line.ljust(width - 2) + "|")
    print("+" + "=" * width + "+")
    print("|" + " " * width + "|")
    print("|  " + f"Selesai       : {counts['completed']} milestone".ljust(width - 2) + "|")
    print("|  " + f"Sedang Jalan  : {counts['in_progress']} milestone".ljust(width - 2) + "|")
    print("|  " + f"Perlu Revisit : {counts['needs_revisit']} milestone".ljust(width - 2) + "|")
    print("|  " + f"Belum Mulai   : {counts['not_started']} milestone".ljust(width - 2) + "|")
    print("|" + " " * width + "|")
    print("|  " + f"Total Waktu   : {format_minutes(proj.get('total_time_minutes', 0))}".ljust(width - 2) + "|")
    print("|  " + f"Progress      : {bar}".ljust(width - 2) + "|")
    print("|" + " " * width + "|")
    print("+" + "-" * width + "+")
    if nxt:
        why_now = extract_why_now(project_dir / "roadmap.yaml", nxt["id"])
        print("|  " + f"Milestone Berikutnya: {nxt['id']} - {nxt['title']}".ljust(width - 2) + "|")
        if why_now:
            for line in wrap_text(why_now, width - 4):
                print("|  " + line.ljust(width - 2) + "|")
    else:
        print("|  " + "Semua milestone selesai!".ljust(width - 2) + "|")
    print("|" + " " * width + "|")
    print("|  " + f"Sesi Terakhir: {proj.get('last_session_at', '')[:10]}".ljust(width - 2) + "|")
    print("+" + "=" * width + "+")


def wrap_text(text, width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def cmd_list(args, root):
    projects = discover_projects(root)
    print("Programming Playground - Semua Proyek Belajar")
    print("=" * 64)
    print()
    if not projects:
        print("Belum ada proyek. Gunakan skill playground-project-architect untuk memulai.")
        regenerate_index(root, projects)
        return

    header = f"{'Tech':<10} {'Slug':<16} {'Judul':<22} {'Progress':<12} {'Sesi Terakhir':<14} Berikutnya"
    print(header)
    print("-" * len(header))

    total_done, total_milestones, total_minutes = 0, 0, 0
    for project_dir, data in projects:
        proj = data["project"]
        milestones = data["milestones"]
        counts = milestone_counts(milestones)
        total = len(milestones)
        nxt = next_milestone(milestones)
        next_label = f"{nxt['id']}: {nxt['title']}" if nxt else "Selesai semua"
        pct = round(counts["completed"] / total * 100) if total else 0
        progress_label = f"{counts['completed']}/{total} ({pct}%)"
        last_session = proj.get("last_session_at", "")[:10]
        print(f"{proj['tech']:<10} {proj['slug']:<16} {proj['title'][:22]:<22} "
              f"{progress_label:<12} {last_session:<14} {next_label}")
        total_done += counts["completed"]
        total_milestones += total
        total_minutes += proj.get("total_time_minutes", 0)

    print()
    overall_pct = round(total_done / total_milestones * 100) if total_milestones else 0
    print(f"Total: {len(projects)} proyek, {total_done}/{total_milestones} milestone "
          f"selesai ({overall_pct}%), {total_minutes} menit belajar")

    regenerate_index(root, projects)


def cmd_recommend(args, root):
    projects = discover_projects(root)
    if not projects:
        print("Belum ada proyek. Gunakan skill playground-project-architect untuk memulai.")
        return

    in_progress_candidates = []
    revisit_candidates = []
    idle_candidates = []
    now = datetime.now(timezone.utc).astimezone()

    for project_dir, data in projects:
        proj = data["project"]
        milestones = data["milestones"]
        for m in milestones:
            if m["status"] == "in_progress":
                in_progress_candidates.append((proj, m))
            elif m["status"] == "needs_revisit":
                revisit_candidates.append((proj, m))
        try:
            last_session = datetime.fromisoformat(proj.get("last_session_at", ""))
            idle_days = (now - last_session).days
        except ValueError:
            idle_days = None
        if idle_days is not None and idle_days > IDLE_DAYS_THRESHOLD:
            idle_candidates.append((proj, idle_days))

    if in_progress_candidates:
        proj, m = in_progress_candidates[0]
        print(f"Rekomendasi: lanjutkan milestone {m['id']} ({m['title']}) "
              f"di proyek {proj['tech']}/{proj['slug']}")
        print("  -> sesi ini masih in_progress dari sebelumnya.")
    elif revisit_candidates:
        proj, m = revisit_candidates[0]
        print(f"Rekomendasi: revisit milestone {m['id']} ({m['title']}) "
              f"di proyek {proj['tech']}/{proj['slug']}")
        print("  -> milestone ini ditandai perlu di-review ulang.")
    else:
        most_recent = max(projects, key=lambda p: p[1]["project"].get("last_session_at", ""))
        project_dir, data = most_recent
        proj = data["project"]
        nxt = next_milestone(data["milestones"])
        if nxt:
            why_now = extract_why_now(project_dir / "roadmap.yaml", nxt["id"])
            print(f"Rekomendasi: lanjutkan proyek {proj['tech']}/{proj['slug']} "
                  f"(aktivitas terbaru), milestone {nxt['id']}: {nxt['title']}")
            if why_now:
                print(f"  why_now: {why_now}")
        else:
            print(f"Proyek {proj['tech']}/{proj['slug']} sudah menyelesaikan semua milestone!")

    for proj, idle_days in idle_candidates:
        print(f"\nReminder: proyek {proj['tech']}/{proj['slug']} sudah {idle_days} hari tidak disentuh.")


def regenerate_index(root, projects=None):
    if projects is None:
        projects = discover_projects(root)
    lines = [
        "# Programming Playground — Learning Project Index",
        "_Auto-generated. Do not edit manually, it will be overwritten by playground-project-architect / playground-progress-tracker._",
        "",
    ]
    if not projects:
        lines.append("No projects yet. Use the `playground-project-architect` skill to get started.")
    else:
        lines.append("| Tech | Project | Title | Progress | Next Milestone | Last Session |")
        lines.append("|------|---------|-------|----------|-----------------|---------------|")
        for project_dir, data in projects:
            proj = data["project"]
            milestones = data["milestones"]
            counts = milestone_counts(milestones)
            total = len(milestones)
            pct = round(counts["completed"] / total * 100) if total else 0
            nxt = next_milestone(milestones)
            next_label = f"{nxt['id']}: {nxt['title']}" if nxt else "All milestones completed"
            last_session = proj.get("last_session_at", "")[:10]
            lines.append(f"| {proj['tech']} | {proj['slug']} | {proj['title']} | "
                         f"{counts['completed']}/{total} ({pct}%) | {next_label} | {last_session} |")
    (root / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_render_index(args, root):
    regenerate_index(root)
    log(f"Index ditulis ke {root / 'README.md'}")


def main():
    parser = argparse.ArgumentParser(description="Dashboard for programming-playground projects")
    parser.add_argument("--root", default=str(PLAYGROUND_ROOT), help="Path to programming-playground root")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="Show all-projects table")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Show single project dashboard")
    p_show.add_argument("project", help="tech/slug, e.g. go/url-shortener")
    p_show.set_defaults(func=cmd_show)

    p_recommend = sub.add_parser("recommend", help="Recommend what to resume next")
    p_recommend.set_defaults(func=cmd_recommend)

    p_index = sub.add_parser("render-index", help="Regenerate top-level README.md index only")
    p_index.set_defaults(func=cmd_render_index)

    args = parser.parse_args()
    root = Path(args.root).resolve()
    args.func(args, root)


if __name__ == "__main__":
    main()
