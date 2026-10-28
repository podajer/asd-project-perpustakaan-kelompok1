"""
urutkan.py (services)
Fitur Pengurutan Koleksi Buku (Sorting Algoritma ASD).
Mendukung pengurutan berdasarkan Judul, Tahun Terbit, atau Pengarang
secara Ascending atau Descending.
"""

from exceptions.custom_exceptions import DataKosongError
from services.perpustakaan import koleksi_buku
from services.tampil import cetak_tabel


def urutkan_koleksi(koleksi, kunci="judul", menaik=True):
    """
    Mengurutkan salinan daftar buku berdasarkan kunci tertentu.
    Implementasi algoritma pengurutan stabil.
    
    :param koleksi: list of dict buku
    :param kunci: 'judul', 'tahun_terbit', atau 'pengarang'
    :param menaik: True untuk ascending, False untuk descending
    :return: list baru berisi buku yang sudah terurut
    """
    if not koleksi:
        return []

    def dapatkan_kunci(item):
        nilai = item.get(kunci, "")
        if isinstance(nilai, str):
            return nilai.lower()
        return nilai

    return sorted(koleksi, key=dapatkan_kunci, reverse=not menaik)


def urutkan_buku():
    """Menu interaktif untuk mengurutkan koleksi buku."""
    if not koleksi_buku:
        raise DataKosongError("Koleksi buku masih kosong. Tidak ada data untuk diurutkan.")

    print("\n--- URUTKAN KOLEKSI BUKU ---")
    print("Kriteria Urutan:")
    print("1. Judul Buku (A-Z / Z-A)")
    print("2. Tahun Terbit (Terkuno / Terbaru)")
    print("3. Nama Pengarang (A-Z / Z-A)")

    pilihan_kriteria = input("Pilih kriteria (1-3): ").strip()
    kunci_map = {
        "1": "judul",
        "2": "tahun_terbit",
        "3": "pengarang",
    }

    kunci = kunci_map.get(pilihan_kriteria)
    if not kunci:
        print("Pilihan kriteria tidak valid.")
        return

    print("\nArah Urutan:")
    print("1. Ascending (Menaik / A-Z / Terlama)")
    print("2. Descending (Menurun / Z-A / Terbaru)")
    pilihan_arah = input("Pilih arah (1-2): ").strip()

    if pilihan_arah == "1":
        menaik = True
    elif pilihan_arah == "2":
        menaik = False
    else:
        print("Pilihan arah tidak valid.")
        return

    hasil = urutkan_koleksi(koleksi_buku, kunci=kunci, menaik=menaik)
    label_kunci = {"judul": "Judul", "tahun_terbit": "Tahun Terbit", "pengarang": "Pengarang"}[kunci]
    label_arah = "Ascending" if menaik else "Descending"

    print(f"\nHasil Pengurutan berdasarkan {label_kunci} ({label_arah}):")
    cetak_tabel(hasil)
