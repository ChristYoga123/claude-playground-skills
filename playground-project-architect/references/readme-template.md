# Template `README.md` per Proyek

Ditulis langsung oleh Claude (via `scaffold_project.py`) saat scaffold, boleh diperbarui manual oleh `playground-session-guide` seiring proyek berkembang (mis. update bagian "Cara Menjalankan" kalau ada dependency baru).

```markdown
# {Judul Proyek}

> Proyek belajar **{tech}** dibuat lewat `playground-project-architect`.
> Progress: lihat `progress.json` atau jalankan `playground-progress-tracker`.

## Tema

{theme_rationale, 2-4 kalimat}

## Cara Menjalankan

```bash
{perintah run/build spesifik teknologi, mis. `go run .` atau `cargo run`}
```

## Struktur Belajar

Roadmap lengkap ada di [`roadmap.yaml`](./roadmap.yaml). Progress dan status tiap milestone ada di [`progress.json`](./progress.json).

Untuk melanjutkan sesi belajar, gunakan skill `playground-session-guide`.

## Jejak Belajar (Git Log)

Setiap milestone yang selesai adalah satu commit tersendiri — jalankan `git log --oneline` di folder ini untuk melihat urutan konsep yang sudah dipelajari.
```

Placeholder `{tech}`, `{theme_rationale}`, dan perintah run diisi oleh `scaffold_project.py` berdasarkan argumen yang diterima dari SKILL.md Step 5.
