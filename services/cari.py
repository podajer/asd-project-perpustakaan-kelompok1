"""
cari.py (services)
Fitur 3: Cari Buku berdasarkan kode (exact match) atau judul (partial match,
tidak case sensitive).
"""

from exceptions.custom_exceptions import (
    BukuTidakDitemukanError,
    DataKosongError,
    InputTidakValidError,
)
from services.perpustakaan import cari_buku_by_kode, koleksi_buku
from services.tampil import cetak_tabel


def cari_by_kode(kode):
    """Pencarian kode: harus persis sama, mengembalikan list berisi 0 atau 1 buku."""
    buku = cari_buku_by_kode(kode)
    return [buku] if buku is not None else []


def cari_by_judul(kata_kunci):
    """Pencarian judul: kata kunci cukup ada di dalam judul, tidak case sensitive."""
    return [buku for buku in koleksi_buku if kata_kunci.lower() in buku["judul"].lower()]


def cari(jenis, kata_kunci):
    """
    Logika Fitur 3. jenis adalah "kode" atau "judul".
    Mengembalikan list hasil (tidak pernah kosong).
    Melempar DataKosongError (kata kunci kosong), InputTidakValidError (jenis salah),
    atau BukuTidakDitemukanError (tidak ada yang cocok).
    """
    kata_kunci = kata_kunci.strip()
    if not kata_kunci:
        raise DataKosongError("kata kunci")

    if jenis == "kode":
        hasil = cari_by_kode(kata_kunci)
    elif jenis == "judul":
        hasil = cari_by_judul(kata_kunci)
    else:
        raise InputTidakValidError("mode pencarian tidak valid. Pilih 1 atau 2.")

    if not hasil:
        raise BukuTidakDitemukanError(jenis, kata_kunci)
    return hasil


def cari_buku():
    """Tampilan terminal Fitur 3: pilih mode (kode / judul), isi kata kunci, tampilkan hasil."""
    print("\n=== CARI BUKU ===")
    print("1. Cari berdasarkan kode")
    print("2. Cari berdasarkan judul")
    mode = input("Pilih mode pencarian (1/2): ").strip()

    if mode == "1":
        jenis = "kode"
    elif mode == "2":
        jenis = "judul"
    else:
        raise InputTidakValidError("mode pencarian tidak valid. Pilih 1 atau 2.")

    kata_kunci = input("Masukkan {} buku: ".format(jenis))
    hasil = cari(jenis, kata_kunci)

    print("Ditemukan {} buku.".format(len(hasil)))
    cetak_tabel(hasil)
    if jenis == "kode":
        # Pencarian kode: tampilkan juga detail lengkap satu buku
        buku = hasil[0]
        print("Detail buku:")
        print("  Kode buku    : {}".format(buku["kode_buku"]))
        print("  Judul        : {}".format(buku["judul"]))
        print("  Pengarang    : {}".format(buku["pengarang"]))
        print("  Genre        : {}".format(buku["genre"]))
        print("  Tahun terbit : {}".format(buku["tahun_terbit"]))
        print("  Status       : {}".format(buku["status"]))
