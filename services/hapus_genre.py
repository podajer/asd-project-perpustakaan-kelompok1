"""
hapus_genre.py (services)
Fitur tambahan: Hapus Semua Buku Berdasarkan Genre.

Aturan keamanan (sejalan dengan Fitur 6):
    - Genre dicocokkan PERSIS (tidak case sensitive), bukan partial match,
      supaya tidak ada buku yang terhapus tanpa sengaja.
    - Buku berstatus Dipinjam tidak pernah dihapus (dilewati).
    - Daftar buku yang akan dihapus ditampilkan dulu, lalu wajib konfirmasi (y/n).
"""

from exceptions.custom_exceptions import BukuTidakDitemukanError, DataKosongError
from models.buku import STATUS_DIPINJAM
from services.hapus import hapus_dari_koleksi
from services.perpustakaan import koleksi_buku, konfirmasi_ya_tidak
from services.tampil import cetak_tabel


def pilah_buku_genre(genre):
    """
    Logika tahap pengecekan: memisahkan buku bergenre `genre` (cocok persis, tidak
    case sensitive) menjadi dua list: (bisa_dihapus, tertahan_dipinjam).
    Melempar DataKosongError jika genre kosong, BukuTidakDitemukanError jika tidak ada
    buku dengan genre tersebut.
    """
    genre = genre.strip()
    if not genre:
        raise DataKosongError("genre")

    sesuai = [buku for buku in koleksi_buku if buku["genre"].lower() == genre.lower()]
    if not sesuai:
        raise BukuTidakDitemukanError("genre", genre)

    bisa_dihapus = [buku for buku in sesuai if buku["status"] != STATUS_DIPINJAM]
    tertahan = [buku for buku in sesuai if buku["status"] == STATUS_DIPINJAM]
    return bisa_dihapus, tertahan


def hapus_banyak(daftar_buku):
    """Logika tahap penghapusan: membuang semua buku di daftar. Mengembalikan jumlah terhapus."""
    for buku in list(daftar_buku):  # salin list agar aman saat koleksi berubah
        hapus_dari_koleksi(buku)
    return len(daftar_buku)


def hapus_buku_per_genre():
    """Tampilan terminal: cek -> tampilkan daftar -> konfirmasi (y/n) -> hapus."""
    print("\n=== HAPUS SEMUA BUKU BERDASARKAN GENRE ===")
    genre = input("Masukkan genre (harus persis): ").strip()
    bisa_dihapus, tertahan = pilah_buku_genre(genre)

    if tertahan:
        print(
            "{} buku bergenre '{}' sedang Dipinjam dan tidak akan dihapus.".format(
                len(tertahan), genre
            )
        )
    if not bisa_dihapus:
        print("Tidak ada buku bergenre '{}' yang dapat dihapus saat ini.".format(genre))
        return

    print("Buku yang akan dihapus ({} buku):".format(len(bisa_dihapus)))
    cetak_tabel(bisa_dihapus)

    if not konfirmasi_ya_tidak("Yakin ingin menghapus {} buku di atas?".format(len(bisa_dihapus))):
        print("Penghapusan dibatalkan.")
        return

    jumlah = hapus_banyak(bisa_dihapus)
    print("{} buku bergenre '{}' berhasil dihapus dari koleksi.".format(jumlah, genre))
