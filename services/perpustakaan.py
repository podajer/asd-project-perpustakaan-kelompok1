"""
perpustakaan.py (services)
Penyimpanan koleksi buku (Array of Struct) dan fungsi dasar yang dipakai semua fitur.

Berisi:
    - koleksi_buku: list of dict, penyimpanan utama (hanya di memori)
    - Fungsi bantu: cari_buku_by_kode, kode_sudah_ada, ambil_buku, konfirmasi_ya_tidak
    - Fitur 1: tambah_buku_baru (logika) dan tambah_buku (tampilan terminal)
    - muat_data_contoh (opsional, untuk demo dan screenshot)
"""

from exceptions.custom_exceptions import (
    BukuTidakDitemukanError,
    DataKosongError,
    KodeDuplikatError,
)
from models.buku import STATUS_DIPINJAM, STATUS_TERSEDIA, buat_buku
from services.storage import sinkronkan_koleksi

# Penting: list ini hanya boleh diubah isinya (append / remove), jangan
# di-assign ulang (koleksi_buku = ...), karena modul lain mengimpor list yang sama.
koleksi_buku = []


# ---------------------------------------------------------------------------
# Fungsi bantu
# ---------------------------------------------------------------------------
def cari_buku_by_kode(kode):
    """Mengembalikan dict buku dengan kode yang persis sama, atau None."""
    for buku in koleksi_buku:
        if buku["kode_buku"] == kode:
            return buku
    return None


def kode_sudah_ada(kode):
    """True jika kode_buku sudah dipakai buku lain di koleksi."""
    return cari_buku_by_kode(kode) is not None


def ambil_buku(kode):
    """
    Mengambil buku berdasarkan kode untuk fitur update dan hapus.
    Melempar DataKosongError jika kode kosong, BukuTidakDitemukanError jika tidak ada.
    """
    kode = kode.strip()
    if not kode:
        raise DataKosongError("kode buku")
    buku = cari_buku_by_kode(kode)
    if buku is None:
        raise BukuTidakDitemukanError("kode", kode)
    return buku


def konfirmasi_ya_tidak(pertanyaan):
    """
    Meminta konfirmasi (y/n) dari petugas. Mengulang sampai jawaban valid.
    Mengembalikan True untuk 'y', False untuk 'n'.
    """
    while True:
        jawaban = input(pertanyaan + " (y/n): ").strip().lower()
        if jawaban == "y":
            return True
        if jawaban == "n":
            return False
        print("Input tidak valid. Ketik 'y' untuk ya atau 'n' untuk tidak.")


# ---------------------------------------------------------------------------
# Fitur 1: Tambah Buku Baru
# ---------------------------------------------------------------------------
def tambah_buku_baru(kode, judul, pengarang, genre, teks_tahun):
    """
    Logika Fitur 1: memvalidasi data lalu menambahkan buku ke koleksi.
    Validasi: semua field tidak kosong, kode tidak duplikat, tahun valid.
    Mengembalikan dict buku yang ditambahkan; melempar exception jika tidak valid.
    """
    kode_bersih = kode.strip()
    if kode_bersih and kode_sudah_ada(kode_bersih):
        raise KodeDuplikatError(kode_bersih)

    buku_baru = buat_buku(kode, judul, pengarang, genre, teks_tahun)
    koleksi_buku.append(buku_baru)
    sinkronkan_koleksi(koleksi_buku)
    return buku_baru


def tambah_buku():
    """Tampilan terminal Fitur 1: meminta input satu per satu, lalu menambahkan buku."""
    print("\n=== TAMBAH BUKU BARU ===")
    kode = input("Kode buku    : ")
    judul = input("Judul        : ")
    pengarang = input("Pengarang    : ")
    genre = input("Genre        : ")
    teks_tahun = input("Tahun terbit : ")

    buku = tambah_buku_baru(kode, judul, pengarang, genre, teks_tahun)
    print(
        "Buku '{}' dengan kode {} berhasil ditambahkan ke koleksi.".format(
            buku["judul"], buku["kode_buku"]
        )
    )


# ---------------------------------------------------------------------------
# Data contoh (opsional, untuk demo dan screenshot laporan)
# ---------------------------------------------------------------------------
def muat_data_contoh(pesan=True):
    """Menambahkan beberapa buku contoh. Kode yang sudah ada dilewati."""
    contoh = [
        ("BK001", "Algoritma dan Pemrograman", "Rinaldi Munir", "Teknologi", "2020", STATUS_TERSEDIA),
        ("BK002", "Pengantar Algoritma", "Thomas H. Cormen", "Teknologi", "2009", STATUS_DIPINJAM),
        ("BK003", "Laskar Pelangi", "Andrea Hirata", "Fiksi", "2005", STATUS_TERSEDIA),
        ("BK004", "Bumi Manusia", "Pramoedya Ananta Toer", "Fiksi Sejarah", "1980", STATUS_TERSEDIA),
        ("BK005", "Sapiens", "Yuval Noah Harari", "Sejarah", "2011", STATUS_DIPINJAM),
        ("BK006", "Cosmos", "Carl Sagan", "Sains", "1980", STATUS_TERSEDIA),
        ("BK007", "Dilan 1990", "Pidi Baiq", "Fiksi Remaja", "2014", STATUS_TERSEDIA),
    ]
    ditambahkan = 0
    for kode, judul, pengarang, genre, tahun, status in contoh:
        if kode_sudah_ada(kode):
            continue
        buku = buat_buku(kode, judul, pengarang, genre, tahun)
        buku["status"] = status
        koleksi_buku.append(buku)
        ditambahkan += 1

    sinkronkan_koleksi(koleksi_buku)
    if pesan:
        print("{} buku contoh ditambahkan ke koleksi.".format(ditambahkan))
