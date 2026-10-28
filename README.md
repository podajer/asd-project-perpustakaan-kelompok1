# Sistem Perpustakaan Mini - Kelompok 1

Project semester Algoritma dan Struktur Data, Program Studi Sistem Informasi FTI Universitas Merdeka Malang, 2026/2027.

**Dosen Pengampu:** Amadea Permana Sanusi, S.Tr.T., M.Tr.Kom

---

## 1. Anggota Kelompok
| No | Nama Lengkap | NIM | GitHub Username | Email |
|:--:|:-----------------------------|:-----------:|:-------------------:|:-------------------------------------:|
| 1  | M Affan Arriza Zamzami       | 25083000078 | `podajer`           | `octaarriza@gmail.com`                |
| 2  | Kinantara Ridho A.           | 25083000035 | `arsyllxd`          | `kinantara2005@gmail.com`             |
| 3  | Yehudha Muman                | 25083000058 | `yehudhamuman-hub`  | `shinryujin4646@gmail.com`            |
| 4  | Figo Alvaro                  | 25083000069 | `fgal-max`          | `25083000069@student.unmer.ac.id`     |
| 5  | Apriliano Steniluciano Nabat | 25083000067 | `aprilianonabat-bit`| `aprilianonabat@gmail.com`            |

---

## 2. Deskripsi Sistem
**Sistem Perpustakaan Mini** adalah aplikasi berbasis antarmuka baris perintah (CLI) yang dibangun dengan bahasa Python untuk mengelola koleksi buku perpustakaan secara interaktif. Sistem ini mengimplementasikan konsep struktur data **Array of Struct (list of dictionary)** dalam memori serta berbagai algoritma dasar seperti pencarian (linear search & filtering), pengurutan data (*sorting*), pengolahan data riwayat transaksi, dan ekspor data eksternal.

---

## 3. Fitur Utama
1. **Tambah Buku Baru**: Menambahkan buku baru ke koleksi dengan validasi data input.
2. **Tampilkan Semua Buku**: Menampilkan seluruh data dalam format tabel rapi.
3. **Cari Buku**: Mencari buku berdasarkan kode atau kata kunci pada judul.
4. **Update Status Buku**: Mengubah status ketersediaan buku (`Tersedia` / `Dipinjam`) dan otomatis mencatat ke log riwayat.
5. **Filter Buku Berdasarkan Genre**: Menyaring daftar buku sesuai genre tertentu.
6. **Hapus Buku**: Menghapus data buku tertentu berdasarkan kode.
7. **Edit Data Buku**: Mengubah informasi buku yang sudah ada.
8. **Daftar Buku Dipinjam**: Menampilkan buku-buku yang sedang berstatus dipinjam.
9. **Statistik Koleksi per Genre**: Ringkasan jumlah dan statistik buku per genre.
10. **Cari Berdasarkan Pengarang**: Menemukan buku karya penulis tertentu.
11. **Filter Rentang Tahun**: Menyaring buku berdasarkan rentang tahun publikasi.
12. **Hapus Semua Buku per Genre**: Menghapus seluruh buku dengan genre terpilih sekaligus.
13. **Urutkan Koleksi (Sorting)**: Mengurutkan buku berdasarkan judul, tahun terbit, atau pengarang secara menaik (*ascending*) atau menurun (*descending*).
14. **Ekspor Data (CSV / JSON)**: Mengekspor koleksi buku ke file `.csv` atau `.json` untuk kebutuhan backup dan integrasi.
15. **Riwayat Peminjaman & Pengembalian**: Menelusuri seluruh riwayat aktivitas transaksi buku dan nama peminjam.
16. **Muat Data Contoh**: Menyediakan sample data dummy untuk demonstrasi aplikasi.

---

## 4. Struktur Direktori Proyek
```text
asd-project-perpustakaan-kelompok1/
├── exceptions/
│   ├── __init__.py
│   └── custom_exceptions.py       # Custom exception handling
├── models/
│   ├── __init__.py
│   └── buku.py                    # Representasi struct data buku
├── services/
│   ├── __init__.py
│   ├── perpustakaan.py            # State koleksi buku & data contoh
│   ├── cari.py                    # Pencarian buku
│   ├── cari_pengarang.py          # Pencarian buku berdasar pengarang
│   ├── dipinjam.py                # Filter buku dipinjam
│   ├── edit.py                    # Edit data buku
│   ├── ekspor.py                  # Ekspor data CSV & JSON
│   ├── hapus.py                   # Hapus buku spesifik
│   ├── hapus_genre.py             # Hapus buku massal per genre
│   ├── rentang_tahun.py           # Filter buku rentang tahun
│   ├── riwayat.py                 # Log riwayat peminjaman/pengembalian
│   ├── statistik.py               # Statistik koleksi
│   ├── status.py                  # Update status pinjam/kembali
│   ├── tampil.py                  # Tampil tabel & filter genre
│   └── urutkan.py                 # Algoritma pengurutan (Sorting)
├── tests/
│   ├── __init__.py
│   ├── test_perpustakaan.py       # Unit tests fitur utama
│   ├── test_riwayat.py            # Unit tests riwayat transaksi
│   └── test_urutkan_dan_ekspor.py # Unit tests fitur sort & ekspor
├── main.py                        # File entry point program
├── README.md                      # Dokumentasi proyek
└── .gitignore                     # Konfigurasi pengabaian file Git
```

---

## 5. Cara Menjalankan Program
Pastikan Python 3.x telah terinstal di komputer Anda.

1. **Jalankan aplikasi utama:**
   ```bash
   python main.py
   ```
2. **Jalankan seluruh Unit Tests:**
   ```bash
   python -m unittest discover tests
   ```

---

## 6. Standar Branching Git (Git Flow)
- **`main`**: Branch rilis produksi yang stabil dan bersih.
- **`develop`**: Branch integrasi utama tempat penggabungan fitur sebelum dirilis ke `main`.
- **`feat/<nama-fitur>`**: Branch pengembangan fitur baru per anggota tim.
