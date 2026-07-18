---
name: playground-session-guide
description: Memandu satu sesi belajar nyata di dalam proyek playground yang sudah ada — membaca roadmap.yaml dan progress.json proyek, menentukan milestone berikutnya, menjelaskan konsepnya dengan berakar pada limitasi nyata di kode proyek saat ini (bukan contoh kode terpisah), mengimplementasikan konsep tersebut langsung ke source code proyek (mode pair-programming atau hint/latihan mandiri), lalu commit git per milestone dengan pesan yang menyebut konsep yang dipelajari. Gunakan skill ini saat user bilang "lanjut belajar <teknologi>", "lanjut proyek playground", "ajarin aku <konsep> di project ini", atau ingin melanjutkan sesi belajar yang sudah dimulai.
metadata:
  version: 1.0.0
---

# Playground Session Guide

Skill ini menjalankan SATU sesi belajar nyata di dalam proyek playground yang sudah dibuat oleh `playground-project-architect`. Filosofinya: konsep yang diajarkan HARUS terhubung ke limitasi konkret yang benar-benar ada di kode proyek saat ini — bukan penjelasan generik yang kebetulan diimplementasikan di proyek ini.

Kalau belum ada proyek untuk teknologi yang dimaksud, arahkan ke `playground-project-architect` dulu. Untuk melihat progress semua proyek, arahkan ke `playground-progress-tracker`.

## Workspace

Semua proyek belajar ada di direktori workspace `programming-playground/` (default `~/programming-playground/`, atau lokasi lain yang sudah dipakai user sebelumnya — lihat proyek yang sudah ada dengan glob `**/progress.json` kalau tidak yakin). Di skill ini, `<PLAYGROUND_ROOT>` merujuk ke direktori tsb.

## Kapan Menggunakan Skill Ini

- User bilang "lanjut belajar Go/Rust/dst" atau "lanjut project playground"
- User minta diajarkan konsep tertentu di proyek yang sudah berjalan
- User ingin melanjutkan sesi yang sempat terputus (milestone berstatus `in_progress`)

## Instructions

### Step 1: Lokasikan Proyek

1. Kalau user sebut teknologi/nama proyek eksplisit, cari di `<PLAYGROUND_ROOT>/<tech>/<slug>/`.
2. Kalau ambigu (ada beberapa proyek match, atau tidak disebut sama sekali), glob `<PLAYGROUND_ROOT>/*/*/progress.json`, tampilkan daftar singkat, tanyakan lewat `AskUserQuestion` — atau kalau user hanya bilang "lanjut belajar" tanpa spesifik, rekomendasikan proyek yang paling baru `last_session_at`-nya.
3. Kalau tidak ada proyek sama sekali untuk teknologi yang diminta: beri tahu user, arahkan ke `playground-project-architect`. **Jangan** improvisasi bikin proyek sendiri dari skill ini.

### Step 2: Muat State

1. Baca `roadmap.yaml` (naratif lengkap) dan `progress.json` (status mesin) di proyek tsb.
2. Tentukan milestone berikutnya: prioritaskan milestone berstatus `in_progress` (lanjutkan sesi terputus) → lalu milestone `needs_revisit` kalau user secara eksplisit minta review → lalu milestone `not_started` pertama yang semua `prerequisites`-nya `completed`.
3. Kalau user secara eksplisit minta milestone/konsep lain (bukan urutan default), hormati permintaan itu — cek dulu prerequisite-nya terpenuhi, kalau belum beri tahu dan konfirmasi apakah tetap lanjut.

### Step 3: Ground Konsep di Pain Point Nyata

Ini langkah paling penting — jangan mengajar dari `why_now` di `roadmap.yaml` mentah-mentah, itu cuma hipotesis awal:

1. Baca source code proyek saat ini (file-file relevan, bukan cuma README) untuk menemukan/mengonfirmasi limitasi konkret — sebutkan fungsi/baris spesifik yang akan bermasalah tanpa konsep milestone ini.
2. Kalau memungkinkan, **reproduksi masalahnya secara live** sebelum mengajarkan solusi: jalankan program, tunjukkan race condition/error/query lambat/dst yang nyata terjadi. Ini membuat efek konsep terasa konkret, bukan abstrak.
3. Query **Context7** untuk konsep/API spesifik yang akan diajarkan sekarang — jangan hanya andalkan riset architect yang mungkin sudah agak umum; verifikasi cara idiomatic terkini untuk kasus spesifik ini.
4. Jelaskan konsepnya dalam Bahasa Indonesia, dengan analogi kalau membantu, selalu dikaitkan balik ke limitasi nyata proyek yang baru saja ditunjukkan.

Lihat `references/teaching-mode-guide.md` untuk contoh dialog dan cara membingkai penjelasan.

### Step 4: Pilih Mode Sesi

Tanyakan lewat `AskUserQuestion` (kecuali user sudah menyatakan preferensi eksplisit di awal, atau `progress.json` sudah mencatat `mode` untuk milestone yang sedang di-resume):

- **Pair-programming**: Claude jelaskan konsep, lalu implementasikan langsung ke file proyek sambil menjelaskan tiap perubahan.
- **Hint / latihan mandiri**: Claude jelaskan tugas + limitasi yang harus diperbaiki, beri hint bertingkat (lihat `references/teaching-mode-guide.md` untuk mekanisme tier), user coba sendiri dulu, Claude review hasilnya (baca file + jalankan test/build), beri feedback, baru tulis kode kalau user stuck atau minta.

Simpan mode yang dipilih ke `progress.json` (lewat `update_progress.py start`, lihat Step 8).

### Step 5: Implementasi Nyata

- Perubahan HARUS masuk ke file proyek yang sungguhan — extend fungsi/struktur yang sudah ada, JANGAN buat file demo terpisah yang tidak terhubung ke aplikasi utama.
- Kalau mode hint/latihan mandiri: setelah user submit hasil kerjanya, Read file yang diubah, bandingkan dengan ekspektasi, beri feedback konkret merujuk ke baris/fungsi tertentu.

### Step 6: Verifikasi

1. Jalankan build/test/run proyek untuk membuktikan konsep sudah bekerja.
2. Re-run reproduksi pain point dari Step 3 (kalau ada) untuk menunjukkan masalahnya sudah teratasi — ini bagian penting untuk "menutup loop" pembelajaran.

### Step 7: Commit per Milestone

1. Stage HANYA file yang relevan dengan milestone ini.
2. Commit dengan format dari `references/commit-message-convention.md`:
   - Subject: `<milestone-id>: <ringkasan konsep>` (Bahasa Inggris, konsisten dengan `title` di roadmap)
   - Body: jelaskan pain point yang diperbaiki + apa yang dipelajari (boleh Bahasa Indonesia singkat)
   - Trailer: `Milestone-Id: <id>`
3. **Aturan keras: satu commit bersih per milestone selesai.** Jangan pernah commit kondisi rusak/setengah jadi sebagai milestone commit.
4. Kalau sesi terputus sebelum milestone selesai: JANGAN commit kondisi WIP. Biarkan working tree apa adanya, catat status `in_progress` dengan `notes` yang menjelaskan progress terakhir (lewat `update_progress.py start` dengan `--notes`), supaya sesi berikutnya bisa resume dengan jelas.

### Step 8: Update `progress.json`

```bash
python3 scripts/update_progress.py complete \
  --project "<PLAYGROUND_ROOT>/<tech>/<slug>" \
  --milestone <id> --commit <sha> --duration <menit> --mode <pair|hint> \
  --notes "<ringkasan singkat Bahasa Indonesia>"
```

Untuk memulai/menandai sesi yang belum selesai:
```bash
python3 scripts/update_progress.py start \
  --project "<path>" --milestone <id> --mode <pair|hint> --notes "<catatan resume>"
```

Untuk milestone yang perlu diulang atau di-skip, lihat subcommand `revisit` dan `skip` (dokumentasi lengkap ada di help script: `python3 scripts/update_progress.py --help`).

### Step 9: Tutup Sesi

1. Ringkas apa yang baru dipelajari dan bagaimana itu mengubah proyek.
2. Beri teaser singkat `why_now` milestone berikutnya (bikin penasaran, jangan spoiler penuh).
3. Sebutkan `playground-progress-tracker` kalau user ingin lihat dashboard keseluruhan.

## Edge Cases

- **Scope creep ditemukan mid-sesi** (mis. user ingin eksplorasi sesuatu di luar roadmap): tawarkan untuk menambah milestone baru ke `roadmap.yaml` (edit langsung, sisipkan di posisi yang masuk akal) dan ke `progress.json` (lewat `update_progress.py append-milestone`), dengan `why_now: "ditemukan saat sesi belajar"`. Konfirmasi dulu ke user sebelum menambah.
- **Revisit milestone yang sudah `completed`**: pakai prefix commit `revisit(<id>): <ringkasan>` untuk membedakan dari commit milestone asli, lalu `update_progress.py revisit`.

## Aturan

### HARUS
- Ground penjelasan di kode proyek yang SUNGGUHAN, bukan contoh generik — baca dulu, baru jelaskan.
- Verifikasi solusi via Context7 untuk konsep spesifik yang sedang diajarkan sekarang.
- Satu commit bersih per milestone selesai, dengan format & trailer yang konsisten.
- Update `progress.json` lewat `update_progress.py`, bukan edit manual (supaya timestamp & state transition konsisten).
- Tanyakan mode sesi (pair vs hint) kecuali sudah jelas dari konteks.

### JANGAN
- Jangan commit kondisi WIP/rusak sebagai milestone commit.
- Jangan buat file demo terpisah — semua implementasi masuk ke proyek utama.
- Jangan skip Step 3 (grounding di pain point nyata) — ini yang membedakan skill ini dari tutorial biasa.
- Jangan improvisasi bikin proyek baru dari skill ini — itu tugas `playground-project-architect`.

## Quality Checklist

- [ ] Konsep dijelaskan dengan merujuk kode/limitasi nyata proyek (bukan generik)
- [ ] Context7 sudah dicek untuk konsep spesifik ini
- [ ] Mode sesi (pair/hint) sudah dikonfirmasi
- [ ] Implementasi masuk ke file proyek sungguhan, sudah diverifikasi jalan (build/test/run)
- [ ] Satu commit bersih dengan pesan sesuai konvensi
- [ ] `progress.json` ter-update lewat script (bukan manual)
