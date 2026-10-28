"""
test_urutkan_dan_ekspor.py
Unit tests untuk fitur urutkan buku dan ekspor data buku.
"""

import os
import unittest
from exceptions.custom_exceptions import DataKosongError
from services.ekspor import ekspor_ke_csv, ekspor_ke_json
from services.urutkan import urutkan_koleksi


class TestUrutkanDanEkspor(unittest.TestCase):
    def setUp(self):
        self.koleksi_dummy = [
            {
                "kode_buku": "BK001",
                "judul": "Belajar Python",
                "pengarang": "Budi",
                "genre": "Teknologi",
                "tahun_terbit": 2021,
                "status": "tersedia",
            },
            {
                "kode_buku": "BK002",
                "judul": "Algoritma Pemrograman",
                "pengarang": "Andi",
                "genre": "Teknologi",
                "tahun_terbit": 2019,
                "status": "dipinjam",
            },
            {
                "kode_buku": "BK003",
                "judul": "Cara Berpikir Kritis",
                "pengarang": "Citra",
                "genre": "Filsafat",
                "tahun_terbit": 2023,
                "status": "tersedia",
            },
        ]

    def test_urutkan_berdasarkan_judul_asc(self):
        hasil = urutkan_koleksi(self.koleksi_dummy, kunci="judul", menaik=True)
        self.assertEqual(hasil[0]["judul"], "Algoritma Pemrograman")
        self.assertEqual(hasil[1]["judul"], "Belajar Python")
        self.assertEqual(hasil[2]["judul"], "Cara Berpikir Kritis")

    def test_urutkan_berdasarkan_tahun_desc(self):
        hasil = urutkan_koleksi(self.koleksi_dummy, kunci="tahun_terbit", menaik=False)
        self.assertEqual(hasil[0]["tahun_terbit"], 2023)
        self.assertEqual(hasil[1]["tahun_terbit"], 2021)
        self.assertEqual(hasil[2]["tahun_terbit"], 2019)

    def test_urutkan_berdasarkan_pengarang(self):
        hasil = urutkan_koleksi(self.koleksi_dummy, kunci="pengarang", menaik=True)
        self.assertEqual(hasil[0]["pengarang"], "Andi")
        self.assertEqual(hasil[1]["pengarang"], "Budi")
        self.assertEqual(hasil[2]["pengarang"], "Citra")

    def test_urutkan_koleksi_kosong(self):
        hasil = urutkan_koleksi([])
        self.assertEqual(hasil, [])

    def test_ekspor_csv(self):
        nama_file = "test_output.csv"
        try:
            path = ekspor_ke_csv(self.koleksi_dummy, nama_file=nama_file)
            self.assertTrue(os.path.exists(path))
            with open(path, "r", encoding="utf-8") as f:
                konten = f.read()
                self.assertIn("BK001", konten)
                self.assertIn("Belajar Python", konten)
        finally:
            if os.path.exists(nama_file):
                os.remove(nama_file)

    def test_ekspor_json(self):
        nama_file = "test_output.json"
        try:
            path = ekspor_ke_json(self.koleksi_dummy, nama_file=nama_file)
            self.assertTrue(os.path.exists(path))
            with open(path, "r", encoding="utf-8") as f:
                konten = f.read()
                self.assertIn("Algoritma Pemrograman", konten)
        finally:
            if os.path.exists(nama_file):
                os.remove(nama_file)

    def test_ekspor_data_kosong_gagal(self):
        with self.assertRaises(DataKosongError):
            ekspor_ke_csv([], "empty.csv")
        with self.assertRaises(DataKosongError):
            ekspor_ke_json([], "empty.json")


if __name__ == "__main__":
    unittest.main()
