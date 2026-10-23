"""
custom_exceptions.py
Exception khusus Sistem Perpustakaan Mini.

Semua kesalahan yang bisa diperkirakan (input kosong, kode duplikat, buku tidak
ditemukan, dst.) dilempar sebagai exception di bawah ini, lalu ditangkap di
main.py dan ditampilkan sebagai pesan ke petugas. Teks pesan sudah mengikuti
format di brief, sehingga cukup dicetak apa adanya.
"""


class PerpustakaanError(Exception):
    """Kelas dasar semua exception di sistem perpustakaan."""


class DataKosongError(PerpustakaanError):
    """Dilempar saat sebuah input wajib diisi, tetapi dikosongkan."""

    def __init__(self, nama_field):
        self.nama_field = nama_field
        super().__init__("Gagal: {} tidak boleh kosong.".format(nama_field))


class KodeDuplikatError(PerpustakaanError):
    """Dilempar saat kode_buku yang ditambahkan sudah dipakai buku lain."""

    def __init__(self, kode):
        self.kode = kode
        super().__init__(
            "Gagal: kode buku '{}' sudah digunakan. Gunakan kode lain.".format(kode)
        )


class TahunTidakValidError(PerpustakaanError):
    """Dilempar saat tahun_terbit bukan angka bulat positif atau melebihi tahun sekarang."""

    def __init__(self, alasan):
        super().__init__("Gagal: " + alasan)


class InputTidakValidError(PerpustakaanError):
    """Dilempar saat pilihan/input petugas tidak dikenali (misal mode pencarian salah)."""

    def __init__(self, alasan):
        super().__init__("Gagal: " + alasan)


class BukuTidakDitemukanError(PerpustakaanError):
    """Dilempar saat buku dengan kode/judul yang dicari tidak ada di koleksi."""

    def __init__(self, jenis, kata_kunci):
        self.jenis = jenis
        self.kata_kunci = kata_kunci
        super().__init__(
            "Buku dengan {} '{}' tidak ditemukan dalam koleksi.".format(jenis, kata_kunci)
        )


class BukuSedangDipinjamError(PerpustakaanError):
    """Dilempar saat petugas mencoba menghapus buku yang berstatus Dipinjam."""

    def __init__(self, judul):
        self.judul = judul
        super().__init__(
            "Buku '{}' tidak dapat dihapus karena sedang dalam status Dipinjam. "
            "Pastikan buku dikembalikan terlebih dahulu sebelum dihapus dari koleksi.".format(
                judul
            )
        )
