"""
edit.py (services)
Fitur tambahan: Edit Data Buku (judul, pengarang, genre, tahun terbit).
Kode buku dan status tidak bisa diubah lewat fitur ini.
"""

from models.buku import validasi_tahun
from services.perpustakaan import ambil_buku


def ubah_data_buku(buku, judul_baru, pengarang_baru, genre_baru, tahun_baru):
    """
    Logika fitur edit. Isian kosong berarti "tidak diubah".
    Semua isian divalidasi lebih dulu; jika ada yang tidak valid, tidak ada
    yang diubah (TahunTidakValidError dilempar).
    Mengembalikan list nama atribut yang benar-benar berubah.
    """
    judul_baru = judul_baru.strip()
    pengarang_baru = pengarang_baru.strip()
    genre_baru = genre_baru.strip()
    tahun_baru = tahun_baru.strip()

    perubahan = {}
    if judul_baru:
        perubahan["judul"] = judul_baru
    if pengarang_baru:
        perubahan["pengarang"] = pengarang_baru
    if genre_baru:
        perubahan["genre"] = genre_baru
    if tahun_baru:
        perubahan["tahun_terbit"] = validasi_tahun(tahun_baru)  # validasi sebelum menyimpan

    atribut_berubah = []
    for atribut, nilai in perubahan.items():
        if buku[atribut] != nilai:
            buku[atribut] = nilai
            atribut_berubah.append(atribut)
    return atribut_berubah


def edit_buku():
    """Tampilan terminal fitur edit: tampilkan data saat ini, lalu minta nilai baru."""
    print("\n=== EDIT DATA BUKU ===")
    buku = ambil_buku(input("Masukkan kode buku yang akan diedit: "))

    print("Data saat ini (kosongkan isian dengan Enter jika tidak ingin mengubah):")
    judul_baru = input("Judul [{}]: ".format(buku["judul"]))
    pengarang_baru = input("Pengarang [{}]: ".format(buku["pengarang"]))
    genre_baru = input("Genre [{}]: ".format(buku["genre"]))
    tahun_baru = input("Tahun terbit [{}]: ".format(buku["tahun_terbit"]))

    atribut_berubah = ubah_data_buku(buku, judul_baru, pengarang_baru, genre_baru, tahun_baru)
    if not atribut_berubah:
        print("Tidak ada perubahan data.")
        return
    print(
        "Data buku '{}' dengan kode {} berhasil diperbarui ({}).".format(
            buku["judul"], buku["kode_buku"], ", ".join(atribut_berubah)
        )
    )
