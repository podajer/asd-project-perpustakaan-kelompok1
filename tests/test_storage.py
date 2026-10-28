"""
test_storage.py
Unit tests untuk modul storage persistensi data lokal.
"""

import os
import shutil
import unittest
from services.storage import (
    inisialisasi_data,
    muat_koleksi_dari_file,
    simpan_koleksi_ke_file,
    simpan_riwayat_ke_file,
    muat_riwayat_dari_file,
)


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_storage_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        self.file_buku = os.path.join(self.test_dir, "test_buku.json")
        self.file_riwayat = os.path.join(self.test_dir, "test_riwayat.json")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_simpan_dan_muat_buku(self):
        dummy_koleksi = [
            {"kode_buku": "BK999", "judul": "Testing Storage", "status": "Tersedia"}
        ]
        hasil_simpan = simpan_koleksi_ke_file(dummy_koleksi, berkas=self.file_buku)
        self.assertTrue(hasil_simpan)

        data_dimuat = muat_koleksi_dari_file(berkas=self.file_buku)
        self.assertIsNotNone(data_dimuat)
        self.assertEqual(len(data_dimuat), 1)
        self.assertEqual(data_dimuat[0]["kode_buku"], "BK999")

    def test_simpan_dan_muat_riwayat(self):
        dummy_riwayat = [
            {"kode_buku": "BK999", "judul": "Testing Storage", "aksi": "PINJAM"}
        ]
        hasil_simpan = simpan_riwayat_ke_file(dummy_riwayat, berkas=self.file_riwayat)
        self.assertTrue(hasil_simpan)

        riwayat_dimuat = muat_riwayat_dari_file(berkas=self.file_riwayat)
        self.assertIsNotNone(riwayat_dimuat)
        self.assertEqual(len(riwayat_dimuat), 1)
        self.assertEqual(riwayat_dimuat[0]["aksi"], "PINJAM")

    def test_muat_file_tidak_ada(self):
        hasil = muat_koleksi_dari_file("berkas_palsu.json")
        self.assertIsNone(hasil)


if __name__ == "__main__":
    unittest.main()
