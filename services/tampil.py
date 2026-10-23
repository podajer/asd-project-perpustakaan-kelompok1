"""
tampil.py (services)
Fitur 2 (Tampilkan Semua Buku) dan Fitur 5 (Filter Buku Berdasarkan Genre),
beserta fungsi cetak tabel yang dipakai juga oleh Fitur 3 (cari.py).
"""

from exceptions.custom_exceptions import DataKosongError
from models.buku import STATUS_DIPINJAM, STATUS_TERSEDIA
from services.perpustakaan import koleksi_buku

KOLOM = ["No", "Kode", "Judul", "Pengarang", "Genre", "Tahun Terbit", "Status"]


def format_status(status):
    """Penanda visual status, contoh: [TERSEDIA] atau [DIPINJAM]."""
    return "[{}]".format(status.upper())


def cetak_tabel(daftar_buku):
    """Mencetak daftar buku dalam bentuk tabel dengan lebar kolom menyesuaikan isi."""
    baris = []
    for nomor, buku in enumerate(daftar_buku, start=1):
        baris.append(
            [
                str(nomor),
                buku["kode_buku"],
                buku["judul"],
                buku["pengarang"],
                buku["genre"],
                str(buku["tahun_terbit"]),
                format_status(buku["status"]),
            ]
        )

    # Lebar tiap kolom = teks terpanjang antara judul kolom dan seluruh isinya
    lebar = [len(nama) for nama in KOLOM]
    for isi_baris in baris:
        for i, sel in enumerate(isi_baris):
            lebar[i] = max(lebar[i], len(sel))

    garis = "+" + "+".join("-" * (w + 2) for w in lebar) + "+"

    def format_baris(isi):
        return "| " + " | ".join(sel.ljust(lebar[i]) for i, sel in enumerate(isi)) + " |"

    print(garis)
    print(format_baris(KOLOM))
    print(garis)
    for isi_baris in baris:
        print(format_baris(isi_baris))
    print(garis)


def hitung_ringkasan():
    """Mengembalikan (total, jumlah_tersedia, jumlah_dipinjam) dari seluruh koleksi."""
    tersedia = sum(1 for buku in koleksi_buku if buku["status"] == STATUS_TERSEDIA)
    dipinjam = sum(1 for buku in koleksi_buku if buku["status"] == STATUS_DIPINJAM)
    return len(koleksi_buku), tersedia, dipinjam


# ---------------------------------------------------------------------------
# Fitur 2: Tampilkan Semua Buku
# ---------------------------------------------------------------------------
def tampilkan_semua_buku():
    """Menampilkan seluruh koleksi dalam tabel, diikuti ringkasan total/tersedia/dipinjam."""
    print("\n=== DAFTAR SEMUA BUKU ===")
    if not koleksi_buku:
        print("Belum ada buku dalam koleksi.")
        return

    cetak_tabel(koleksi_buku)
    total, tersedia, dipinjam = hitung_ringkasan()
    print("Total buku : {}".format(total))
    print("Tersedia   : {}".format(tersedia))
    print("Dipinjam   : {}".format(dipinjam))


# ---------------------------------------------------------------------------
# Fitur 5: Filter Buku Berdasarkan Genre
# ---------------------------------------------------------------------------
def filter_by_genre(kata_kunci):
    """
    Logika Fitur 5: mengembalikan buku yang genre-nya mengandung kata kunci
    (partial match, tidak case sensitive). 'fiksi' cocok dengan 'Fiksi Ilmiah'.
    Melempar DataKosongError jika kata kunci kosong.
    """
    kata_kunci = kata_kunci.strip()
    if not kata_kunci:
        raise DataKosongError("genre")
    return [buku for buku in koleksi_buku if kata_kunci.lower() in buku["genre"].lower()]


def filter_genre():
    """Tampilan terminal Fitur 5."""
    print("\n=== FILTER BUKU BERDASARKAN GENRE ===")
    kata_kunci = input("Masukkan genre: ").strip()
    hasil = filter_by_genre(kata_kunci)

    if not hasil:
        print("Tidak ada buku dengan genre '{}' dalam koleksi.".format(kata_kunci))
        return

    print("Menampilkan buku genre: {} ({} buku ditemukan).".format(kata_kunci, len(hasil)))
    cetak_tabel(hasil)
