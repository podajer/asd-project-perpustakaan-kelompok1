"""
main.py
Entry point Sistem Perpustakaan Mini (Tahap 1: Array & Struct).
Jalankan dengan: python main.py
"""

from exceptions.custom_exceptions import PerpustakaanError
from services.cari import cari_buku
from services.cari_pengarang import cari_buku_pengarang
from services.dipinjam import tampilkan_buku_dipinjam
from services.edit import edit_buku
from services.ekspor import ekspor_data_buku
from services.hapus import hapus_buku
from services.hapus_genre import hapus_buku_per_genre
from services.perpustakaan import (
    koleksi_buku,
    muat_data_contoh,
    tambah_buku,
)
from services.rentang_tahun import filter_rentang_tahun
from services.riwayat import riwayat_transaksi, tampilkan_riwayat_transaksi
from services.statistik import tampilkan_statistik_genre
from services.status import update_status_buku
from services.storage import inisialisasi_data
from services.tampil import filter_genre, tampilkan_semua_buku
from services.urutkan import urutkan_buku


def tampilkan_menu():
    """Mencetak menu utama."""
    print("\n========================================")
    print("      SISTEM PERPUSTAKAAN MINI")
    print("========================================")
    print("1. Tambah Buku Baru")
    print("2. Tampilkan Semua Buku")
    print("3. Cari Buku")
    print("4. Update Status Buku (Pinjam / Kembali)")
    print("5. Filter Buku Berdasarkan Genre")
    print("6. Hapus Buku")
    print("7. Edit Data Buku")
    print("8. Daftar Buku yang Sedang Dipinjam")
    print("9. Statistik Koleksi per Genre")
    print("10. Cari Buku Berdasarkan Pengarang")
    print("11. Filter Buku Berdasarkan Rentang Tahun")
    print("12. Hapus Semua Buku Berdasarkan Genre")
    print("13. Urutkan Buku (Sorting Judul/Tahun/Pengarang)")
    print("14. Ekspor Data Buku (CSV / JSON)")
    print("15. Riwayat Peminjaman & Pengembalian Buku")
    print("16. Muat Data Contoh (opsional)")
    print("0. Keluar")
    print("----------------------------------------")


# Peta pilihan menu -> fungsi fitur
MENU_FITUR = {
    "1": tambah_buku,
    "2": tampilkan_semua_buku,
    "3": cari_buku,
    "4": update_status_buku,
    "5": filter_genre,
    "6": hapus_buku,
    "7": edit_buku,
    "8": tampilkan_buku_dipinjam,
    "9": tampilkan_statistik_genre,
    "10": cari_buku_pengarang,
    "11": filter_rentang_tahun,
    "12": hapus_buku_per_genre,
    "13": urutkan_buku,
    "14": ekspor_data_buku,
    "15": tampilkan_riwayat_transaksi,
    "16": muat_data_contoh,
}


def main():
    """Loop utama: inisialisasi persistensi data, tampilkan menu, lalu jalankan fitur."""
    # Muat data lokal yang tersimpan di disk ke memori (Array of Struct)
    inisialisasi_data(koleksi_buku, riwayat_transaksi, callback_contoh=muat_data_contoh)

    try:
        while True:
            tampilkan_menu()
            pilihan = input("Pilih menu (0-16): ").strip()

            if pilihan == "0":
                print("Terima kasih. Program selesai.")
                break

            fitur = MENU_FITUR.get(pilihan)
            if fitur is None:
                print("Pilihan tidak valid. Masukkan angka 0 sampai 16.")
                continue

            try:
                fitur()
            except PerpustakaanError as galat:
                # Kesalahan yang sudah diperkirakan: tampilkan pesannya lalu kembali ke menu
                print(galat)
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C atau input terputus: keluar dengan rapi tanpa traceback
        print("\nProgram dihentikan. Terima kasih.")


if __name__ == "__main__":
    main()
