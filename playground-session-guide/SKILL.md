---
name: playground-session-guide
description: Memandu satu sesi belajar nyata di dalam proyek playground yang sudah ada — membaca roadmap.yaml dan progress.json proyek, menentukan milestone berikutnya, menjelaskan konsepnya dengan berakar pada limitasi nyata di kode proyek saat ini (bukan contoh kode terpisah), mengimplementasikan konsep tersebut langsung ke source code proyek (mode pair-programming atau hint/latihan mandiri), lalu commit git per milestone dengan pesan yang menyebut konsep yang dipelajari. Gunakan skill ini saat user bilang "lanjut belajar <teknologi>", "lanjut proyek playground", "ajarin aku <konsep> di project ini", atau ingin melanjutkan sesi belajar yang sudah dimulai.
metadata:
  version: 1.5.0
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

### Step 3: Pilih Sumber Referensi Materi (sekali per sesi)

Sebelum menjelaskan milestone pertama di sesi ini, tanyakan ke user lewat `AskUserQuestion` mau pakai sumber referensi apa untuk teori sepanjang sesi ini:

- **AI yang riset** (default) — Claude riset sendiri via Context7 seperti biasa (lanjut ke Step 4).
- **Saya kasih referensi sendiri** — user boleh ketik langsung materi/poin-poin di chat, ATAU kasih path file lokal / URL yang sudah dia siapkan. Kalau file lokal, `Read` isinya; kalau URL, `WebFetch`. Materi ini jadi basis utama penjelasan teori di Step 4 — Context7 tetap boleh dipakai sebagai pelengkap kalau referensi user tidak menyebutkan detail teknis/API spesifik yang dibutuhkan.

**Lewati pertanyaan ini** (langsung pakai default AI riset) kalau:
- User sudah eksplisit menyebutkan preferensi di awal permintaan sesi ini (mis. "pakai materi dari file ini aja", "jelasin pakai gaya buku X").
- Sesi ini melanjutkan sesi yang sudah pernah ditanya sebelumnya (pilihan sudah didapat, jangan tanya ulang tiap kali user bilang "lanjut").

Preferensi ini berlaku untuk **seluruh sesi** (semua milestone yang dikerjakan sampai percakapan ini berakhir), bukan per milestone — tidak perlu ditulis ke `progress.json`, cukup diingat sepanjang percakapan. Kalau user ganti pikiran di tengah sesi (mis. minta pakai referensi sendiri padahal tadinya AI), ikuti perubahan itu untuk milestone berikutnya.

### Step 4: Ground Konsep di Pain Point Nyata

Ini langkah paling penting — jangan mengajar dari `why_now` di `roadmap.yaml` mentah-mentah, itu cuma hipotesis awal:

1. Baca source code proyek saat ini (file-file relevan, bukan cuma README) untuk menemukan/mengonfirmasi limitasi konkret — sebutkan fungsi/baris spesifik yang akan bermasalah tanpa konsep milestone ini.
2. Kalau memungkinkan, **reproduksi masalahnya secara live** sebelum mengajarkan solusi: jalankan program, tunjukkan race condition/error/query lambat/dst yang nyata terjadi. Ini membuat efek konsep terasa konkret, bukan abstrak.
3. Sesuai pilihan Step 3: kalau sumber referensi "AI yang riset", query **Context7** untuk konsep/API spesifik yang akan diajarkan sekarang — jangan hanya andalkan riset architect yang mungkin sudah agak umum, verifikasi cara idiomatic terkini. Kalau sumber referensi "dari user", dasarkan penjelasan pada materi yang sudah diberikan user itu (boleh tetap cross-check ke Context7 untuk detail teknis yang tidak disebutkan materi user).
4. Jelaskan konsepnya dalam Bahasa Indonesia, dengan analogi kalau membantu, selalu dikaitkan balik ke limitasi nyata proyek yang baru saja ditunjukkan.

Lihat `references/teaching-mode-guide.md` untuk contoh dialog dan cara membingkai penjelasan.

### Step 5: Tulis Catatan Lengkap ke Folder `notes/` (SEBELUM kasih tugas)

Begitu teori di Step 3 selesai dijelaskan — sebelum memberi tugas/hint ke user — tulis catatan lengkap ke file terpisah di proyek. Tujuannya jadi **panduan tertulis mandiri yang bisa dibuka user sambil mengerjakan**, bukan ringkasan tipis yang cuma mengulang chat.

1. Buat folder `notes/<milestone-id>-<slug-singkat>/` di root proyek kalau belum ada (mis. `notes/m01-var-const/`, `notes/m08-channel-waitgroup/`). Buat juga folder induk `notes/` kalau proyek belum punya.
2. Tulis `notes/<id>-<slug>/README.md` dengan struktur:
   - **Judul & konsep** — daftar istilah teknis yang dicakup.
   - **Penjelasan lengkap** — definisi, kenapa konsep ini ada, kapan dipakai. Boleh dan didorong pakai **contoh dummy/generik** yang berdiri sendiri (tidak harus dari proyek ini) kalau itu membuat konsep lebih jelas dipahami sebelum masuk ke konteks proyek. Tulis sederhana tapi detail, hindari jargon tanpa penjelasan.
   - **Code block** untuk tiap contoh (baik dummy maupun cuplikan nyata dari proyek).
   - **Diagram** — pakai Mermaid (```mermaid) kalau konsepnya punya alur/struktur yang lebih mudah dipahami secara visual. **Wajib** untuk konsep concurrency (goroutine, channel, select, worker pool, context) — gambarkan data flow antar goroutine/channel pakai `sequenceDiagram` atau `flowchart` (mis. goroutine mana kirim ke channel mana, kapan `select` memilih cabang mana). Untuk struct/pointer, diagram referensi memori (siapa menunjuk ke mana) juga sangat membantu. Untuk konsep yang murni sintaksis (var/const dasar) diagram opsional — jangan dipaksakan kalau tidak menambah kejelasan.
   - Section terakhir **`## Tugas di Proyek Ini`** — baru di sini dikaitkan ke pain point nyata proyek dari Step 4 (fungsi/file spesifik yang harus diubah), dengan sedikit panduan progresif (bukan solusi penuh, ikuti tier hint di `references/teaching-mode-guide.md` kalau mode hint).
3. Update `README.md` root proyek: section `## Learning Notes` cukup jadi **daftar link**, jangan duplikasi isi lengkap di situ:
   ```markdown
   ## Learning Notes
   - [m01: Proper var declarations & constants](./notes/m01-var-const/README.md)
   ```
4. Bagian "Tugas di Proyek Ini" ditulis prospektif (kondisi yang SEDANG diperbaiki) karena tugas belum selesai saat ini ditulis. Kalau implementasi akhir user berbeda dari rencana, revisi bagian itu secukupnya di Step 8 sebelum commit — bagian teori/diagram di atasnya biasanya tidak perlu berubah karena tidak bergantung pada implementasi spesifik user.

### Step 6: Pilih Mode Sesi

Default mode adalah **hint / latihan mandiri** — skill ini dirancang seperti website coding-playground: user mengetik sendiri agar terbiasa dengan syntax-nya, bukan dituliskan Claude. Langsung pakai mode ini tanpa bertanya, kecuali:

- User sudah menyatakan preferensi eksplisit lain di awal ("mode pair-programming aja", dst).
- `progress.json` sudah mencatat `mode` untuk milestone yang sedang di-resume — lanjutkan mode yang sama.
- Konteksnya jelas butuh pair-programming (mis. konsep terlalu setup-heavy/boilerplate untuk latihan mandiri, atau user eksplisit minta contoh dulu) — dalam kasus ini, tawarkan lewat `AskUserQuestion` alih-alih otomatis pindah mode.

- **Hint / latihan mandiri** (default): Claude TETAP jelaskan teori dasar konsepnya dulu (apa itu, kenapa ada, syntax/semantics dasar — sama dalamnya dengan pair-programming, lihat Step 4), baru beri arahan tugas + limitasi yang harus diperbaiki + sedikit panduan cara mengerjakannya di proyek ini (bukan solusi penuh), lalu hint bertingkat lanjutan kalau masih stuck (lihat `references/teaching-mode-guide.md` untuk mekanisme tier). User coba sendiri dulu, Claude review hasilnya (baca file + jalankan test/build), beri feedback, baru tulis kode kalau user stuck atau minta. **Hint mode bukan berarti user dilepas tanpa teori** — bedanya dengan pair-programming ada di siapa yang mengetik kode, bukan di seberapa lengkap konsep dijelaskan.
- **Pair-programming**: Claude jelaskan konsep, lalu implementasikan langsung ke file proyek sambil menjelaskan tiap perubahan.

Simpan mode yang dipilih ke `progress.json` (lewat `update_progress.py start`, lihat Step 10).

### Step 7: Implementasi Nyata

- Perubahan HARUS masuk ke file proyek yang sungguhan — extend fungsi/struktur yang sudah ada, JANGAN buat file demo terpisah yang tidak terhubung ke aplikasi utama.
- Kalau mode hint/latihan mandiri: setelah user submit hasil kerjanya, Read file yang diubah, bandingkan dengan ekspektasi, beri feedback konkret merujuk ke baris/fungsi tertentu.

### Step 8: Verifikasi

1. Jalankan build/test/run proyek untuk membuktikan konsep sudah bekerja.
2. Re-run reproduksi pain point dari Step 4 (kalau ada) untuk menunjukkan masalahnya sudah teratasi — ini bagian penting untuk "menutup loop" pembelajaran.
3. Cek balik section `## Tugas di Proyek Ini` di `notes/<id>-<slug>/README.md` yang ditulis di Step 5 — kalau implementasi akhir user berbeda dari yang direncanakan saat teori dijelaskan, revisi bagian itu secukupnya supaya tetap akurat.

### Step 9: Commit per Milestone

1. Stage HANYA file yang relevan dengan milestone ini.
2. Commit dengan format dari `references/commit-message-convention.md`:
   - Subject: `<milestone-id>: <ringkasan konsep>` (Bahasa Inggris, konsisten dengan `title` di roadmap)
   - Body: jelaskan pain point yang diperbaiki + apa yang dipelajari (boleh Bahasa Indonesia singkat)
   - Trailer: `Milestone-Id: <id>`
3. **Aturan keras: satu commit bersih per milestone selesai.** Jangan pernah commit kondisi rusak/setengah jadi sebagai milestone commit.
4. Kalau sesi terputus sebelum milestone selesai: JANGAN commit kondisi WIP. Biarkan working tree apa adanya, catat status `in_progress` dengan `notes` yang menjelaskan progress terakhir (lewat `update_progress.py start` dengan `--notes`), supaya sesi berikutnya bisa resume dengan jelas.

### Step 10: Update `progress.json`

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

### Step 11: Tutup Sesi

1. Ringkas apa yang baru dipelajari dan bagaimana itu mengubah proyek.
2. Beri teaser singkat `why_now` milestone berikutnya (bikin penasaran, jangan spoiler penuh).
3. Sebutkan `playground-progress-tracker` kalau user ingin lihat dashboard keseluruhan.

## Edge Cases

- **Scope creep ditemukan mid-sesi** (mis. user ingin eksplorasi sesuatu di luar roadmap): tawarkan untuk menambah milestone baru ke `roadmap.yaml` (edit langsung, sisipkan di posisi yang masuk akal) dan ke `progress.json` (lewat `update_progress.py append-milestone`), dengan `why_now: "ditemukan saat sesi belajar"`. Konfirmasi dulu ke user sebelum menambah.
- **Revisit milestone yang sudah `completed`**: pakai prefix commit `revisit(<id>): <ringkasan>` untuk membedakan dari commit milestone asli, lalu `update_progress.py revisit`.

## Aturan

### HARUS
- Ground penjelasan di kode proyek yang SUNGGUHAN, bukan contoh generik — baca dulu, baru jelaskan.
- Jelaskan teori dasar konsep secara penuh SEBELUM memberi hint/tugas, di mode apa pun (termasuk hint/latihan mandiri) — jangan lompat langsung ke "coba cari sendiri konsep apa" tanpa mengajarkan teorinya dulu.
- Tulis catatan lengkap (teori + contoh + diagram kalau relevan + tugas) ke `notes/<id>-<slug>/README.md` SEBELUM memberi tugas ke user (Step 5), bukan setelah selesai — supaya jadi panduan tertulis yang bisa dibuka sambil mengerjakan. `README.md` root proyek cukup berisi link ke folder ini, jangan biarkan penjelasan cuma ada di chat.
- Sertakan diagram Mermaid di catatan untuk konsep concurrency (goroutine/channel/select/worker pool/context) supaya data flow-nya kelihatan, bukan cuma teks.
- Tanyakan sumber referensi materi (AI riset vs referensi user sendiri) sekali di awal sesi (Step 3), kecuali sudah jelas dari konteks permintaan user atau sesi lanjutan yang sudah pernah ditanya.
- Verifikasi solusi via Context7 untuk konsep spesifik yang sedang diajarkan sekarang (kecuali user pilih referensi sendiri — dalam kasus itu Context7 jadi pelengkap, bukan sumber utama).
- Satu commit bersih per milestone selesai, dengan format & trailer yang konsisten.
- Update `progress.json` lewat `update_progress.py`, bukan edit manual (supaya timestamp & state transition konsisten).
- Tanyakan mode sesi (pair vs hint) kecuali sudah jelas dari konteks.

### JANGAN
- Jangan commit kondisi WIP/rusak sebagai milestone commit.
- Jangan buat file demo terpisah — semua implementasi masuk ke proyek utama.
- Jangan skip Step 4 (grounding di pain point nyata) — ini yang membedakan skill ini dari tutorial biasa.
- Jangan improvisasi bikin proyek baru dari skill ini — itu tugas `playground-project-architect`.
- Jangan tanya ulang sumber referensi materi tiap milestone dalam sesi yang sama — cukup sekali di awal (Step 3).

## Quality Checklist

- [ ] Konsep dijelaskan dengan merujuk kode/limitasi nyata proyek (bukan generik)
- [ ] Sumber referensi materi (AI/user) sudah dikonfirmasi di awal sesi
- [ ] Context7 sudah dicek untuk konsep spesifik ini (atau referensi user dipakai sebagai basis utama)
- [ ] Mode sesi (pair/hint) sudah dikonfirmasi
- [ ] Implementasi masuk ke file proyek sungguhan, sudah diverifikasi jalan (build/test/run)
- [ ] `notes/<id>-<slug>/README.md` sudah berisi teori lengkap + contoh + tugas (dan diagram Mermaid kalau konsepnya concurrency/struktural), dan root `README.md` sudah link ke situ
- [ ] Satu commit bersih dengan pesan sesuai konvensi
- [ ] `progress.json` ter-update lewat script (bukan manual)
