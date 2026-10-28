"""
status.py (services)
Fitur 4: Update Status Buku (toggle otomatis Tersedia <-> Dipinjam).
Terintegrasi dengan pencatatan riwayat transaksi dan penyimpanan storage lokal.
"""

from models.buku import STATUS_DIPINJAM, STATUS_TERSEDIA
from services.perpustakaan import ambil_buku, konfirmasi_ya_tidak, koleksi_buku
from services.riwayat import catat_transaksi
from services.storage import sinkronkan_koleksi


def ubah_status(buku, peminjam="Umum"):
    """
    Logika Fitur 4: membalik status buku (Tersedia <-> Dipinjam).
    Mencatat aksi ke riwayat transaksi.
    Mengembalikan tuple (status_lama, status_baru).
    """
    status_lama = buku["status"]
    status_baru = STATUS_DIPINJAM if status_lama == STATUS_TERSEDIA else STATUS_TERSEDIA
    buku["status"] = status_baru

    aksi = "PINJAM" if status_baru == STATUS_DIPINJAM else "KEMBALI"
    catat_transaksi(buku["kode_buku"], buku["judul"], aksi, peminjam=peminjam)
    sinkronkan_koleksi(koleksi_buku)

    return status_lama, status_baru


def update_status_buku():
    """
    Tampilan terminal Fitur 4. Arah perubahan ditentukan otomatis dari status saat ini.
    Sebelum diubah, ditampilkan info buku dan diminta konfirmasi (y/n).
    """
    print("\n=== UPDATE STATUS BUKU ===")
    buku = ambil_buku(input("Masukkan kode buku: "))

    print("Judul          : {}".format(buku["judul"]))
    print("Pengarang      : {}".format(buku["pengarang"]))
    print("Status saat ini: {}".format(buku["status"]))

    status_tujuan = STATUS_DIPINJAM if buku["status"] == STATUS_TERSEDIA else STATUS_TERSEDIA
    if not konfirmasi_ya_tidak("Ubah status menjadi {}?".format(status_tujuan)):
        print("Perubahan status dibatalkan.")
        return

    peminjam = "Umum"
    if status_tujuan == STATUS_DIPINJAM:
        input_peminjam = input("Nama Peminjam (kosongkan jika 'Umum'): ").strip()
        if input_peminjam:
            peminjam = input_peminjam

    status_lama, status_baru = ubah_status(buku, peminjam=peminjam)
    kata_kerja = "dipinjam" if status_baru == STATUS_DIPINJAM else "dikembalikan"
    print(
        "Buku '{}' berhasil {}. Status diubah: {} menjadi {}.".format(
            buku["judul"], kata_kerja, status_lama, status_baru
        )
    )
