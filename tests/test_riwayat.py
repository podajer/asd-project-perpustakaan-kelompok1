"""
test_riwayat.py
Unit tests untuk fitur pencatatan dan penelusuran riwayat transaksi buku.
"""

import unittest
from exceptions.custom_exceptions import DataKosongError
from models.buku import STATUS_DIPINJAM, STATUS_TERSEDIA
from services.riwayat import bersihkan_riwayat, catat_transaksi, riwayat_transaksi
from services.status import ubah_status


class TestRiwayatTransaksi(unittest.TestCase):
    def setUp(self):
        bersihkan_riwayat()
        self.buku_dummy = {
            "kode_buku": "BK001",
            "judul": "Struktur Data",
            "pengarang": "Budi",
            "genre": "Komputer",
            "tahun_terbit": 2021,
            "status": STATUS_TERSEDIA,
        }

    def tearDown(self):
        bersihkan_riwayat()

    def test_catat_transaksi_manual(self):
        log = catat_transaksi("BK001", "Struktur Data", "PINJAM", "Budi Santoso")
        self.assertEqual(len(riwayat_transaksi), 1)
        self.assertEqual(log["kode_buku"], "BK001")
        self.assertEqual(log["aksi"], "PINJAM")
        self.assertEqual(log["peminjam"], "Budi Santoso")

    def test_ubah_status_otomatis_mencatat_log(self):
        # Saat dipinjam
        status_lama, status_baru = ubah_status(self.buku_dummy, peminjam="Ahmad")
        self.assertEqual(status_lama, STATUS_TERSEDIA)
        self.assertEqual(status_baru, STATUS_DIPINJAM)
        self.assertEqual(len(riwayat_transaksi), 1)
        self.assertEqual(riwayat_transaksi[0]["aksi"], "PINJAM")
        self.assertEqual(riwayat_transaksi[0]["peminjam"], "Ahmad")

        # Saat dikembalikan
        status_lama2, status_baru2 = ubah_status(self.buku_dummy)
        self.assertEqual(status_lama2, STATUS_DIPINJAM)
        self.assertEqual(status_baru2, STATUS_TERSEDIA)
        self.assertEqual(len(riwayat_transaksi), 2)
        self.assertEqual(riwayat_transaksi[1]["aksi"], "KEMBALI")


if __name__ == "__main__":
    unittest.main()
