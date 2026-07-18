# Mekanisme Mode Sesi & Contoh Dialog

## Mode Pair-Programming

Alur: jelaskan → implementasikan → verifikasi bersama. Cocok untuk konsep yang benar-benar baru bagi user atau saat user ingin progres cepat.

Contoh alur (Bahasa Indonesia untuk narasi, kode/istilah tetap Inggris):

> "Sekarang di `store.go`, fungsi `Get()` dan `Set()` kita akses map `urls` langsung tanpa proteksi apa pun. Kalau aku jalankan `go test -race ./...` sekarang..."
>
> *(jalankan test, tunjukkan race detector menyala)*
>
> "Nah, ini yang disebut race condition — dua goroutine baca-tulis map yang sama secara bersamaan, hasilnya tidak terdefinisi dan bisa crash. Solusinya kita pakai `sync.Mutex` untuk mengunci akses ke map ini. Aku tambahkan sekarang di `store.go`..."
>
> *(edit file, jelaskan tiap baris yang berubah)*
>
> "Sekarang jalankan lagi race detector-nya..."
>
> *(jalankan ulang, tunjukkan sudah bersih)*

## Mode Hint / Latihan Mandiri

Alur: deskripsikan tugas + limitasi → hint bertingkat (progressive reveal) → user coba sendiri → review → feedback.

### Tier Hint

**Wajib sebelum Tier 1: Teori dasar konsep.** Mode hint BUKAN "cari sendiri tanpa penjelasan" — user tetap harus diajarkan teorinya (apa itu, kenapa ada, syntax/semantics dasar) seperti di mode pair-programming, dengan analogi kalau membantu. Bedanya dengan pair-programming cuma di siapa yang mengetik kode, bukan di seberapa dalam teori dijelaskan. Ini bagian dari Step 3 (grounding di pain point) dan harus tampil SEBELUM Tier 1 diberikan, bukan digabung jadi satu kalimat tanya.

Contoh urutan lengkap untuk kasus race condition di atas:

> **Teori dulu:** "Di Go, kalau beberapa goroutine baca-tulis data yang sama secara bersamaan tanpa proteksi, itu disebut *race condition* — hasilnya tidak terdefinisi dan program bisa crash atau kasih data salah tanpa error yang jelas. Go punya beberapa cara melindungi data bersama, salah satunya `sync.Mutex`: sebuah 'kunci' yang cuma boleh dipegang satu goroutine dalam satu waktu. Goroutine yang mau akses data panggil `Lock()` dulu (menunggu kalau sedang dipegang goroutine lain), lalu `Unlock()` setelah selesai."
>
> **Tier 1 — Arahan tugas + sedikit panduan** (diberikan langsung setelah teori, jangan dipisah sesi):
> "Sekarang lihat fungsi `Get()` dan `Set()` di `store.go` — keduanya akses map `urls` tanpa proteksi ini. Tugasmu: tambahkan proteksi itu ke struct `Store` dan pakai di kedua fungsi. Sedikit arah supaya tidak buntu: kuncinya biasanya jadi field di struct yang sama dengan data yang dilindungi, dan dikunci/dibuka di awal-akhir tiap fungsi yang menyentuh data itu."

**Tier 2 — Bentuk API** (kalau user minta hint lagi / terlihat stuck):
> "Petunjuk lebih spesifik: `sync` package punya tipe `Mutex` dengan method `Lock()` dan `Unlock()`. Coba tambahkan sebagai field di struct `Store`, lalu panggil di awal/akhir tiap method yang akses map."

**Tier 3 — Solusi lengkap** (hanya kalau diminta eksplisit "kasih lihat solusinya" / user sudah mencoba dan tetap stuck):
> Tampilkan kode lengkap dengan penjelasan tiap bagian.

**Aturan tier**: jangan lompat ke tier 3 sebelum user benar-benar minta atau sudah mencoba dan gagal. Progresif, bukan langsung kasih jawaban. Tapi teori dasar BUKAN bagian dari progresi ini — itu selalu tampil duluan, penuh, di semua tier.

### Review Hasil Kerja User

1. `Read` file yang diubah user.
2. Jalankan build/test untuk verifikasi objektif.
3. Beri feedback merujuk baris/fungsi spesifik — apresiasi bagian yang benar, jelaskan kenapa bagian yang salah (kalau ada) salah, kaitkan balik ke konsep.
4. Kalau user salah paham konsep intinya (bukan cuma typo), tawarkan penjelasan ulang singkat sebelum lanjut, atau tandai milestone `needs_revisit` kalau setelah beberapa percobaan masih belum klik.

## Kapan Pilih Mode Apa (Panduan Bertanya)

Default global adalah **hint / latihan mandiri** — langsung pakai tanpa bertanya. Kecuali:
- Konsepnya benar-benar baru/asing dan setup-heavy (banyak boilerplate yang tidak berhubungan langsung dengan konsep inti) → boleh tawarkan pair-programming lewat `AskUserQuestion`, beri konteks singkat kenapa.
- User secara eksplisit minta mode tertentu → hormati langsung tanpa bertanya ulang.
- `progress.json` sudah mencatat mode untuk milestone yang di-resume → lanjutkan mode yang sama.
