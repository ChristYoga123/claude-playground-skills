# Heuristik Memilih Tema Proyek

Tujuan: pilih SATU tema proyek yang cukup kompleks untuk secara alami membutuhkan fitur-fitur unggulan teknologi yang sedang dipelajari, tanpa terlalu luas sehingga tidak pernah selesai skeleton awalnya.

## Prinsip Utama: Kerja Mundur dari Fitur Unggulan

Jangan mulai dari "ide aplikasi keren", mulai dari "fitur apa yang membuat teknologi ini spesial" (hasil riset Context7 di Step 2), lalu cari domain proyek yang **butuh** fitur itu untuk bekerja dengan benar — bukan sekadar bisa memakainya secara opsional.

Contoh alur berpikir yang BENAR:
- Riset: Go dikenal karena goroutines, channels, dan concurrency primitives yang ringan.
- Domain yang butuh ini secara alami: layanan yang harus menangani banyak request/koneksi bersamaan (URL shortener dengan traffic tinggi, chat server, web scraper paralel, task queue worker).
- Domain yang TIDAK cocok: kalkulator CLI sederhana (tidak pernah butuh concurrency untuk bekerja benar).

Contoh alur berpikir yang SALAH:
- "Aku suka aplikasi to-do list, jadi kita bikin to-do list pakai Go" — lalu goroutines dipaksakan masuk sebagai fitur tempelan yang tidak organik.

## Heuristik per Kategori Teknologi

**Bahasa pemrograman (Go, Rust, Python async, dll)**
→ Layanan networked/concurrent kecil-menengah: URL shortener dengan caching, chat server, job queue/worker pool, CLI berbasis plugin, web scraper paralel dengan rate limiting.
→ Alasannya: bahasa-bahasa modern biasanya unggul di I/O, concurrency, dan error handling — semua butuh beban kerja nyata (banyak request/koneksi/goroutine) untuk terasa gunanya.

**Database relasional (PostgreSQL, MySQL, dll)**
→ Aplikasi dengan skema yang tumbuh dan beban query yang meningkat: katalog produk + pesanan (e-commerce mini), sistem inventaris multi-gudang, social feed dengan follow/like.
→ Alasannya: indexing, transaction, JSONB/full-text search, replication, dan query optimization baru terasa perlu kalau data dan relasinya cukup kompleks — bukan tabel tunggal.

**Database NoSQL / key-value / cache (Redis, MongoDB, dll)**
→ Aplikasi yang butuh akses cepat berulang atau struktur data fleksibel: leaderboard real-time, session store, rate limiter, feed dengan skema yang sering berubah.

**Message broker (Kafka, RabbitMQ, NATS, dll)**
→ Pipeline event-driven: pemrosesan pesanan (order placed → payment → shipping → notification), fan-out notifikasi, log aggregation.
→ Alasannya: broker baru menunjukkan nilainya (partitioning, consumer groups, delivery guarantees, dead-letter queue) kalau ada beberapa consumer/producer independen dan skenario kegagalan yang realistis.

**Infra/DevOps tool (Docker, Kubernetes, Terraform, dll)**
→ Deploy & operasikan salah satu proyek di atas — infra tool selalu butuh workload nyata untuk dipraktikkan, jangan jadi proyek "kosong" berisi hanya konfigurasi tanpa aplikasi yang jalan di dalamnya.

## Cek Ukuran Sebelum Finalisasi

1. **Skeleton `m00` < 30 menit**: bisa di-scaffold dan dijalankan (walau masih sangat sederhana) dalam waktu singkat. Kalau setup awal saja butuh berjam-jam, tema kebesaran.
2. **Ada jalan natural ke fitur lanjutan**: coba petakan cepat 3-5 fitur unggulan hasil riset ke bagian proyek mana yang akan membutuhkannya. Kalau ada fitur unggulan yang tidak menemukan tempat wajar di tema ini, pertimbangkan tema lain atau perluas scope sedikit.
3. **Tidak infinite-scope**: proyek harus punya titik "selesai" yang jelas (mis. "sistem pemrosesan pesanan end-to-end dengan retry & dead-letter queue") — bukan "platform serba bisa" yang bisa terus diperluas tanpa batas.

## Konfirmasi ke User

Setelah menentukan 1-2 kandidat tema, sampaikan singkat ke user (lewat `AskUserQuestion` atau langsung dalam teks kalau opsinya jelas):
- Nama tema + deskripsi 1-2 kalimat
- Kenapa tema ini cocok untuk teknologi yang mau dipelajari (sebutkan fitur unggulan yang akan tersentuh)
- Estimasi kompleksitas akhir (jumlah milestone kira-kira)

Jangan lanjut ke Step 4 (rancang roadmap penuh) sebelum ada konfirmasi.
