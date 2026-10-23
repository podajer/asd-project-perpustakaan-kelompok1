"""
hapus.py (services)
Fitur 6: Hapus Buku (tidak boleh jika berstatus Dipinjam, wajib konfirmasi).
"""

from exceptions.custom_exceptions import BukuSedangDipinjamError
from models.buku import STATUS_DIPINJAM
from services.perpustakaan import ambil_buku, konfirmasi_ya_tidak, koleksi_buku


def ambil_buku_untuk_dihapus(kode):
    """
    Logika Fitur 6 (tahap pengecekan): memastikan buku boleh dihapus.
    Melempar DataKosongError, BukuTidakDitemukanError, atau BukuSedangDipinjamError.
    Pengecekan status dilakukan sebelum konfirmasi ditampilkan.
    """
    buku = ambil_buku(kode)
    if buku["status"] == STATUS_DIPINJAM:
        raise BukuSedangDipinjamError(buku["judul"])
    return buku


def hapus_dari_koleksi(buku):
    """Logika Fitur 6 (tahap penghapusan): membuang buku dari koleksi."""
    koleksi_buku.remove(buku)


def hapus_buku():
    """Tampilan terminal Fitur 6: cek -> tampilkan detail -> konfirmasi (y/n) -> hapus."""
    print("\n=== HAPUS BUKU ===")
    buku = ambil_buku_untuk_dihapus(input("Masukkan kode buku yang akan dihapus: "))

    print("Judul     : {}".format(buku["judul"]))
    print("Pengarang : {}".format(buku["pengarang"]))
    print("Genre     : {}".format(buku["genre"]))
    print("Status    : {}".format(buku["status"]))

    if not konfirmasi_ya_tidak("Yakin ingin menghapus buku ini?"):
        print("Penghapusan dibatalkan.")
        return

    hapus_dari_koleksi(buku)
    print(
        "Buku '{}' dengan kode {} berhasil dihapus dari koleksi.".format(
            buku["judul"], buku["kode_buku"]
        )
    )
