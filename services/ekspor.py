"""
ekspor.py (services)
Fitur Ekspor Koleksi Buku ke format file CSV atau JSON.
"""

import csv
import json
import os
from exceptions.custom_exceptions import DataKosongError
from services.perpustakaan import koleksi_buku


def ekspor_ke_csv(koleksi, nama_file="koleksi_buku.csv"):
    """Mengekspor koleksi buku ke file CSV."""
    if not koleksi:
        raise DataKosongError("Koleksi buku kosong, tidak ada data yang diekspor.")

    fieldnames = ["kode_buku", "judul", "pengarang", "genre", "tahun_terbit", "status"]
    with open(nama_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for buku in koleksi:
            writer.writerow(buku)
    return os.path.abspath(nama_file)


def ekspor_ke_json(koleksi, nama_file="koleksi_buku.json"):
    """Mengekspor koleksi buku ke file JSON berformat rapi (indented)."""
    if not koleksi:
        raise DataKosongError("Koleksi buku kosong, tidak ada data yang diekspor.")

    with open(nama_file, mode="w", encoding="utf-8") as f:
        json.dump(koleksi, f, indent=4, ensure_ascii=False)
    return os.path.abspath(nama_file)


def ekspor_data_buku():
    """Menu interaktif untuk mengekspor data buku."""
    if not koleksi_buku:
        raise DataKosongError("Koleksi buku masih kosong. Tidak ada data untuk diekspor.")

    print("\n--- EKSPOR DATA BUKU ---")
    print("1. Ekspor ke CSV (Excel compatible)")
    print("2. Ekspor ke JSON")
    pilihan = input("Pilih format ekspor (1-2): ").strip()

    try:
        if pilihan == "1":
            nama_file = input("Masukkan nama file [default: koleksi_buku.csv]: ").strip()
            if not nama_file:
                nama_file = "koleksi_buku.csv"
            if not nama_file.endswith(".csv"):
                nama_file += ".csv"
            path = ekspor_ke_csv(koleksi_buku, nama_file)
            print(f"Berhasil mengekspor {len(koleksi_buku)} buku ke file CSV:")
            print(f"Path: {path}")

        elif pilihan == "2":
            nama_file = input("Masukkan nama file [default: koleksi_buku.json]: ").strip()
            if not nama_file:
                nama_file = "koleksi_buku.json"
            if not nama_file.endswith(".json"):
                nama_file += ".json"
            path = ekspor_ke_json(koleksi_buku, nama_file)
            print(f"Berhasil mengekspor {len(koleksi_buku)} buku ke file JSON:")
            print(f"Path: {path}")
        else:
            print("Pilihan format tidak valid.")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengekspor: {e}")
