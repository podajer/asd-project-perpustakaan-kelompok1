"""
dipinjam.py (services)
Fitur tambahan: Daftar Buku yang Sedang Dipinjam.
"""

from models.buku import STATUS_DIPINJAM
from services.perpustakaan import koleksi_buku
from services.tampil import cetak_tabel


def daftar_buku_dipinjam():
    """Logika fitur: mengembalikan list buku yang berstatus Dipinjam."""
    return [buku for buku in koleksi_buku if buku["status"] == STATUS_DIPINJAM]


def tampilkan_buku_dipinjam():
    """Tampilan terminal: tabel buku yang sedang dipinjam beserta jumlahnya."""
    print("\n=== DAFTAR BUKU YANG SEDANG DIPINJAM ===")
    hasil = daftar_buku_dipinjam()
    if not hasil:
        print("Tidak ada buku yang sedang dipinjam.")
        return

    cetak_tabel(hasil)
    print("Jumlah buku dipinjam: {}".format(len(hasil)))
