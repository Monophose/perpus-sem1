import pandas as pd
from datetime import date, timedelta
from system import search, tampilkan_buku, pilih_buku, tampilkan_peminjaman

from database import (
    hitung_statistik,
    cari_buku,
    simpan_peminjaman,
    semua_peminjaman,
    kembalikan_buku
)


def data_buku():
    while True:
        print("\n========== DATA BUKU ==========")

        data = cari_buku()
        tampilkan_buku(data)

        print("\nMenu:")
        print("1. Search Buku")
        print("2. Refresh")
        print("0. Back")

        nav = input("Pilih: ").strip()

        if nav == "1":
            search()
        elif nav == "2":
            continue
        elif nav == "0":
            return
        else:
            print("Pilihan tidak valid!")


def peminjaman():
    print("\n========== PEMINJAMAN BUKU ==========")

    nama = input("Nama Peminjam: ").strip()

    if not nama:
        print("Nama peminjam tidak boleh kosong!")
        return

    buku = pilih_buku()

    if buku is None:
        print("Peminjaman dibatalkan.")
        return

    print("\nPilih Lama Peminjaman:")
    print("1. 3 Hari")
    print("2. 7 Hari")
    print("3. 14 Hari")

    pilihan = input("Pilih (1-3): ").strip()

    durasi = {
        "1": 3,
        "2": 7,
        "3": 14
    }

    if pilihan not in durasi:
        print("Pilihan tidak valid!")
        return

    tanggal_pinjam = date.today()
    tanggal_kembali = tanggal_pinjam + timedelta(
        days=durasi[pilihan]
    )

    print("\n========== KONFIRMASI ==========")
    print(f"Nama            : {nama}")
    print(f"Judul Buku      : {buku[2]}")
    print(f"Kode Buku       : {buku[1]}")
    print(f"Tanggal Pinjam  : {tanggal_pinjam}")
    print(f"Tanggal Kembali : {tanggal_kembali}")

    konfirmasi = input(
        "\nSimpan peminjaman? (Y/N): "
    ).strip().lower()

    if konfirmasi != "y":
        print("Peminjaman dibatalkan!")
        return

    berhasil, pesan = simpan_peminjaman(
        nama,
        buku[0],
        str(tanggal_pinjam),
        str(tanggal_kembali)
    )

    print(f"\n{pesan}")


def pengembalian():
    while True:
        data = semua_peminjaman("Dipinjam")

        print("\n========== PENGEMBALIAN BUKU ==========")
        df = tampilkan_peminjaman(data)

        if df.empty:
            input("\nTekan Enter untuk kembali...")
            return

        pilihan = input(
            "\nMasukkan ID Peminjaman (0 = kembali): "
        ).strip()

        if pilihan == "0":
            return

        if not pilihan.isdigit():
            print("Masukkan ID yang valid!")
            continue

        peminjaman_id = int(pilihan)

        if peminjaman_id not in df["ID"].values:
            print("ID peminjaman tidak ditemukan!")
            continue

        konfirmasi = input(
            "Konfirmasi pengembalian? (Y/N): "
        ).strip().lower()

        if konfirmasi == "n":
            continue

        if konfirmasi != "y":
            print("Pilihan tidak valid!")
            continue

        berhasil = kembalikan_buku(peminjaman_id)

        if berhasil:
            print("Buku berhasil dikembalikan!")
        else:
            print("Pengembalian gagal atau buku sudah dikembalikan!")


def riwayat():
    data = semua_peminjaman()

    print("\n========== RIWAYAT PEMINJAMAN ==========")
    tampilkan_peminjaman(data)

    input("\nTekan Enter untuk kembali...")


def petugas_dashboard(username):
    while True:
        print(f"\n========== WELCOME, {username} ==========")

        data = hitung_statistik()

        print(f"Total Buku       : {data['total_buku']}")
        print(f"Buku Tersedia    : {data['tersedia']}")
        print(f"Sedang Dipinjam  : {data['dipinjam']}")
        print(f"Sudah Dikembalikan: {data['dikembalikan']}")

        print("\nMenu:")
        print("1. Data Buku")
        print("2. Peminjaman")
        print("3. Pengembalian")
        print("4. Riwayat")
        print("5. Logout")

        nav = input("\nNavigasi (1-5): ").strip()

        if nav == "1":
            data_buku()
        elif nav == "2":
            peminjaman()
        elif nav == "3":
            pengembalian()
        elif nav == "4":
            riwayat()
        elif nav == "5":
            print("Logging out...")
            return
        else:
            print("Pilihan tidak valid!")
