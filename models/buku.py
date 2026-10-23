"""
buku.py (models)
Definisi struct Buku: konstanta status, validasi atribut, dan pembuatan data buku.

Satu buku direpresentasikan sebagai dict (struct) dengan 6 atribut wajib:
kode_buku, judul, pengarang, genre, tahun_terbit, status.
Kumpulan buku disimpan dalam list (array) di services/perpustakaan.py.
"""

from datetime import datetime

from exceptions.custom_exceptions import DataKosongError, TahunTidakValidError

STATUS_TERSEDIA = "Tersedia"
STATUS_DIPINJAM = "Dipinjam"


def validasi_tahun(teks_tahun):
    """
    Memeriksa tahun terbit dan mengembalikannya sebagai int.
    Aturan: tidak kosong, angka bulat positif, tidak lebih besar dari tahun sekarang.
    Melempar DataKosongError atau TahunTidakValidError jika tidak valid.
    """
    teks_tahun = teks_tahun.strip()
    if not teks_tahun:
        raise DataKosongError("tahun terbit")
    # isascii() + isdigit() menolak huruf, tanda minus/plus, desimal, dan spasi.
    if not (teks_tahun.isascii() and teks_tahun.isdigit()):
        raise TahunTidakValidError("tahun terbit harus berupa angka bulat positif.")
    tahun = int(teks_tahun)
    if tahun <= 0:
        raise TahunTidakValidError("tahun terbit harus berupa angka bulat positif.")
    tahun_sekarang = datetime.now().year
    if tahun > tahun_sekarang:
        raise TahunTidakValidError(
            "tahun terbit tidak boleh lebih besar dari tahun sekarang ({}).".format(
                tahun_sekarang
            )
        )
    return tahun


def buat_buku(kode, judul, pengarang, genre, teks_tahun):
    """
    Membuat dict buku baru setelah semua atribut divalidasi.
    Status awal selalu "Tersedia". Melempar exception jika ada atribut yang tidak valid.
    """
    kode = kode.strip()
    judul = judul.strip()
    pengarang = pengarang.strip()
    genre = genre.strip()

    if not kode:
        raise DataKosongError("kode buku")
    if not judul:
        raise DataKosongError("judul")
    if not pengarang:
        raise DataKosongError("pengarang")
    if not genre:
        raise DataKosongError("genre")
    tahun = validasi_tahun(teks_tahun)

    return {
        "kode_buku": kode,
        "judul": judul,
        "pengarang": pengarang,
        "genre": genre,
        "tahun_terbit": tahun,
        "status": STATUS_TERSEDIA,
    }
