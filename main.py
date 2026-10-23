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
from services.hapus import hapus_buku
from services.perpustakaan import muat_data_contoh, tambah_buku
from services.rentang_tahun import filter_rentang_tahun
from services.statistik import tampilkan_statistik_genre
from services.status import update_status_buku
from services.tampil import filter_genre, tampilkan_semua_buku


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
    print("12. Muat Data Contoh (opsional)")
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
    "12": muat_data_contoh,
}


def main():
    """Loop utama: tampilkan menu, jalankan fitur, lalu kembali ke menu."""
    try:
        while True:
            tampilkan_menu()
            pilihan = input("Pilih menu (0-12): ").strip()

            if pilihan == "0":
                print("Terima kasih. Program selesai.")
                break

            fitur = MENU_FITUR.get(pilihan)
            if fitur is None:
                print("Pilihan tidak valid. Masukkan angka 0 sampai 12.")
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
