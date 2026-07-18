# Skema `roadmap.yaml` dan JSON Input untuk `scaffold_project.py`

`roadmap.yaml` adalah dokumen naratif yang ditulis langsung oleh Claude (bukan lewat script, bukan di-parse balik oleh script manapun — kecuali `scaffold_project.py` yang menerima datanya sebagai JSON lalu menulis representasi YAML-nya). Isinya boleh berubah/ditambah manual oleh Claude kapan saja (mis. saat `playground-session-guide` menemukan scope creep dan perlu menambah milestone baru).

## Struktur `roadmap.yaml`

```yaml
project:
  tech: go
  slug: url-shortener
  title: "URL Shortener with Caching & Rate Limiting"
  created_at: "2026-07-18"

theme_rationale: |
  Proyek URL shortener dipilih karena secara alami akan menghadapi concurrency
  saat traffic naik, kebutuhan caching untuk redirect yang sering diakses, dan
  rate limiting untuk mencegah abuse — use-case nyata untuk goroutines, channels,
  sync primitives, dan integrasi Redis.

context7_libraries_consulted:
  - id: /golang/go
    note: "verifikasi idiomatic net/http, context, testing package versi saat ini"
  - id: /redis/go-redis
    note: "verifikasi pola client Redis idiomatic untuk milestone caching"

milestones:
  - id: m00
    title: "Project scaffolding & Hello World HTTP server"
    concepts: [go modules, net/http basics, project layout]
    prerequisites: []
    why_now: >
      Butuh titik awal yang bisa dijalankan sebelum menambah fitur apa pun.
  - id: m01
    title: "In-memory URL store & short code generation"
    concepts: [maps, structs, basic hashing/encoding]
    prerequisites: [m00]
    why_now: >
      Proyek butuh cara menyimpan mapping short-code -> long URL sebelum bisa
      melakukan redirect apa pun.
  - id: m02
    title: "Concurrent-safe store with goroutines & mutex"
    concepts: [goroutines, sync.Mutex, race conditions]
    prerequisites: [m01]
    why_now: >
      Server menerima banyak request bersamaan; map biasa di Go tidak aman
      diakses concurrent — akan terlihat race condition saat di-load test.
```

Field wajib per milestone: `id` (format `m00`, `m01`, ...), `title` (Bahasa Inggris, jadi label commit), `concepts` (list string, Bahasa Inggris/istilah teknis), `prerequisites` (list id milestone lain), `why_now` (Bahasa Indonesia, naratif, konkret).

## Skema JSON untuk `scaffold_project.py`

Script menerima roadmap sebagai JSON via `--roadmap-json` (satu baris/string JSON valid), dengan bentuk:

```json
{
  "title": "URL Shortener with Caching & Rate Limiting",
  "theme_rationale": "Proyek URL shortener dipilih karena ...",
  "context7_libraries_consulted": [
    {"id": "/golang/go", "note": "verifikasi idiomatic net/http, context, testing package versi saat ini"},
    {"id": "/redis/go-redis", "note": "verifikasi pola client Redis idiomatic untuk milestone caching"}
  ],
  "milestones": [
    {
      "id": "m00",
      "title": "Project scaffolding & Hello World HTTP server",
      "concepts": ["go modules", "net/http basics", "project layout"],
      "prerequisites": [],
      "why_now": "Butuh titik awal yang bisa dijalankan sebelum menambah fitur apa pun."
    },
    {
      "id": "m01",
      "title": "In-memory URL store & short code generation",
      "concepts": ["maps", "structs", "basic hashing/encoding"],
      "prerequisites": ["m00"],
      "why_now": "Proyek butuh cara menyimpan mapping short-code -> long URL sebelum bisa melakukan redirect apa pun."
    }
  ]
}
```

Catatan penting:
- Milestone `m00` HARUS ada di list ini dan mewakili skeleton yang sudah diverifikasi jalan pada Step 5 SKILL.md — `scaffold_project.py` otomatis menandainya `completed` di `progress.json` (dengan `commit_sha` dari commit awal yang dibuat script) karena skeleton sudah terbukti berfungsi sebelum scaffold dijalankan.
- Semua milestone selain `m00` mulai dengan status `not_started`.
- `id`, `title`, `concepts` dalam Bahasa Inggris (dipakai juga sebagai kosakata commit message nanti). `why_now` dan `theme_rationale` dalam Bahasa Indonesia.
- Urutan milestone di JSON menentukan urutan tampil di `roadmap.yaml` dan `progress.json` — usahakan sudah terurut dasar → mahir.
