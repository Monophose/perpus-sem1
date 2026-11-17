import pandas as pd
from datetime import date, timedelta
from system import search, tampilkan_buku, tampilkan_peminjaman, input_buku, edit_buku, delete_buku, tampilkan_petugas, search_petugas, input_petugas, edit_petugas, delete_petugas

from database import (
    hitung_statistik,
    cari_buku,
    semua_peminjaman,
    kembalikan_buku,
    semua_petugas
)

def data_buku():
    while True:
        print("\n========== DATA BUKU ==========")

        data = cari_buku()
        tampilkan_buku(data)

        print("\nMenu:")
        print("1. Search Buku")
        print("2. Input Buku")
        print("3. Edit Buku")
        print("4. Hapus Buku")
        print("0. Back")

        nav = input("Pilih: ").strip()

        if nav == "1":
            search()
        elif nav == "2":
            input_buku()
        elif nav == "3":
            edit_buku()
        elif nav == "4":
            delete_buku()
        elif nav == "0":
            return
        else:
            print("Pilihan tidak valid!")


def data_petugas():
    while True:
        print("\n========== DATA PETUGAS ==========")

        data = semua_petugas()
        tampilkan_petugas(data)

        print("\nMenu:")
        print("1. Search Petugas")
        print("2. Tambah Petugas")
        print("3. Edit Petugas")
        print("4. Hapus Petugas")
        print("0. Back")

        nav = input("Pilih: ").strip()

        if nav == "1":
            search_petugas()
        elif nav == "2":
            input_petugas()
        elif nav == "3":
            edit_petugas()
        elif nav == "4":
            delete_petugas()
        elif nav == "0":
            return
        else:
            print("Pilihan tidak valid!")


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


def admin_dashboard(username):
    while True:
        print(f"\n========== WELCOME, {username} ==========")

        data = hitung_statistik()

        print(f"Total Buku       : {data['total_buku']}")
        print(f"Total Petugas    : {data['total_petugas']}")
        print(f"Sedang Dipinjam  : {data['dipinjam']}")
        print(f"Sudah Dikembalikan: {data['dikembalikan']}")

        print("\nMenu:")
        print("1. Data Buku")
        print("2. Data Petugas")
        print("3. Data Peminjaman")
        print("4. Logout")

        nav = input("\nNavigasi (1-4): ").strip()

        if nav == "1":
            data_buku()
        elif nav == "2":
            data_petugas()
        elif nav == "3":
            riwayat()
        elif nav == "4":
            print("Logging out...")
            return
        else:
            print("Pilihan tidak valid!")
