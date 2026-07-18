#!/usr/bin/env python3
"""
Update Progress - playground-session-guide
Atomic read-modify-write helper for a project's progress.json.
Stdlib only - no third-party dependencies.

Subcommands: start, complete, revisit, skip, append-milestone, resume-info
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

VALID_STATUSES = {"not_started", "in_progress", "completed", "needs_revisit", "skipped"}


def log(msg):
    print(f"[*] {msg}")


def success(msg):
    print(f"[+] {msg}")


def warn(msg):
    print(f"[!] {msg}")


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_progress(project_dir):
    path = project_dir / "progress.json"
    if not path.exists():
        raise SystemExit(f"[!] progress.json not found in {project_dir}")
    return path, json.loads(path.read_text(encoding="utf-8"))


def save_progress(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def find_milestone(data, milestone_id):
    for m in data["milestones"]:
        if m["id"] == milestone_id:
            return m
    raise SystemExit(f"[!] Milestone '{milestone_id}' not found in progress.json")


def touch_session(data):
    data["project"]["last_session_at"] = now_iso()
    data["project"]["total_sessions"] = data["project"].get("total_sessions", 0) + 1


def cmd_start(args, project_dir):
    path, data = load_progress(project_dir)
    m = find_milestone(data, args.milestone)
    if m["status"] not in ("not_started", "in_progress", "needs_revisit", "skipped"):
        warn(f"Milestone {args.milestone} has status '{m['status']}', proceeding anyway.")
    m["status"] = "in_progress"
    if args.mode:
        m["mode"] = args.mode
    if not m.get("started_at"):
        m["started_at"] = now_iso()
    if args.notes:
        m["notes"] = args.notes
    touch_session(data)
    save_progress(path, data)
    success(f"Milestone {args.milestone} -> in_progress")


def cmd_complete(args, project_dir):
    path, data = load_progress(project_dir)
    m = find_milestone(data, args.milestone)
    m["status"] = "completed"
    m["completed_at"] = now_iso()
    if not m.get("started_at"):
        m["started_at"] = m["completed_at"]
    if args.mode:
        m["mode"] = args.mode
    if args.commit:
        m["commit_sha"] = args.commit
    if args.duration is not None:
        m["duration_minutes"] = args.duration
        data["project"]["total_time_minutes"] = data["project"].get("total_time_minutes", 0) + args.duration
    if args.notes:
        m["notes"] = args.notes
    touch_session(data)
    save_progress(path, data)
    success(f"Milestone {args.milestone} -> completed (commit {args.commit or 'n/a'})")


def cmd_revisit(args, project_dir):
    path, data = load_progress(project_dir)
    m = find_milestone(data, args.milestone)
    m["status"] = "needs_revisit"
    if args.notes:
        m["notes"] = args.notes
    touch_session(data)
    save_progress(path, data)
    success(f"Milestone {args.milestone} -> needs_revisit")


def cmd_skip(args, project_dir):
    path, data = load_progress(project_dir)
    m = find_milestone(data, args.milestone)
    if m["status"] != "not_started":
        warn(f"Milestone {args.milestone} has status '{m['status']}', skip is usually used for not_started.")
    m["status"] = "skipped"
    if args.notes:
        m["notes"] = args.notes
    save_progress(path, data)
    success(f"Milestone {args.milestone} -> skipped")


def cmd_append_milestone(args, project_dir):
    path, data = load_progress(project_dir)
    if any(m["id"] == args.id for m in data["milestones"]):
        raise SystemExit(f"[!] Milestone id '{args.id}' already exists.")
    new_milestone = {
        "id": args.id,
        "title": args.title,
        "concepts": [c.strip() for c in args.concepts.split(",") if c.strip()],
        "prerequisites": [p.strip() for p in args.prerequisites.split(",") if p.strip()] if args.prerequisites else [],
        "status": "not_started",
        "mode": None,
        "started_at": None,
        "completed_at": None,
        "duration_minutes": None,
        "commit_sha": None,
        "notes": args.notes or "",
    }
    if args.after:
        idx = next((i for i, m in enumerate(data["milestones"]) if m["id"] == args.after), None)
        if idx is None:
            raise SystemExit(f"[!] Milestone '{args.after}' (for --after) not found.")
        data["milestones"].insert(idx + 1, new_milestone)
    else:
        data["milestones"].append(new_milestone)
    save_progress(path, data)
    success(f"Milestone {args.id} added to progress.json. Remember to update roadmap.yaml manually too.")


def cmd_resume_info(args, project_dir):
    _, data = load_progress(project_dir)
    milestones = data["milestones"]

    in_progress = [m for m in milestones if m["status"] == "in_progress"]
    needs_revisit = [m for m in milestones if m["status"] == "needs_revisit"]

    def prereqs_done(m):
        done_ids = {x["id"] for x in milestones if x["status"] == "completed"}
        return all(p in done_ids for p in m.get("prerequisites", []))

    not_started_ready = [m for m in milestones if m["status"] == "not_started" and prereqs_done(m)]

    result = {
        "project": data["project"],
        "in_progress": in_progress,
        "needs_revisit": needs_revisit,
        "next_ready": not_started_ready[0] if not_started_ready else None,
        "counts": {
            "completed": sum(1 for m in milestones if m["status"] == "completed"),
            "in_progress": len(in_progress),
            "needs_revisit": len(needs_revisit),
            "not_started": sum(1 for m in milestones if m["status"] == "not_started"),
            "skipped": sum(1 for m in milestones if m["status"] == "skipped"),
            "total": len(milestones),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Update a playground project's progress.json")
    parser.add_argument("--project", required=True, help="Absolute path to the project directory")
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start", help="Mark a milestone as in_progress")
    p_start.add_argument("--milestone", required=True)
    p_start.add_argument("--mode", choices=["pair", "hint"])
    p_start.add_argument("--notes")
    p_start.set_defaults(func=cmd_start)

    p_complete = sub.add_parser("complete", help="Mark a milestone as completed")
    p_complete.add_argument("--milestone", required=True)
    p_complete.add_argument("--commit", help="Short git commit sha")
    p_complete.add_argument("--duration", type=int, help="Minutes spent")
    p_complete.add_argument("--mode", choices=["pair", "hint"])
    p_complete.add_argument("--notes")
    p_complete.set_defaults(func=cmd_complete)

    p_revisit = sub.add_parser("revisit", help="Mark a milestone as needs_revisit")
    p_revisit.add_argument("--milestone", required=True)
    p_revisit.add_argument("--notes")
    p_revisit.set_defaults(func=cmd_revisit)

    p_skip = sub.add_parser("skip", help="Mark a not_started milestone as skipped")
    p_skip.add_argument("--milestone", required=True)
    p_skip.add_argument("--notes")
    p_skip.set_defaults(func=cmd_skip)

    p_append = sub.add_parser("append-milestone", help="Append a new milestone discovered mid-session")
    p_append.add_argument("--id", required=True)
    p_append.add_argument("--title", required=True)
    p_append.add_argument("--concepts", required=True, help="Comma-separated list")
    p_append.add_argument("--prerequisites", help="Comma-separated milestone ids")
    p_append.add_argument("--after", help="Insert after this milestone id (default: append at end)")
    p_append.add_argument("--notes")
    p_append.set_defaults(func=cmd_append_milestone)

    p_resume = sub.add_parser("resume-info", help="Print resume info as JSON (read-only)")
    p_resume.set_defaults(func=cmd_resume_info)

    args = parser.parse_args()
    project_dir = Path(args.project).resolve()
    if not project_dir.is_dir():
        raise SystemExit(f"[!] Project dir not found: {project_dir}")

    args.func(args, project_dir)


if __name__ == "__main__":
    main()
