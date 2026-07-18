# Format Dashboard ASCII

## Single-Project (`dashboard.py show <tech>/<slug>`)

```
+============================================================+
|  Dashboard Belajar: Hello Test (go)                        |
+============================================================+
|                                                              |
|  Selesai       : 2 milestone                                |
|  Sedang Jalan  : 0 milestone                                |
|  Perlu Revisit : 0 milestone                                |
|  Belum Mulai   : 1 milestone                                |
|                                                              |
|  Total Waktu   : 0 jam 25 menit                             |
|  Progress      : [######____] 66%                           |
|                                                              |
+--------------------------------------------------------------+
|  Milestone Berikutnya: m02 - Extra concept                  |
|  ditemukan saat sesi                                         |
|                                                              |
|  Sesi Terakhir: 2026-07-18                                   |
+============================================================+
```

Progress bar: 10 karakter, `#` untuk terisi (persentase selesai), `_` untuk sisa.

## All-Projects (`dashboard.py list`)

```
Programming Playground - Semua Proyek Belajar
================================================================

Tech   Slug           Judul                Progress    Sesi Terakhir  Berikutnya
------ -------------- -------------------- ----------- -------------- --------------------------
go     hello-service  Hello Test           2/3 (66%)   2026-07-18     m02: Extra concept
postgresql  order-db  Order Processing DB  1/10 (10%)  2026-07-15     m01: Design orders schema

Total: 2 proyek, 3/13 milestone selesai (23%), 25 menit belajar
```

## Rekomendasi (`dashboard.py recommend`)

Format teks singkat, contoh:

```
Rekomendasi: lanjutkan milestone m02 (Extra concept) di proyek go/hello-service
  -> sesi ini masih in_progress dari sebelumnya.

Reminder: proyek postgresql/order-db sudah 16 hari tidak disentuh.
```

Kalau tidak ada `in_progress`/`needs_revisit`, bentuknya:
```
Rekomendasi: lanjutkan proyek go/hello-service (aktivitas terbaru), milestone m02: Extra concept
  why_now: ditemukan saat sesi belajar
```
