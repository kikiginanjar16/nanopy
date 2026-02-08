# 🗨️ Contoh Diskusi & Penggunaan NanoPyBot

Dokumen ini memberikan contoh nyata bagaimana cara berinteraksi dengan NanoPyBot, mulai dari chat biasa, memberikan instruksi belajar (self-learning), hingga menggunakan tools.

---

## 1. Chat Biasa & Pertanyaan Umum
Anda bisa bertanya apa saja layaknya asisten AI pada umumnya.

**Input:**
```bash
nanopy agent "Apa itu Bitcoin dalam 1 kalimat?"
```

**Output:**
> Bitcoin adalah mata uang digital terdesentralisasi berbasis teknologi blockchain yang memungkinkan transaksi peer-to-peer tanpa perantara otoritas pusat.

---

## 2. Mengajari Bot (Self-Learning)
Ingat, NanoPyBot akan menyimpan aturan jika Anda menggunakan kata kunci seperti **ingat**, **catat**, atau **jangan**.

**Input (Memberi Aturan):**
```bash
nanopy agent "Ingat, panggil saya 'Juragan' dan gunakan bahasa yang sangat sopan."
```

**Output:**
> Baik, Juragan. Perintah Anda telah saya catat. Mulai sekarang saya akan menyapa Anda dengan sebutan tersebut dan menggunakan bahasa yang sangat sopan. Ada yang bisa saya bantu, Juragan?

**Input Berikutnya (Mengetes Memori):**
```bash
nanopy agent "Bantu saya buatkan resep kopi susu."
```

**Output:**
> Tentu, Juragan. Dengan segala hormat, berikut adalah resep kopi susu yang nikmat untuk Anda sajikan...

---

## 3. Menggunakan Tools (Built-in & Custom)
Bot bisa diperintah untuk menggunakan fungsi teknis tertentu.

### Menebak Waktu
**Input:**
```bash
nanopy agent "tool:time {}"
```

### Mencari di Internet (Search Tool + Auto Summarize)
Bot bisa mencari informasi terbaru dan merangkumnya untuk Anda.

**Input:**
```bash
nanopy agent "Cari tahu berapa harga emas antam hari ini dan ringkas untuk saya."
```

**Output:**
> [Auto-exec] Calling search tool...
> Harga emas Antam hari ini, 8 Februari 2026, adalah Rp 2.920.000 per gram (harga dasar). Untuk pecahan 0.5 gram seharga Rp 1.510.000...

### Mengecek Cuaca (Weather Tool)
Bot bisa memberikan info cuaca lengkap beserta saran aktivitas.

**Input:**
```bash
nanopy agent "Bagaimana cuaca di Jakarta hari ini? Apakah cocok untuk lari sore?"
```

**Output:**
> [Auto-exec] Calling weather tool...
> Cuaca di Jakarta saat ini sebagian berawan dengan suhu 27°C. Karena kelembapan cukup tinggi (84%), jika ingin lari sore disarankan untuk membawa air minum tambahan agar tidak dehidrasi.

### Konversi Mata Uang (Currency Tool)
Bot bisa membantu menghitung nilai tukar mata uang terbaru.

**Input:**
```bash
nanopy agent "Berapa Rp 5.000.000 kalau diubah ke USD?"
```

**Output:**
> [Auto-exec] Calling currency tool...
> Rp 5.000.000 setara dengan sekitar 312,50 USD (berdasarkan nilai tukar saat ini).

---

## 4. Membuat Tool Baru Secara Dinamis
Anda bisa menyuruh bot untuk menambah kemampuannya sendiri.

**Input:**
```bash
nanopy agent "Buatkan tool bernama 'kalkulator_pajak' untuk menghitung PPN 11% dari sebuah angka."
```

**Output:**
> [Auto-exec] Tool 'kalkulator_pajak' added successfully.
> Saya telah membuatkan tool kalkulator pajak untuk Anda. Sekarang saya bisa membantu menghitung PPN secara otomatis.

---

## 5. Otomasi dengan Cron
Menjadwalkan bot untuk mengerjakan sesuatu secara rutin.

**Input (Menambah Jadwal):**
```bash
nanopy cron-add --name "salam-pagi" --message "Berikan kutipan motivasi pagi ini" --cron "0 7 * * *"
```

**Input (Menjalankan Runner):**
```bash
nanopy cron-run
```

---

## 💡 Tips Berinteraksi
- **Prefix `tool:`**: Gunakan ini jika Anda ingin memaksa bot menjalankan fungsi tertentu secara manual.
- **Konformitas**: Jika bot mulai lupa aturan, ingatkan kembali dengan kata "Ingat..." atau "Jangan lupa...".
- **Eksperimen**: Jangan ragu meminta bot membuat tool yang kompleks, selama logikanya bisa ditulis dalam Python.
