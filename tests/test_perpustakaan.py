"""
test_perpustakaan.py
Unit test untuk logika 6 fitur Tahap 1.

Jalankan dari folder utama project:
    python -m unittest discover -s tests -v
"""

import os
import sys
import unittest
from datetime import datetime

# Agar `import models...` dan `import services...` berjalan dari folder tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from exceptions.custom_exceptions import (  # noqa: E402
    BukuSedangDipinjamError,
    BukuTidakDitemukanError,
    DataKosongError,
    InputTidakValidError,
    KodeDuplikatError,
    TahunTidakValidError,
)
from models.buku import STATUS_DIPINJAM, STATUS_TERSEDIA, buat_buku, validasi_tahun  # noqa: E402
from services import perpustakaan  # noqa: E402
from services.cari import cari  # noqa: E402
from services.dipinjam import daftar_buku_dipinjam  # noqa: E402
from services.cari_pengarang import cari_by_pengarang  # noqa: E402
from services.edit import ubah_data_buku  # noqa: E402
from services.rentang_tahun import filter_by_rentang_tahun  # noqa: E402
from services.statistik import hitung_statistik_genre  # noqa: E402
from services.hapus import ambil_buku_untuk_dihapus, hapus_dari_koleksi  # noqa: E402
from services.hapus_genre import hapus_banyak, pilah_buku_genre  # noqa: E402
from services.perpustakaan import ambil_buku, koleksi_buku, tambah_buku_baru  # noqa: E402
from services.status import ubah_status  # noqa: E402
from services.tampil import filter_by_genre, hitung_ringkasan  # noqa: E402


class DasarTest(unittest.TestCase):
    """Mengosongkan koleksi sebelum setiap test supaya test saling independen."""

    def setUp(self):
        koleksi_buku.clear()

    def isi_contoh(self):
        tambah_buku_baru("BK001", "Algoritma dan Pemrograman", "Rinaldi Munir", "Teknologi", "2020")
        tambah_buku_baru("BK002", "Pengantar Algoritma", "Cormen", "Teknologi", "2009")
        tambah_buku_baru("BK003", "Laskar Pelangi", "Andrea Hirata", "Fiksi", "2005")
        tambah_buku_baru("BK004", "Ilmu Antariksa", "Carl Sagan", "Fiksi Ilmiah", "1980")


class TestModelBuku(unittest.TestCase):
    def test_buat_buku_status_awal_tersedia(self):
        buku = buat_buku("BK001", "Judul", "Penulis", "Genre", "2020")
        self.assertEqual(buku["status"], STATUS_TERSEDIA)
        self.assertEqual(buku["tahun_terbit"], 2020)
        self.assertEqual(
            sorted(buku), sorted(["kode_buku", "judul", "pengarang", "genre", "tahun_terbit", "status"])
        )

    def test_buat_buku_membersihkan_spasi(self):
        buku = buat_buku("  BK1 ", " J ", " P ", " G ", " 2020 ")
        self.assertEqual(buku["kode_buku"], "BK1")
        self.assertEqual(buku["judul"], "J")

    def test_field_kosong_ditolak(self):
        for argumen in [
            ("", "J", "P", "G", "2020"),
            ("K", "  ", "P", "G", "2020"),
            ("K", "J", "", "G", "2020"),
            ("K", "J", "P", "", "2020"),
            ("K", "J", "P", "G", ""),
        ]:
            with self.assertRaises(DataKosongError):
                buat_buku(*argumen)

    def test_tahun_tidak_valid(self):
        for teks in ["abc", "-5", "0", "3.5", "20 20", "+2020", "1_000", "٢٠٢٠"]:
            with self.assertRaises(TahunTidakValidError, msg=teks):
                validasi_tahun(teks)

    def test_tahun_tidak_boleh_melebihi_tahun_sekarang(self):
        sekarang = datetime.now().year
        self.assertEqual(validasi_tahun(str(sekarang)), sekarang)
        with self.assertRaises(TahunTidakValidError):
            validasi_tahun(str(sekarang + 1))


class TestF1TambahBuku(DasarTest):
    def test_tambah_sukses(self):
        buku = tambah_buku_baru("BK001", "Judul", "Penulis", "Genre", "2020")
        self.assertEqual(len(koleksi_buku), 1)
        self.assertIs(koleksi_buku[0], buku)

    def test_kode_duplikat_ditolak(self):
        tambah_buku_baru("BK001", "Judul", "Penulis", "Genre", "2020")
        with self.assertRaises(KodeDuplikatError):
            tambah_buku_baru("BK001", "Lain", "Lain", "Lain", "2021")
        self.assertEqual(len(koleksi_buku), 1)

    def test_gagal_tidak_menambah_data(self):
        with self.assertRaises(TahunTidakValidError):
            tambah_buku_baru("BK001", "J", "P", "G", "abc")
        self.assertEqual(len(koleksi_buku), 0)


class TestF2Ringkasan(DasarTest):
    def test_ringkasan(self):
        self.isi_contoh()
        koleksi_buku[0]["status"] = STATUS_DIPINJAM
        self.assertEqual(hitung_ringkasan(), (4, 3, 1))

    def test_ringkasan_kosong(self):
        self.assertEqual(hitung_ringkasan(), (0, 0, 0))


class TestF3Cari(DasarTest):
    def setUp(self):
        super().setUp()
        self.isi_contoh()

    def test_kode_exact_match(self):
        hasil = cari("kode", "BK003")
        self.assertEqual([b["judul"] for b in hasil], ["Laskar Pelangi"])

    def test_kode_tidak_boleh_sebagian_atau_beda_huruf(self):
        for kata in ["BK00", "bk003"]:
            with self.assertRaises(BukuTidakDitemukanError):
                cari("kode", kata)

    def test_judul_partial_tidak_case_sensitive(self):
        hasil = cari("judul", "ALGORITMA")
        self.assertEqual(len(hasil), 2)

    def test_tidak_ditemukan(self):
        with self.assertRaises(BukuTidakDitemukanError) as konteks:
            cari("judul", "tidak ada")
        self.assertEqual(
            str(konteks.exception),
            "Buku dengan judul 'tidak ada' tidak ditemukan dalam koleksi.",
        )

    def test_kata_kunci_kosong(self):
        with self.assertRaises(DataKosongError):
            cari("judul", "   ")

    def test_jenis_tidak_valid(self):
        with self.assertRaises(InputTidakValidError):
            cari("pengarang", "x")


class TestF4Status(DasarTest):
    def test_toggle_dua_arah(self):
        self.isi_contoh()
        buku = ambil_buku("BK001")
        self.assertEqual(ubah_status(buku), (STATUS_TERSEDIA, STATUS_DIPINJAM))
        self.assertEqual(buku["status"], STATUS_DIPINJAM)
        self.assertEqual(ubah_status(buku), (STATUS_DIPINJAM, STATUS_TERSEDIA))

    def test_kode_tidak_ditemukan(self):
        with self.assertRaises(BukuTidakDitemukanError):
            ambil_buku("NOPE")

    def test_kode_kosong(self):
        with self.assertRaises(DataKosongError):
            ambil_buku("")


class TestF5Genre(DasarTest):
    def setUp(self):
        super().setUp()
        self.isi_contoh()

    def test_partial_match_dan_tidak_case_sensitive(self):
        hasil = filter_by_genre("FIKSI")
        self.assertEqual(sorted(b["kode_buku"] for b in hasil), ["BK003", "BK004"])

    def test_tidak_ada_hasil_mengembalikan_list_kosong(self):
        self.assertEqual(filter_by_genre("xyz"), [])

    def test_genre_kosong(self):
        with self.assertRaises(DataKosongError):
            filter_by_genre("")


class TestF6Hapus(DasarTest):
    def setUp(self):
        super().setUp()
        self.isi_contoh()

    def test_hapus_sukses(self):
        buku = ambil_buku_untuk_dihapus("BK001")
        hapus_dari_koleksi(buku)
        self.assertEqual(len(koleksi_buku), 3)
        self.assertIsNone(perpustakaan.cari_buku_by_kode("BK001"))

    def test_buku_dipinjam_tidak_boleh_dihapus(self):
        ambil_buku("BK002")["status"] = STATUS_DIPINJAM
        with self.assertRaises(BukuSedangDipinjamError):
            ambil_buku_untuk_dihapus("BK002")
        self.assertEqual(len(koleksi_buku), 4)

    def test_kode_tidak_ditemukan(self):
        with self.assertRaises(BukuTidakDitemukanError):
            ambil_buku_untuk_dihapus("NOPE")


class TestEditBuku(DasarTest):
    def setUp(self):
        super().setUp()
        self.isi_contoh()
        self.buku = ambil_buku("BK001")

    def test_ubah_sebagian_atribut(self):
        berubah = ubah_data_buku(self.buku, "Judul Baru", "", "", "2022")
        self.assertEqual(berubah, ["judul", "tahun_terbit"])
        self.assertEqual(self.buku["judul"], "Judul Baru")
        self.assertEqual(self.buku["tahun_terbit"], 2022)
        self.assertEqual(self.buku["pengarang"], "Rinaldi Munir")  # tidak berubah

    def test_semua_kosong_tidak_ada_perubahan(self):
        self.assertEqual(ubah_data_buku(self.buku, "", " ", "", ""), [])

    def test_nilai_sama_tidak_dihitung_berubah(self):
        self.assertEqual(ubah_data_buku(self.buku, "Algoritma dan Pemrograman", "", "", ""), [])

    def test_tahun_tidak_valid_membatalkan_semua_perubahan(self):
        with self.assertRaises(TahunTidakValidError):
            ubah_data_buku(self.buku, "Judul Baru", "Penulis Baru", "Genre Baru", "abc")
        self.assertEqual(self.buku["judul"], "Algoritma dan Pemrograman")
        self.assertEqual(self.buku["pengarang"], "Rinaldi Munir")

    def test_kode_dan_status_tidak_berubah(self):
        ubah_data_buku(self.buku, "J", "P", "G", "2000")
        self.assertEqual(self.buku["kode_buku"], "BK001")
        self.assertEqual(self.buku["status"], STATUS_TERSEDIA)


class TestDaftarDipinjam(DasarTest):
    def test_hanya_buku_dipinjam(self):
        self.isi_contoh()
        self.assertEqual(daftar_buku_dipinjam(), [])
        ambil_buku("BK002")["status"] = STATUS_DIPINJAM
        ambil_buku("BK004")["status"] = STATUS_DIPINJAM
        self.assertEqual([b["kode_buku"] for b in daftar_buku_dipinjam()], ["BK002", "BK004"])


class TestStatistikGenre(DasarTest):
    def test_kosong(self):
        self.assertEqual(hitung_statistik_genre(), [])

    def test_pengelompokan_tidak_case_sensitive(self):
        self.isi_contoh()
        tambah_buku_baru("BK005", "Buku Lain", "X", "teknologi", "2010")  # huruf kecil
        ambil_buku("BK002")["status"] = STATUS_DIPINJAM
        hasil = {d["genre"]: d for d in hitung_statistik_genre()}
        self.assertEqual(len(hasil), 3)  # Teknologi, Fiksi, Fiksi Ilmiah
        self.assertEqual(hasil["Teknologi"]["total"], 3)
        self.assertEqual(hasil["Teknologi"]["dipinjam"], 1)
        self.assertEqual(hasil["Teknologi"]["tersedia"], 2)
        self.assertEqual(hasil["Fiksi"]["total"], 1)  # "Fiksi Ilmiah" genre terpisah


class TestCariPengarang(DasarTest):
    def setUp(self):
        super().setUp()
        self.isi_contoh()

    def test_partial_tidak_case_sensitive(self):
        self.assertEqual([b["kode_buku"] for b in cari_by_pengarang("SAGAN")], ["BK004"])
        self.assertEqual(len(cari_by_pengarang("an")), 2)  # Andrea Hirata, Carl Sagan

    def test_tidak_ditemukan(self):
        with self.assertRaises(BukuTidakDitemukanError):
            cari_by_pengarang("tidak ada")

    def test_kosong(self):
        with self.assertRaises(DataKosongError):
            cari_by_pengarang("  ")


class TestRentangTahun(DasarTest):
    def setUp(self):
        super().setUp()
        self.isi_contoh()  # 2020, 2009, 2005, 1980

    def test_batas_termasuk(self):
        awal, akhir, hasil = filter_by_rentang_tahun("2005", "2009")
        self.assertEqual((awal, akhir), (2005, 2009))
        self.assertEqual(sorted(b["kode_buku"] for b in hasil), ["BK002", "BK003"])

    def test_tidak_ada_hasil(self):
        self.assertEqual(filter_by_rentang_tahun("1990", "2000")[2], [])

    def test_awal_lebih_besar_ditolak(self):
        with self.assertRaises(InputTidakValidError):
            filter_by_rentang_tahun("2020", "2000")

    def test_tahun_tidak_valid(self):
        with self.assertRaises(TahunTidakValidError):
            filter_by_rentang_tahun("abc", "2000")
        with self.assertRaises(DataKosongError):
            filter_by_rentang_tahun("2000", "")


class TestHapusPerGenre(DasarTest):
    def setUp(self):
        super().setUp()
        self.isi_contoh()  # Teknologi x2, Fiksi x1, Fiksi Ilmiah x1

    def test_pencocokan_persis_bukan_partial(self):
        bisa, tertahan = pilah_buku_genre("fiksi")  # tidak boleh ikut "Fiksi Ilmiah"
        self.assertEqual([b["kode_buku"] for b in bisa], ["BK003"])
        self.assertEqual(tertahan, [])

    def test_buku_dipinjam_dilewati(self):
        ambil_buku("BK002")["status"] = STATUS_DIPINJAM
        bisa, tertahan = pilah_buku_genre("TEKNOLOGI")
        self.assertEqual([b["kode_buku"] for b in bisa], ["BK001"])
        self.assertEqual([b["kode_buku"] for b in tertahan], ["BK002"])

    def test_hapus_banyak_hanya_yang_dipilih(self):
        ambil_buku("BK002")["status"] = STATUS_DIPINJAM
        bisa, _ = pilah_buku_genre("Teknologi")
        self.assertEqual(hapus_banyak(bisa), 1)
        self.assertEqual(sorted(b["kode_buku"] for b in koleksi_buku), ["BK002", "BK003", "BK004"])

    def test_hapus_semua_buku_satu_genre(self):
        bisa, _ = pilah_buku_genre("Teknologi")
        self.assertEqual(hapus_banyak(bisa), 2)
        self.assertEqual(len(koleksi_buku), 2)

    def test_genre_kosong_dan_tidak_ada(self):
        with self.assertRaises(DataKosongError):
            pilah_buku_genre(" ")
        with self.assertRaises(BukuTidakDitemukanError):
            pilah_buku_genre("Komik")


if __name__ == "__main__":
    unittest.main()
