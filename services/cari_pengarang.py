"""
cari_pengarang.py (services)
Fitur tambahan: Cari Buku Berdasarkan Pengarang
(partial match, tidak case sensitive).
"""

from exceptions.custom_exceptions import BukuTidakDitemukanError, DataKosongError
from services.perpustakaan import koleksi_buku
from services.tampil import cetak_tabel


def cari_by_pengarang(kata_kunci):
    """
    Logika fitur: mengembalikan buku yang nama pengarangnya mengandung kata kunci.
    Melempar DataKosongError jika kata kunci kosong, BukuTidakDitemukanError jika tidak ada hasil.
    """
    kata_kunci = kata_kunci.strip()
    if not kata_kunci:
        raise DataKosongError("kata kunci")

    hasil = [
        buku for buku in koleksi_buku if kata_kunci.lower() in buku["pengarang"].lower()
    ]
    if not hasil:
        raise BukuTidakDitemukanError("pengarang", kata_kunci)
    return hasil


def cari_buku_pengarang():
    """Tampilan terminal: minta nama pengarang, tampilkan hasil dalam tabel."""
    print("\n=== CARI BUKU BERDASARKAN PENGARANG ===")
    hasil = cari_by_pengarang(input("Masukkan nama pengarang: "))
    print("Ditemukan {} buku.".format(len(hasil)))
    cetak_tabel(hasil)
