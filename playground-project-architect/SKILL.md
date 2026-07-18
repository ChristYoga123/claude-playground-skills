---
name: playground-project-architect
description: Merancang proyek belajar baru untuk teknologi apa pun (bahasa pemrograman, database, message broker, dsb) dengan memilih tema proyek yang cukup kompleks, menyusun roadmap milestone terurut dari dasar sampai mahir yang berakar pada konsep nyata teknologi tersebut (diverifikasi via Context7), lalu men-scaffold skeleton proyek yang bisa langsung dijalankan (git init, README, roadmap.yaml, progress.json) di dalam programming-playground/<tech>/<project-slug>/. Gunakan skill ini saat user bilang "aku mau belajar <teknologi>", "mulai proyek belajar <teknologi>", "bikin playground project untuk <teknologi>", atau minta dirancangkan kurikulum/roadmap untuk teknologi baru yang belum ada proyeknya.
metadata:
  version: 1.0.0
---

# Playground Project Architect

Skill ini merancang proyek belajar baru untuk teknologi apa pun (bahasa pemrograman, database, message broker, tool infra, dsb), dengan filosofi **project-based playground**: bukan tutorial dengan contoh kode terpisah-pisah, tapi SATU proyek nyata yang tumbuh dari skeleton kecil menjadi kompleks seiring konsep-konsep dipelajari. Setiap konsep nanti diimplementasikan langsung ke dalam proyek ini oleh skill pasangannya, `playground-session-guide`.

Skill ini HANYA menangani desain awal (tema + roadmap + scaffold). Untuk menjalankan sesi belajar di proyek yang sudah ada, gunakan `playground-session-guide`. Untuk melihat progress semua proyek, gunakan `playground-progress-tracker`.

## Workspace

Semua proyek belajar disimpan di direktori workspace `programming-playground/`. Default-nya `~/programming-playground/` (home directory user). Sebelum memakai default ini:
1. Cek apakah user sudah punya folder `programming-playground/` di tempat lain (mis. di dalam direktori project yang sedang dibuka saat ini) — kalau ada, pakai itu.
2. Kalau user pernah menyebutkan lokasi custom sebelumnya, pakai itu secara konsisten.
3. Kalau tidak ada indikasi apa pun, pakai `~/programming-playground/` dan beri tahu user lokasinya.

Selanjutnya di skill ini, `<PLAYGROUND_ROOT>` merujuk ke direktori ini.

## Kapan Menggunakan Skill Ini

- User bilang "aku mau belajar Go/Rust/PostgreSQL/Kafka/dst"
- User minta "bikin playground project untuk X"
- User minta dirancangkan roadmap/kurikulum belajar teknologi baru
- **Bukan** untuk melanjutkan proyek yang sudah ada (itu tugas `playground-session-guide`) — selalu cek dulu di Step 1

## Instructions

### Step 1: Klarifikasi Scope & Cek Proyek Existing

Sebelum merancang apa pun:

1. Cek apakah sudah ada proyek untuk teknologi ini: `ls <PLAYGROUND_ROOT>/<tech-slug>/` (glob juga `*/progress.json` untuk melihat semua proyek yang ada).
2. **Jika sudah ada proyek untuk tech ini** — jangan scaffold ulang. Beri tahu user proyeknya sudah ada, tawarkan untuk lanjut dengan `playground-session-guide`, atau (kalau user memang eksplisit minta proyek KEDUA untuk tech yang sama, mis. mau eksperimen dengan tema berbeda) lanjutkan dengan slug proyek yang berbeda.
3. Kumpulkan info berikut (pakai `AskUserQuestion` kalau belum jelas dari permintaan user):
   - Nama & versi teknologi (mis. "Go 1.22", "PostgreSQL", "Kafka")
   - Level pengalaman user dengan teknologi ini (pemula total / pernah coba dikit / berpengalaman di bahasa lain tapi baru di ini)
   - Preferensi domain proyek kalau ada (mis. "aku suka bikin sesuatu yang berhubungan dengan e-commerce") — kalau tidak ada preferensi, lanjut ke Step 3 untuk mengusulkan.

### Step 2: Riset via Context7

Sebelum merancang tema atau roadmap, riset teknologi ini dulu:

1. `resolve-library-id` untuk teknologi utama (dan 1-2 library ekosistem yang kemungkinan akan dipakai, mis. driver database, client library).
2. `query-docs` untuk memahami:
   - Struktur proyek idiomatic untuk teknologi ini
   - Tooling standar (build tool, test framework, package manager)
   - **Fitur-fitur unggulan/khas** teknologi ini — ini penting karena akan jadi target akhir roadmap (mis. Go dikenal karena goroutines/channels; PostgreSQL karena indexing/transactions/JSONB; Kafka karena partitioning/consumer groups/delivery guarantees)

Simpan temuan ini secara ringkas — akan dicatat di `roadmap.yaml` sebagai `context7_libraries_consulted`.

### Step 3: Pilih Tema Proyek

Lihat `references/project-theme-heuristics.md` untuk heuristik detail. Ringkasnya:

1. Kerja **mundur dari fitur unggulan** teknologi (hasil Step 2), bukan maju dari ide aplikasi generik. Tema proyek harus punya jalan alami menuju fitur-fitur tersebut.
2. Cek ukuran: skeleton awal (`m00`) harus bisa jalan dalam <30 menit, tapi proyek harus punya titik ekstensi natural ke arah kompleksitas (jangan terlalu trivial seperti "hello world", jangan terlalu luas seperti "platform SaaS lengkap").
3. Susun 1-2 opsi tema konkret dan **konfirmasi ke user** lewat `AskUserQuestion` sebelum lanjut merancang roadmap penuh — jangan langsung putuskan sepihak.

### Step 4: Rancang Roadmap

Lihat `references/roadmap-template.md` untuk skema lengkap dan contoh. Ringkasnya:

1. Brainstorm daftar konsep dari dasar → mahir berdasarkan riset Step 2, mengarah ke fitur-fitur unggulan teknologi tsb.
2. Kelompokkan jadi **8-15 milestone**, tiap milestone berisi 1-3 konsep yang berkaitan, estimasi 30-90 menit pengerjaan.
3. Tiap milestone WAJIB punya field `why_now`: limitasi/kebutuhan KONKRET dari state proyek saat ini yang baru bisa diselesaikan dengan konsep milestone ini. Ini kunci filosofi "project-based" — bukan "sekarang kita belajar X" tapi "proyek kita butuh X karena Y".
4. Sequencing: `m00` = skeleton yang jalan. Lalu pola berulang: **tambah fitur dengan cara naif → fitur itu kelihatan bermasalah/terbatas di kondisi realistis → pelajari konsep untuk memperbaikinya**. Tutup dengan 1-2 milestone kualitas (testing, error handling, observability) supaya proyek selalu berakhir dalam kondisi presentable.
5. Tiap milestone punya `prerequisites` (list milestone id yang harus selesai dulu).

### Step 5: Scaffold Proyek

1. Tentukan `tech-slug` (kebab-case, mis. `go`, `postgresql`, `rabbitmq`) dan `project-slug` (kebab-case dari tema, mis. `url-shortener`).
2. Path proyek: `<PLAYGROUND_ROOT>/<tech-slug>/<project-slug>/`. Pastikan belum ada.
3. **Jalankan langsung command init asli teknologi tsb via Bash** (bukan hardcoded di script generik) — mis. `go mod init <module>`, `cargo init`, `npm init`, dsb — sesuai hasil riset Step 2. Buat skeleton `m00` yang benar-benar bisa dijalankan (mis. HTTP server "hello world", koneksi DB dasar).
4. **Verifikasi skeleton benar-benar jalan** (run/build) sebelum lanjut.
5. Jalankan scaffold meta-files:
   ```bash
   python3 scripts/scaffold_project.py \
     --project-dir "<PLAYGROUND_ROOT>/<tech-slug>/<project-slug>" \
     --tech "<tech-slug>" --slug "<project-slug>" --title "<judul proyek>" \
     --roadmap-json '<json roadmap yang sudah dirancang di Step 4>'
   ```
   Script ini akan menulis `roadmap.yaml`, `progress.json` (milestone pertama `m00` langsung berstatus `completed` karena skeleton sudah diverifikasi jalan), `README.md`, `git init` + commit awal, dan regenerasi index `programming-playground/README.md`.
6. Format JSON roadmap yang diharapkan script: lihat `references/roadmap-template.md` bagian "Schema JSON untuk scaffold_project.py".

### Step 6: Wrap-up

1. Ringkas roadmap secara naratif ke user dalam Bahasa Indonesia: tema proyek, kenapa tema ini cocok untuk teknologi ini, daftar milestone singkat.
2. Arahkan user ke `playground-session-guide` untuk mulai milestone pertama (m01), dan sebutkan `playground-progress-tracker` untuk cek dashboard kapan saja.

## Aturan

### HARUS
- Riset via Context7 SEBELUM merancang tema/roadmap — jangan andalkan pengetahuan training data untuk hal versi-spesifik.
- Setiap milestone punya `why_now` yang konkret, terhubung ke state proyek, bukan penjelasan generik.
- Konfirmasi tema ke user sebelum merancang roadmap penuh (satu round-trip, jangan berlarut-larut).
- Verifikasi skeleton `m00` benar-benar bisa dijalankan sebelum scaffold selesai.
- Cek proyek existing dulu sebelum scaffold (Step 1) — jangan menimpa proyek yang sudah ada.

### JANGAN
- Jangan pakai kurikulum hardcoded/template tetap — setiap teknologi dirancang ulang dari riset Context7-nya sendiri.
- Jangan buat skeleton `m00` melebihi cakupannya sendiri (fitur milestone lain belum boleh diimplementasikan di awal).
- Jangan pilih domain proyek yang terlalu trivial (tidak akan pernah butuh fitur lanjutan) atau terlalu luas (tidak akan pernah selesai skeleton-nya).
- Jangan scaffold ulang proyek yang tech-nya sudah ada tanpa konfirmasi eksplisit dari user.

## Quality Checklist

Sebelum menyatakan proyek siap:
- [ ] Riset Context7 sudah dilakukan dan dicatat di `roadmap.yaml`
- [ ] Tema sudah dikonfirmasi user
- [ ] 8-15 milestone dengan `why_now` konkret per milestone
- [ ] Skeleton `m00` benar-benar berjalan (sudah dites)
- [ ] `roadmap.yaml`, `progress.json`, `README.md` tertulis
- [ ] Git repo ter-init dengan commit awal
- [ ] Index `programming-playground/README.md` ter-update
