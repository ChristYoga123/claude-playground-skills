# Konvensi Commit per Milestone

## Format

```
<milestone-id>: <ringkasan konsep, Bahasa Inggris, singkat>

<body: 1-3 kalimat, boleh Bahasa Indonesia, jelaskan pain point yang
diperbaiki dan apa yang dipelajari>

Milestone-Id: <milestone-id>
```

## Contoh

```
m02: Add mutex to protect concurrent map access

Store.Get()/Set() sebelumnya race saat diakses banyak goroutine sekaligus
(kelihatan jelas pakai `go test -race`). Sekarang dilindungi sync.Mutex.

Milestone-Id: m02
```

Contoh revisit:
```
revisit(m02): Re-explain mutex vs RWMutex tradeoff

Milestone m02 di-revisit karena sebelumnya masih bingung soal kapan pakai
RWMutex vs Mutex biasa. Ditambahkan RWMutex + benchmark perbandingan.

Milestone-Id: m02
```

## Aturan

- Subject baris pertama: `<id>: <title milestone>` atau ringkasan yang jelas kalau sedikit berbeda dari `title` di roadmap — tetap dalam Bahasa Inggris supaya `git log --oneline` konsisten dan mudah dibaca sebagai jejak teknis.
- Body boleh campur Bahasa Indonesia untuk narasi, tapi istilah teknis/nama fungsi tetap apa adanya (Bahasa Inggris).
- Trailer `Milestone-Id: <id>` WAJIB ada — dipakai `playground-progress-tracker` dan `git log --grep "Milestone-Id: m02"` untuk lookup cepat.
- Satu milestone = satu commit. Kalau butuh multiple commit teknis saat eksplorasi (coba-coba), squash jadi satu sebelum menyelesaikan milestone, atau gunakan `git commit --amend` selama belum lanjut ke milestone berikutnya.
- Jangan campur perubahan dari 2 milestone berbeda dalam 1 commit.

## Cara Membuat Commit (contoh Bash)

```bash
git add <file-file yang relevan dengan milestone ini>
git commit -m "m02: Add mutex to protect concurrent map access" -m "Store.Get()/Set() sebelumnya race saat diakses banyak goroutine sekaligus (kelihatan jelas pakai \`go test -race\`). Sekarang dilindungi sync.Mutex.

Milestone-Id: m02"
```

Ambil short SHA setelahnya untuk dicatat ke `progress.json`:
```bash
git rev-parse --short HEAD
```
