"""
statistik.py (services)
Fitur tambahan: Statistik Koleksi per Genre
(jumlah buku total, tersedia, dan dipinjam untuk setiap genre).
"""

from models.buku import STATUS_DIPINJAM, STATUS_TERSEDIA
from services.perpustakaan import koleksi_buku


def hitung_statistik_genre():
    """
    Logika fitur: mengelompokkan koleksi per genre (tidak case sensitive,
    "Fiksi" dan "fiksi" dianggap satu genre). Urutan mengikuti kemunculan pertama.
    Mengembalikan list dict: {"genre", "total", "tersedia", "dipinjam"}.
    """
    kelompok = {}  # kunci: genre huruf kecil -> data statistik
    for buku in koleksi_buku:
        kunci = buku["genre"].lower()
        if kunci not in kelompok:
            kelompok[kunci] = {
                "genre": buku["genre"],  # nama tampilan: penulisan pertama yang muncul
                "total": 0,
                "tersedia": 0,
                "dipinjam": 0,
            }
        data = kelompok[kunci]
        data["total"] += 1
        if buku["status"] == STATUS_TERSEDIA:
            data["tersedia"] += 1
        elif buku["status"] == STATUS_DIPINJAM:
            data["dipinjam"] += 1
    return list(kelompok.values())


def tampilkan_statistik_genre():
    """Tampilan terminal: tabel statistik per genre."""
    print("\n=== STATISTIK KOLEKSI PER GENRE ===")
    statistik = hitung_statistik_genre()
    if not statistik:
        print("Belum ada buku dalam koleksi.")
        return

    judul_kolom = ["Genre", "Total", "Tersedia", "Dipinjam"]
    baris = [
        [d["genre"], str(d["total"]), str(d["tersedia"]), str(d["dipinjam"])] for d in statistik
    ]
    lebar = [len(nama) for nama in judul_kolom]
    for isi in baris:
        for i, sel in enumerate(isi):
            lebar[i] = max(lebar[i], len(sel))

    garis = "+" + "+".join("-" * (w + 2) for w in lebar) + "+"

    def format_baris(isi):
        return "| " + " | ".join(sel.ljust(lebar[i]) for i, sel in enumerate(isi)) + " |"

    print(garis)
    print(format_baris(judul_kolom))
    print(garis)
    for isi in baris:
        print(format_baris(isi))
    print(garis)
    print("Jumlah genre: {}".format(len(statistik)))
