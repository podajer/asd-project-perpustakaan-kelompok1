"""
rentang_tahun.py (services)
Fitur tambahan: Filter Buku Berdasarkan Rentang Tahun Terbit
(tahun awal sampai tahun akhir, keduanya termasuk).
"""

from exceptions.custom_exceptions import InputTidakValidError
from models.buku import validasi_tahun
from services.perpustakaan import koleksi_buku
from services.tampil import cetak_tabel


def filter_by_rentang_tahun(teks_awal, teks_akhir):
    """
    Logika fitur: mengembalikan (tahun_awal, tahun_akhir, daftar_buku).
    Kedua tahun divalidasi seperti tahun terbit buku (angka bulat positif, tidak melebihi
    tahun sekarang). Melempar InputTidakValidError jika tahun awal > tahun akhir.
    """
    tahun_awal = validasi_tahun(teks_awal)
    tahun_akhir = validasi_tahun(teks_akhir)
    if tahun_awal > tahun_akhir:
        raise InputTidakValidError("tahun awal tidak boleh lebih besar dari tahun akhir.")

    hasil = [buku for buku in koleksi_buku if tahun_awal <= buku["tahun_terbit"] <= tahun_akhir]
    return tahun_awal, tahun_akhir, hasil


def filter_rentang_tahun():
    """Tampilan terminal: minta tahun awal dan akhir, tampilkan buku yang terbit di antaranya."""
    print("\n=== FILTER BUKU BERDASARKAN RENTANG TAHUN TERBIT ===")
    teks_awal = input("Tahun awal  : ")
    teks_akhir = input("Tahun akhir : ")
    tahun_awal, tahun_akhir, hasil = filter_by_rentang_tahun(teks_awal, teks_akhir)

    if not hasil:
        print("Tidak ada buku yang terbit antara tahun {} dan {}.".format(tahun_awal, tahun_akhir))
        return

    print(
        "Menampilkan buku terbit {} sampai {} ({} buku ditemukan).".format(
            tahun_awal, tahun_akhir, len(hasil)
        )
    )
    cetak_tabel(hasil)
