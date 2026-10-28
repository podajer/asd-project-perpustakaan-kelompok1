"""
storage.py (services)
Modul Persistensi Data Lokal:
Menyimpan dan memuat koleksi buku serta riwayat transaksi ke/dari file JSON lokal,
sehingga perubahan data tetap tersimpan saat program ditutup dan dibuka kembali.
"""

import json
import os

FOLDER_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
BERKAS_BUKU = os.path.join(FOLDER_DATA, "koleksi_buku.json")
BERKAS_RIWAYAT = os.path.join(FOLDER_DATA, "riwayat_transaksi.json")


def pastikan_folder_data():
    """Memastikan direktori penyimpanan 'data/' ada."""
    if not os.path.exists(FOLDER_DATA):
        os.makedirs(FOLDER_DATA, exist_ok=True)


def simpan_koleksi_ke_file(koleksi, berkas=BERKAS_BUKU):
    """Menyimpan list koleksi_buku ke file JSON."""
    pastikan_folder_data()
    try:
        with open(berkas, "w", encoding="utf-8") as f:
            json.dump(koleksi, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Peringatan: Gagal menyimpan data buku ke storage: {e}")
        return False


def muat_koleksi_dari_file(berkas=BERKAS_BUKU):
    """
    Memuat list koleksi_buku dari file JSON jika ada.
    Mengembalikan list data atau None jika berkas belum ada.
    """
    if not os.path.exists(berkas):
        return None
    try:
        with open(berkas, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception as e:
        print(f"Peringatan: Gagal membaca data buku dari storage: {e}")
    return None


def simpan_riwayat_ke_file(riwayat, berkas=BERKAS_RIWAYAT):
    """Menyimpan riwayat transaksi ke file JSON."""
    pastikan_folder_data()
    try:
        with open(berkas, "w", encoding="utf-8") as f:
            json.dump(riwayat, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Peringatan: Gagal menyimpan log transaksi: {e}")
        return False


def muat_riwayat_dari_file(berkas=BERKAS_RIWAYAT):
    """Memuat riwayat transaksi dari file JSON jika ada."""
    if not os.path.exists(berkas):
        return None
    try:
        with open(berkas, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception as e:
        print(f"Peringatan: Gagal membaca riwayat transaksi: {e}")
    return None


def inisialisasi_data(koleksi_buku, riwayat_transaksi, callback_contoh=None):
    """
    Memuat data tersimpan dari file ke koleksi memori saat aplikasi dijalankan.
    Jika belum ada data sama sekali, memanggil callback_contoh (opsional).
    """
    data_tersimpan = muat_koleksi_dari_file()
    if data_tersimpan is not None and len(data_tersimpan) > 0:
        koleksi_buku.clear()
        koleksi_buku.extend(data_tersimpan)
    elif callback_contoh is not None and len(koleksi_buku) == 0:
        callback_contoh(pesan=False)
        simpan_koleksi_ke_file(koleksi_buku)

    log_tersimpan = muat_riwayat_dari_file()
    if log_tersimpan is not None:
        riwayat_transaksi.clear()
        riwayat_transaksi.extend(log_tersimpan)


def sinkronkan_koleksi(koleksi_buku):
    """Helper praktis untuk menyimpan kondisi terbaru koleksi."""
    simpan_koleksi_ke_file(koleksi_buku)


def sinkronkan_riwayat(riwayat_transaksi):
    """Helper praktis untuk menyimpan kondisi terbaru riwayat."""
    simpan_riwayat_ke_file(riwayat_transaksi)
