# `roadmap.yaml` Schema and JSON Input for `scaffold_project.py`

`roadmap.yaml` is a narrative document written directly by Claude (not through a script, not parsed back by any script — except `scaffold_project.py`, which receives its data as JSON and writes the YAML representation). Its content may be changed/added to manually by Claude at any time (e.g., when `playground-session-guide` finds scope creep and needs to add a new milestone).

## `roadmap.yaml` Structure

```yaml
project:
  tech: go
  slug: url-shortener
  title: "URL Shortener with Caching & Rate Limiting"
  created_at: "2026-07-18"

theme_rationale: |
  The URL shortener project was chosen because it will naturally face concurrency
  as traffic grows, a need for caching frequently-accessed redirects, and rate
  limiting to prevent abuse — real use cases for goroutines, channels, sync
  primitives, and Redis integration.

context7_libraries_consulted:
  - id: /golang/go
    note: "verify idiomatic net/http, context, and testing package for the current version"
  - id: /redis/go-redis
    note: "verify the idiomatic Redis client pattern for the caching milestone"

milestones:
  - id: m00
    title: "Project scaffolding & Hello World HTTP server"
    concepts: [go modules, net/http basics, project layout]
    prerequisites: []
    why_now: >
      Need a runnable starting point before adding any feature.
  - id: m01
    title: "In-memory URL store & short code generation"
    concepts: [maps, structs, basic hashing/encoding]
    prerequisites: [m00]
    why_now: >
      The project needs a way to store the short-code -> long URL mapping
      before it can do any redirecting at all.
  - id: m02
    title: "Concurrent-safe store with goroutines & mutex"
    concepts: [goroutines, sync.Mutex, race conditions]
    prerequisites: [m01]
    why_now: >
      The server receives many concurrent requests; a plain Go map isn't safe
      for concurrent access — a race condition will show up under load testing.
```

Required fields per milestone: `id` (format `m00`, `m01`, ...), `title` (English, becomes the commit label), `concepts` (list of strings, English/technical terms), `prerequisites` (list of other milestone ids), `why_now` (English, narrative, concrete).

## JSON Schema for `scaffold_project.py`

The script accepts the roadmap as JSON via `--roadmap-json` (a single valid JSON string), shaped like:

```json
{
  "title": "URL Shortener with Caching & Rate Limiting",
  "theme_rationale": "The URL shortener project was chosen because ...",
  "context7_libraries_consulted": [
    {"id": "/golang/go", "note": "verify idiomatic net/http, context, and testing package for the current version"},
    {"id": "/redis/go-redis", "note": "verify the idiomatic Redis client pattern for the caching milestone"}
  ],
  "milestones": [
    {
      "id": "m00",
      "title": "Project scaffolding & Hello World HTTP server",
      "concepts": ["go modules", "net/http basics", "project layout"],
      "prerequisites": [],
      "why_now": "Need a runnable starting point before adding any feature."
    },
    {
      "id": "m01",
      "title": "In-memory URL store & short code generation",
      "concepts": ["maps", "structs", "basic hashing/encoding"],
      "prerequisites": ["m00"],
      "why_now": "The project needs a way to store the short-code -> long URL mapping before it can do any redirecting at all."
    }
  ]
}
```

Important notes:
- Milestone `m00` MUST be present in this list and represent the skeleton already verified to run in SKILL.md Step 5 — `scaffold_project.py` automatically marks it `completed` in `progress.json` (with the `commit_sha` from the initial commit the script makes) since the skeleton was already proven to work before the scaffold ran.
- All milestones other than `m00` start with status `not_started`.
- `id`, `title`, `concepts`, `why_now`, and `theme_rationale` are all written in English (the `id`/`title`/`concepts` vocabulary is also reused in commit messages later).
- The order of milestones in the JSON determines their display order in `roadmap.yaml` and `progress.json` — keep them ordered basics → mastery.
