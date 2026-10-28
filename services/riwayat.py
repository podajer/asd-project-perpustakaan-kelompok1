"""
riwayat.py (services)
Fitur Pencatatan dan Penampilan Riwayat Transaksi Perpustakaan.
Mencatat aktivitas peminjaman dan pengembalian buku serta menyimpannya ke storage lokal.
"""

from datetime import datetime
from exceptions.custom_exceptions import DataKosongError
from services.storage import sinkronkan_riwayat

# List of dict untuk menyimpan riwayat transaksi
riwayat_transaksi = []


def catat_transaksi(kode_buku, judul, aksi, peminjam="Umum"):
    """
    Mencatat log transaksi buku ke memori dan storage.
    :param kode_buku: Kode buku
    :param judul: Judul buku
    :param aksi: 'PINJAM' atau 'KEMBALI'
    :param peminjam: Nama peminjam / pihak terkait
    """
    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_item = {
        "waktu": waktu_sekarang,
        "kode_buku": kode_buku,
        "judul": judul,
        "aksi": aksi.upper(),
        "peminjam": peminjam,
    }
    riwayat_transaksi.append(log_item)
    sinkronkan_riwayat(riwayat_transaksi)
    return log_item


def bersihkan_riwayat():
    """Mengosongkan daftar riwayat transaksi (untuk testing)."""
    riwayat_transaksi.clear()


def tampilkan_riwayat_transaksi():
    """Menampilkan riwayat peminjaman dan pengembalian buku dalam bentuk tabel."""
    if not riwayat_transaksi:
        raise DataKosongError("Belum ada riwayat transaksi peminjaman/pengembalian buku.")

    print("\n=== RIWAYAT TRANSAKSI PERPUSTAKAAN ===")
    kolom = ["No", "Waktu", "Kode", "Judul Buku", "Aktivitas", "Peminjam"]
    baris = []
    for no, log in enumerate(riwayat_transaksi, start=1):
        baris.append([
            str(no),
            log["waktu"],
            log["kode_buku"],
            log["judul"],
            f"[{log['aksi']}]",
            log["peminjam"],
        ])

    lebar = [len(k) for k in kolom]
    for b in baris:
        for i, val in enumerate(b):
            lebar[i] = max(lebar[i], len(val))

    garis = "+" + "+".join("-" * (w + 2) for w in lebar) + "+"

    def format_baris(isi):
        return "| " + " | ".join(sel.ljust(lebar[i]) for i, sel in enumerate(isi)) + " |"

    print(garis)
    print(format_baris(kolom))
    print(garis)
    for b in baris:
        print(format_baris(b))
    print(garis)
