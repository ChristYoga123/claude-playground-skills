# Claude Playground Skills

Tiga [Claude Code Skill](https://docs.claude.com/en/docs/claude-code/skills) yang saling melengkapi untuk belajar bahasa pemrograman atau teknologi lain (database, message broker, tool infra, dsb) dengan cara **project-based playground**: bukan tutorial dengan contoh kode yang terpisah-pisah dan dummy, tapi satu proyek nyata yang tumbuh dari skeleton kecil menjadi kompleks seiring konsep-konsep dipelajari — setiap konsep langsung diimplementasikan ke dalam proyek yang sama, jadi kamu selalu paham use-case dan dampak nyatanya ke codebase-mu sendiri.

## Filosofi

Belajar konvensional sering begini: baca teori goroutine → lihat contoh kode 10 baris yang berdiri sendiri → lupa lagi minggu depan karena tidak pernah lihat efeknya di sesuatu yang nyata.

Skill ini membalik itu: kamu mulai dengan proyek kecil (misalnya URL shortener untuk belajar Go), dan setiap konsep baru muncul karena proyekmu **benar-benar membutuhkannya** — server mulai menerima banyak request bersamaan? Saatnya belajar goroutine & mutex. Redirect makin lambat karena selalu query storage? Saatnya belajar caching. Konsepnya menempel karena kamu melihat efeknya langsung di kode yang kamu tulis sendiri, dan git log proyekmu jadi jejak belajar yang bisa ditelusuri ulang.

## Tiga Skill

| Skill | Kapan Dipakai |
|---|---|
| [`playground-project-architect`](./playground-project-architect) | Mulai belajar teknologi baru — riset teknologi via Context7, rancang tema proyek + roadmap milestone, scaffold proyek nyata. |
| [`playground-session-guide`](./playground-session-guide) | Lanjutkan sesi belajar di proyek yang sudah ada — ajarkan konsep berikutnya berakar pada limitasi nyata kode saat ini, implementasikan, commit per milestone. |
| [`playground-progress-tracker`](./playground-progress-tracker) | Lihat progress lintas semua proyek belajar, dapat rekomendasi harus lanjut proyek/milestone yang mana. |

Detail lengkap ada di `SKILL.md` masing-masing folder.

## Instalasi

Skill ini dibaca oleh Claude Code dari direktori skill personal:

```bash
git clone https://github.com/<username>/claude-playground-skills.git
cp -r claude-playground-skills/playground-project-architect \
      claude-playground-skills/playground-session-guide \
      claude-playground-skills/playground-progress-tracker \
      ~/.claude/skills/
chmod +x ~/.claude/skills/playground-*/scripts/*.py
```

Skill akan otomatis terdeteksi Claude Code di sesi berikutnya (cek dengan mengetik nama skill atau memicu salah satu trigger phrase di deskripsinya).

## Workspace

Ketiga skill sepakat memakai satu direktori workspace (`programming-playground/`) tempat semua proyek belajar disimpan, satu subfolder per teknologi:

```
~/programming-playground/            <- default, bisa diganti
  <tech-slug>/                       <- contoh: go, rust, postgresql, kafka
    <project-slug>/                  <- contoh: url-shortener
      .git/                          <- repo git sendiri per proyek
      README.md
      roadmap.yaml                   <- desain naratif: tema, milestone, alasan tiap konsep
      progress.json                  <- state mesin: status/timestamp/commit sha per milestone
      <source code proyek>
```

Default lokasinya `~/programming-playground/`. Kalau kamu mau pakai lokasi lain, cukup sebutkan ke Claude saat mulai ("bikin di folder ~/dev/learning ya"), atau pakai flag `--root <path>` saat memanggil `playground-progress-tracker` secara manual.

## Contoh Pemakaian

```
Kamu: aku mau belajar Go
Claude: [playground-project-architect] riset via Context7, usul tema "URL shortener
        dengan caching & rate limiting", susun 9 milestone, scaffold proyek jalan.

Kamu: lanjut belajar Go
Claude: [playground-session-guide] baca kode saat ini, tunjukkan race condition nyata
        pas load test, ajarkan goroutine + mutex, implementasikan, commit m02.

Kamu: progress belajar aku gimana?
Claude: [playground-progress-tracker] tampilkan dashboard semua proyek + rekomendasi
        lanjut yang mana.
```

## Konvensi Konten

- Narasi/penjelasan konsep: Bahasa Indonesia.
- Kode, istilah teknis, nama field, commit message: Bahasa Inggris.
- Satu commit git bersih per milestone selesai, dengan trailer `Milestone-Id: <id>`.
- Semua script Python bergantung stdlib saja — tidak ada dependency eksternal yang perlu diinstal.

## Lisensi

MIT — lihat [LICENSE](./LICENSE).
