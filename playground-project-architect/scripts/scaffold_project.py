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


def write_roadmap_yaml(path, tech, slug, title, roadmap, created_at, skeleton_mode):
    lines = []
    lines.append("project:")
    lines.append(f"  tech: {tech}")
    lines.append(f"  slug: {slug}")
    lines.append(f"  title: {yaml_str(title)}")
    lines.append(f"  skeleton_mode: {skeleton_mode}")
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


def build_progress(tech, slug, title, project_rel_path, roadmap, now_iso, skeleton_mode):
    milestones = []
    for i, m in enumerate(roadmap["milestones"]):
        is_m00_done = i == 0 and skeleton_mode == "ai"
        if i == 0 and skeleton_mode == "scratch":
            notes = "Skeleton not built yet - will be built from scratch as the first playground-session-guide session (hint/pair mode)."
        elif is_m00_done:
            notes = "Initial skeleton, verified to run before scaffolding."
        else:
            notes = ""
        milestones.append({
            "id": m["id"],
            "title": m["title"],
            "concepts": m["concepts"],
            "prerequisites": m.get("prerequisites", []),
            "status": "completed" if is_m00_done else "not_started",
            "mode": "pair" if is_m00_done else None,
            "started_at": now_iso if is_m00_done else None,
            "completed_at": now_iso if is_m00_done else None,
            "duration_minutes": None,
            "commit_sha": None,
            "notes": notes,
        })
    return {
        "project": {
            "tech": tech,
            "slug": slug,
            "title": title,
            "path": project_rel_path,
            "skeleton_mode": skeleton_mode,
            "created_at": now_iso,
            "last_session_at": now_iso,
            "total_sessions": 1,
            "total_time_minutes": 0,
        },
        "milestones": milestones,
    }


def write_progress_json(path, progress):
    path.write_text(json.dumps(progress, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_readme(path, title, tech, theme_rationale, run_command, skeleton_mode):
    if skeleton_mode == "scratch":
        running_section = """## Running It

Not runnable yet - the m00 skeleton hasn't been built. It will be built from scratch
in the first `playground-session-guide` session (hint/pair mode), just like every
other milestone.
"""
    else:
        running_section = f"""## Running It

```bash
{run_command}
```
"""
    content = f"""# {title}

> A **{tech}** learning project created via `playground-project-architect`.
> Progress: see `progress.json` or run the `playground-progress-tracker` skill.

## Theme

{theme_rationale.strip()}

{running_section}
## Learning Structure

The full roadmap is in [`roadmap.yaml`](./roadmap.yaml). Progress and status for each milestone
is in [`progress.json`](./progress.json).

To continue a learning session, use the `playground-session-guide` skill.

## Learning Trail (Git Log)

Each completed milestone is its own commit — run `git log --oneline`
in this folder to see the sequence of concepts learned.
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
        next_label = f"{next_m['id']}: {next_m['title']}" if next_m else "All milestones completed"
        last_session = proj.get("last_session_at", "")[:10]
        rows.append((proj["tech"], proj["slug"], proj["title"], f"{done}/{total} ({pct}%)", next_label, last_session))

    lines = [
        "# Programming Playground — Learning Project Index",
        "_Auto-generated. Do not edit manually, it will be overwritten by playground-project-architect / playground-progress-tracker._",
        "",
    ]
    if not rows:
        lines.append("No projects yet. Use the `playground-project-architect` skill to get started.")
    else:
        lines.append("| Tech | Project | Title | Progress | Next Milestone | Last Session |")
        lines.append("|------|---------|-------|----------|-----------------|---------------|")
        for tech, slug, title, progress, next_label, last_session in rows:
            lines.append(f"| {tech} | {slug} | {title} | {progress} | {next_label} | {last_session} |")

    (playground_root / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new playground learning project")
    parser.add_argument("--project-dir", required=True, help="Absolute path to the project directory")
    parser.add_argument("--tech", required=True, help="Tech slug, e.g. go, postgresql, kafka")
    parser.add_argument("--slug", required=True, help="Project slug, e.g. url-shortener")
    parser.add_argument("--title", required=True, help="Project title")
    parser.add_argument("--skeleton-mode", choices=["ai", "scratch"], default="scratch",
                         help="'ai' = m00 already built and verified to run by Claude before this script runs. "
                              "'scratch' (default) = no m00 code was written; m00 stays not_started and will be "
                              "built from scratch as the project's first playground-session-guide session.")
    parser.add_argument("--run-command", default=None,
                         help="Command to run the m00 skeleton, e.g. 'go run .' (required when --skeleton-mode ai)")
    parser.add_argument("--roadmap-json", required=True, help="JSON string with theme_rationale, context7_libraries_consulted, milestones")
    args = parser.parse_args()

    if args.skeleton_mode == "ai" and not args.run_command:
        raise SystemExit("[!] --run-command is required when --skeleton-mode ai")

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

    log(f"Writing roadmap.yaml at {project_dir}")
    write_roadmap_yaml(project_dir / "roadmap.yaml", args.tech, args.slug, args.title, roadmap, created_at, args.skeleton_mode)

    log("Writing progress.json")
    progress = build_progress(args.tech, args.slug, args.title, project_rel_path, roadmap, now_iso, args.skeleton_mode)
    write_progress_json(project_dir / "progress.json", progress)

    log("Writing README.md")
    write_readme(project_dir / "README.md", args.title, args.tech, roadmap["theme_rationale"], args.run_command, args.skeleton_mode)

    log("git init & initial commit")
    if not (project_dir / ".git").exists():
        run_git(["init"], project_dir)
    run_git(["add", "-A"], project_dir)

    m00 = roadmap["milestones"][0]
    if args.skeleton_mode == "ai":
        commit_subject = f"{m00['id']}: {m00['title']}"
        commit_body = f"Initial project skeleton, verified to run.\n\nMilestone-Id: {m00['id']}"
    else:
        commit_subject = "chore: scaffold learning project metadata"
        commit_body = (
            "roadmap.yaml, progress.json, README.md for a new playground project.\n"
            "No m00 code yet - it will be built from scratch in the first "
            "playground-session-guide session."
        )
    run_git(["commit", "-m", commit_subject, "-m", commit_body], project_dir)
    commit_sha = run_git(["rev-parse", "--short", "HEAD"], project_dir)

    if args.skeleton_mode == "ai":
        log(f"Updating commit_sha m00 -> {commit_sha}")
        progress["milestones"][0]["commit_sha"] = commit_sha
        write_progress_json(project_dir / "progress.json", progress)
        run_git(["add", "progress.json"], project_dir)
        run_git(["commit", "--amend", "--no-edit"], project_dir)

    log("Regenerating programming-playground/README.md index")
    regenerate_index(playground_root)

    success(f"Project '{args.title}' is ready at {project_dir}")


if __name__ == "__main__":
    main()
