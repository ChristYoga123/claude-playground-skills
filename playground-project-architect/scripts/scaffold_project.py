#!/usr/bin/env python3
"""
Scaffold Project - playground-project-architect
Writes roadmap.yaml, progress.json, README.md for a new playground project,
git-inits the project directory, commits the initial skeleton (m00), and
refreshes the top-level programming-playground/README.md index.

Assumes the project directory already contains a working m00 skeleton
(created and verified by Claude in SKILL.md Step 5 before this script runs).
Stdlib only - no third-party dependencies (no PyYAML, no requests).
"""

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def log(msg):
    print(f"[*] {msg}")


def success(msg):
    print(f"[+] {msg}")


def warn(msg):
    print(f"[!] {msg}")


def run_git(args, cwd):
    result = subprocess.run(
        ["git"] + args, cwd=cwd, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def yaml_block(text, indent):
    pad = " " * indent
    lines = text.strip("\n").split("\n")
    return "\n".join(f"{pad}{line}" for line in lines) if lines else pad


def yaml_str(value):
    escaped = value.replace('"', '\\"')
    return f'"{escaped}"'


def write_roadmap_yaml(path, tech, slug, title, roadmap, created_at):
    lines = []
    lines.append("project:")
    lines.append(f"  tech: {tech}")
    lines.append(f"  slug: {slug}")
    lines.append(f"  title: {yaml_str(title)}")
    lines.append(f"  created_at: {yaml_str(created_at)}")
    lines.append("")
    lines.append("theme_rationale: |")
    lines.append(yaml_block(roadmap["theme_rationale"], 2))
    lines.append("")

    libs = roadmap.get("context7_libraries_consulted", [])
    if libs:
        lines.append("context7_libraries_consulted:")
        for lib in libs:
            lines.append(f"  - id: {lib['id']}")
            lines.append(f"    note: {yaml_str(lib['note'])}")
    else:
        lines.append("context7_libraries_consulted: []")
    lines.append("")

    lines.append("milestones:")
    for m in roadmap["milestones"]:
        lines.append(f"  - id: {m['id']}")
        lines.append(f"    title: {yaml_str(m['title'])}")
        concepts = ", ".join(yaml_str(c) for c in m["concepts"])
        lines.append(f"    concepts: [{concepts}]")
        prereqs = ", ".join(m.get("prerequisites", []))
        lines.append(f"    prerequisites: [{prereqs}]")
        lines.append("    why_now: >")
        lines.append(yaml_block(m["why_now"], 6))

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_progress(tech, slug, title, project_rel_path, roadmap, now_iso):
    milestones = []
    for i, m in enumerate(roadmap["milestones"]):
        is_m00 = i == 0
        milestones.append({
            "id": m["id"],
            "title": m["title"],
            "concepts": m["concepts"],
            "prerequisites": m.get("prerequisites", []),
            "status": "completed" if is_m00 else "not_started",
            "mode": "pair" if is_m00 else None,
            "started_at": now_iso if is_m00 else None,
            "completed_at": now_iso if is_m00 else None,
            "duration_minutes": None,
            "commit_sha": None,
            "notes": "Skeleton awal, diverifikasi jalan sebelum scaffold." if is_m00 else "",
        })
    return {
        "project": {
            "tech": tech,
            "slug": slug,
            "title": title,
            "path": project_rel_path,
            "created_at": now_iso,
            "last_session_at": now_iso,
            "total_sessions": 1,
            "total_time_minutes": 0,
        },
        "milestones": milestones,
    }


def write_progress_json(path, progress):
    path.write_text(json.dumps(progress, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_readme(path, title, tech, theme_rationale, run_command):
    content = f"""# {title}

> Proyek belajar **{tech}** dibuat lewat `playground-project-architect`.
> Progress: lihat `progress.json` atau jalankan skill `playground-progress-tracker`.

## Tema

{theme_rationale.strip()}

## Cara Menjalankan

```bash
{run_command}
```

## Struktur Belajar

Roadmap lengkap ada di [`roadmap.yaml`](./roadmap.yaml). Progress dan status tiap milestone
ada di [`progress.json`](./progress.json).

Untuk melanjutkan sesi belajar, gunakan skill `playground-session-guide`.

## Jejak Belajar (Git Log)

Setiap milestone yang selesai adalah satu commit tersendiri — jalankan `git log --oneline`
di folder ini untuk melihat urutan konsep yang sudah dipelajari.
"""
    path.write_text(content, encoding="utf-8")


def regenerate_index(playground_root):
    rows = []
    for progress_file in sorted(playground_root.glob("*/*/progress.json")):
        try:
            data = json.loads(progress_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        proj = data["project"]
        milestones = data["milestones"]
        done = sum(1 for m in milestones if m["status"] == "completed")
        total = len(milestones)
        pct = round(done / total * 100) if total else 0
        next_m = next((m for m in milestones if m["status"] in ("not_started", "in_progress")), None)
        next_label = f"{next_m['id']}: {next_m['title']}" if next_m else "Selesai semua milestone"
        last_session = proj.get("last_session_at", "")[:10]
        rows.append((proj["tech"], proj["slug"], proj["title"], f"{done}/{total} ({pct}%)", next_label, last_session))

    lines = [
        "# Programming Playground — Index Proyek Belajar",
        "_Auto-generated. Jangan edit manual, akan ditimpa oleh playground-project-architect / playground-progress-tracker._",
        "",
    ]
    if not rows:
        lines.append("Belum ada proyek. Gunakan skill `playground-project-architect` untuk memulai.")
    else:
        lines.append("| Tech | Proyek | Judul | Progress | Milestone Berikutnya | Sesi Terakhir |")
        lines.append("|------|--------|-------|----------|-----------------------|----------------|")
        for tech, slug, title, progress, next_label, last_session in rows:
            lines.append(f"| {tech} | {slug} | {title} | {progress} | {next_label} | {last_session} |")

    (playground_root / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new playground learning project")
    parser.add_argument("--project-dir", required=True, help="Absolute path to the project directory (already has m00 skeleton)")
    parser.add_argument("--tech", required=True, help="Tech slug, e.g. go, postgresql, kafka")
    parser.add_argument("--slug", required=True, help="Project slug, e.g. url-shortener")
    parser.add_argument("--title", required=True, help="Project title")
    parser.add_argument("--run-command", required=True, help="Command to run the m00 skeleton, e.g. 'go run .'")
    parser.add_argument("--roadmap-json", required=True, help="JSON string with theme_rationale, context7_libraries_consulted, milestones")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    if not project_dir.is_dir():
        raise SystemExit(f"[!] Project dir does not exist: {project_dir}")

    roadmap = json.loads(args.roadmap_json)
    if not roadmap.get("milestones"):
        raise SystemExit("[!] roadmap-json must contain at least milestone m00")

    now = datetime.now(timezone.utc).astimezone()
    now_iso = now.isoformat(timespec="seconds")
    created_at = now.strftime("%Y-%m-%d")

    playground_root = project_dir.parent.parent
    project_rel_path = f"{args.tech}/{args.slug}"

    log(f"Menulis roadmap.yaml di {project_dir}")
    write_roadmap_yaml(project_dir / "roadmap.yaml", args.tech, args.slug, args.title, roadmap, created_at)

    log("Menulis progress.json")
    progress = build_progress(args.tech, args.slug, args.title, project_rel_path, roadmap, now_iso)
    write_progress_json(project_dir / "progress.json", progress)

    log("Menulis README.md")
    write_readme(project_dir / "README.md", args.title, args.tech, roadmap["theme_rationale"], args.run_command)

    log("git init & commit awal")
    if not (project_dir / ".git").exists():
        run_git(["init"], project_dir)
    run_git(["add", "-A"], project_dir)

    m00 = roadmap["milestones"][0]
    commit_subject = f"{m00['id']}: {m00['title']}"
    commit_body = (
        "Skeleton awal proyek, diverifikasi bisa dijalankan.\n\n"
        f"Milestone-Id: {m00['id']}"
    )
    run_git(["commit", "-m", commit_subject, "-m", commit_body], project_dir)
    commit_sha = run_git(["rev-parse", "--short", "HEAD"], project_dir)

    log(f"Update commit_sha m00 -> {commit_sha}")
    progress["milestones"][0]["commit_sha"] = commit_sha
    write_progress_json(project_dir / "progress.json", progress)
    run_git(["add", "progress.json"], project_dir)
    run_git(["commit", "--amend", "--no-edit"], project_dir)

    log("Regenerasi index programming-playground/README.md")
    regenerate_index(playground_root)

    success(f"Proyek '{args.title}' siap di {project_dir}")


if __name__ == "__main__":
    main()
