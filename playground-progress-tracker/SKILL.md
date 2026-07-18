---
name: playground-progress-tracker
description: Melacak dan menampilkan progress belajar di semua proyek programming-playground sekaligus (satu proyek per teknologi yang sedang dipelajari), membaca roadmap.yaml dan progress.json tiap proyek, menghitung statistik, menampilkan dashboard ASCII per-proyek maupun gabungan semua proyek, serta merekomendasikan proyek/milestone mana yang sebaiknya dilanjutkan. Gunakan skill ini saat user bertanya "progress belajar aku gimana", "dashboard playground", "project apa aja yang lagi aku kerjain", atau "lanjutin belajar yang mana ya".
metadata:
  version: 1.0.0
---

# Playground Progress Tracker

Skill ini menampilkan progress belajar di semua proyek `programming-playground/` — satu proyek biasanya mewakili satu teknologi yang sedang dipelajari (Go, PostgreSQL, Kafka, dst), masing-masing berjalan independen.

Skill ini bersifat **read-mostly**: penyelesaian milestone yang sesungguhnya (perubahan status jadi `completed`) selalu harus lewat `playground-session-guide` supaya tiap status `completed` punya commit git yang membuktikannya. Skill ini hanya boleh melakukan koreksi klerikal kecil secara eksplisit kalau diminta user (mis. salah catat durasi).

## Workspace

Default lokasi workspace adalah `~/programming-playground/` (dibaca otomatis oleh `scripts/dashboard.py`). Kalau user memakai lokasi lain (mis. di dalam direktori project tertentu), tambahkan `--root <path>` di semua pemanggilan script pada skill ini.

## Kapan Menggunakan Skill Ini

- User tanya "progress belajar aku gimana", "dashboard playground"
- User tanya "project apa aja yang lagi aku kerjain"
- User tanya "lanjutin belajar yang mana ya" / minta rekomendasi
- Setelah `playground-project-architect` atau `playground-session-guide` selesai bekerja, skill lain itu sudah cukup untuk merujuk ke sini — skill ini tidak perlu dipanggil otomatis, hanya saat user eksplisit minta lihat progress.

## Instructions

### Step 1: Discover Semua Proyek

```bash
python3 scripts/dashboard.py list
```

Script ini men-glob `programming-playground/*/*/progress.json` — tidak ada registry terpisah, jadi selalu up to date dengan apa yang benar-benar ada di disk.

Kalau tidak ada proyek sama sekali, arahkan user ke `playground-project-architect`.

### Step 2: Dashboard Satu Proyek

Kalau user tanya soal satu teknologi/proyek spesifik:

```bash
python3 scripts/dashboard.py show <tech>/<slug>
```

Menampilkan ASCII box: jumlah milestone per status, total waktu belajar, progress bar, milestone saat ini + berikutnya (ambil narasi `why_now` singkat dari `roadmap.yaml` untuk memberi konteks, bukan sekadar id).

Lihat `references/dashboard-format.md` untuk format persis.

### Step 3: Dashboard Semua Proyek

Kalau user tanya progress secara umum (tanpa sebut teknologi tertentu):

```bash
python3 scripts/dashboard.py list
```

Tampilkan tabel gabungan (tech, slug, judul, % selesai, sesi terakhir, milestone berikutnya) + total keseluruhan (total proyek, total milestone selesai, total waktu belajar semua proyek).

### Step 4: Rekomendasi

```bash
python3 scripts/dashboard.py recommend
```

Logika (murni berbasis state, BUKAN kurikulum tetap — tidak ada urutan "harus belajar A dulu baru B"):
1. Ada milestone `in_progress` di proyek mana pun → rekomendasikan lanjutkan itu dulu (sesi yang belum selesai).
2. Kalau tidak ada, ada milestone `needs_revisit` → rekomendasikan sesi review.
3. Kalau tidak ada, pilih proyek dengan `last_session_at` paling baru yang masih punya milestone `not_started` (momentum — lanjutkan yang baru saja disentuh).
4. Proyek yang idle >14 hari (dari `last_session_at`) ditandai sebagai reminder halus, bukan dipaksa harus dikerjakan duluan.

Sampaikan rekomendasi dalam Bahasa Indonesia, natural, sertakan alasan singkat (mis. "kamu lagi di tengah milestone m02 di proyek Go, lanjutin itu dulu yuk").

### Step 5: Regenerasi Index

Setiap kali `list` atau `show` dijalankan, script otomatis menulis ulang `programming-playground/README.md` sebagai efek samping (self-healing index, tidak bergantung skill lain untuk memicunya).

## Aturan

### HARUS
- Selalu baca `progress.json` sebagai sumber kebenaran untuk status/statistik (bukan `roadmap.yaml`, yang hanya untuk konteks naratif).
- Arahkan user ke `playground-session-guide` untuk benar-benar menyelesaikan/mengubah status milestone.
- Rekomendasi murni berbasis state proyek, jangan asumsikan urutan belajar lintas teknologi.

### JANGAN
- Jangan tandai milestone `completed` dari skill ini tanpa commit git yang menyertainya — itu tugas `playground-session-guide`.
- Jangan buat registry/file index tambahan selain `programming-playground/README.md` yang auto-generated.
- Jangan memaksa urutan "belajar X dulu baru boleh Y" antar teknologi berbeda.

## Quality Checklist

- [ ] Dashboard menampilkan data yang cocok dengan isi `progress.json` terkini (bukan cache basi)
- [ ] Rekomendasi menyebutkan proyek + milestone + alasan singkat
- [ ] `programming-playground/README.md` ter-update setelah pemanggilan
