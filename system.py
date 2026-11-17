from database import (
    cari_buku,
    hitung_stok_tersedia,
    tambah_buku,
    kode_buku_sudah_ada,
    ubah_buku,
    hapus_buku,
    semua_petugas,
    tambah_petugas,
    ubah_petugas,
    hapus_petugas
)
import pandas as pd

KOLOM_BUKU = [
    "ID", "Kode Buku", "Judul", "Penulis",
    "Penerbit", "Tahun Terbit", "Kategori", "Jumlah Total"
]

KOLOM_PINJAMAN = [
    "ID", "Nama Peminjam", "Kode Buku", "Judul",
    "Tanggal Pinjam", "Tanggal Kembali", "Status"
]



def tampilkan_buku(data):
    df = pd.DataFrame(data, columns=KOLOM_BUKU)

    if df.empty:
        print("Tidak ada data buku.")
        return df

    df["Tersedia"] = [
        hitung_stok_tersedia(buku[0])
        for buku in data
    ]

    print(df.to_string(index=False))
    return df


def tampilkan_peminjaman(data):
    df = pd.DataFrame(data, columns=KOLOM_PINJAMAN)

    if df.empty:
        print("Tidak ada data peminjaman.")
    else:
        print(df.to_string(index=False))

    return df

def pilih_buku():
    while True:
        keyword = input(
            "\nCari buku (kosong = semua, q = batal): "
        ).strip()

        if keyword.lower() == "q":
            return None

        data = cari_buku(keyword)

        if not data:
            print("Buku tidak ditemukan!")
            continue

        print("\n========== DAFTAR BUKU ==========")
        tampilkan_buku(data)

        pilihan = input(
            "\nMasukkan ID buku (0 = batal): "
        ).strip()

        if pilihan == "0":
            return None

        if not pilihan.isdigit():
            print("ID harus berupa angka!")
            continue

        buku = next(
            (b for b in data if b[0] == int(pilihan)),
            None
        )

        if buku is None:
            print("ID buku tidak ditemukan!")
            continue

        tersedia = hitung_stok_tersedia(buku[0])

        if tersedia <= 0:
            print("Stok buku sedang habis!")
            continue

        print("\n========== DETAIL BUKU ==========")
        print(f"Kode      : {buku[1]}")
        print(f"Judul     : {buku[2]}")
        print(f"Penulis   : {buku[3]}")
        print(f"Penerbit  : {buku[4]}")
        print(f"Tahun     : {buku[5]}")
        print(f"Kategori  : {buku[6]}")
        print(f"Tersedia  : {tersedia}")

        konfirmasi = input(
            "\nPilih buku ini? (Y/N): "
        ).strip().lower()

        if konfirmasi == "y":
            return buku
        elif konfirmasi == "n":
            continue
        else:
            print("Pilihan tidak valid!")

def search():
    while True:
        keyword = input(
            "\nMasukkan keyword (q = kembali): "
        ).strip()

        if keyword.lower() == "q":
            return

        data = cari_buku(keyword)

        print("\n========== HASIL PENCARIAN ==========")
        tampilkan_buku(data)

        nav = input(
            "\nTekan Enter untuk mencari lagi / q untuk kembali: "
        ).strip().lower()

        if nav == "q":
            return

def input_buku():
    print("\n========== TAMBAH BUKU ==========")

    kode = input("Kode Buku      : ").strip()

    if kode_buku_sudah_ada(kode):
            print("Kode buku sudah digunakan!")
            return

    judul = input("Judul Buku     : ").strip()
    penulis = input("Penulis        : ").strip()
    penerbit = input("Penerbit       : ").strip()
    tahun = input("Tahun Terbit   : ").strip()
    kategori = input("Kategori       : ").strip()
    jumlah = input("Jumlah Buku    : ").strip()

    if not all([kode, judul, penulis, penerbit, tahun, kategori, jumlah]):
        print("Semua kolom wajib diisi!")
        return   

    if not tahun.isdigit() or not jumlah.isdigit():
        print("Tahun dan jumlah harus berupa angka!")
        return

    tahun = int(tahun)
    jumlah = int(jumlah)

    if jumlah < 0:
        print("Jumlah buku tidak boleh negatif!")
        return

    if tahun < 0:
        print("Tahun tidak valid!")
        return

    print("\n========== KONFIRMASI ==========")
    print(f"Kode Buku   : {kode}")
    print(f"Judul       : {judul}")
    print(f"Penulis     : {penulis}")
    print(f"Penerbit    : {penerbit}")
    print(f"Tahun       : {tahun}")
    print(f"Kategori    : {kategori}")
    print(f"Jumlah      : {jumlah}")

    konfirmasi = input("\nSimpan buku? (Y/N): ").strip().lower()

    if konfirmasi != "y":
        print("Penambahan buku dibatalkan!")
        return

    berhasil, pesan = tambah_buku(
        kode, judul, penulis, penerbit,
        tahun, kategori, jumlah
    )

    print(f"\n{pesan}")


def edit_buku():
    print("\n========== EDIT BUKU ==========")

    data = cari_buku()

    if not data:
        print("Belum ada data buku!")
        return

    df = pd.DataFrame(data, columns=[
        "ID", "Kode Buku", "Judul", "Penulis",
        "Penerbit", "Tahun Terbit", "Kategori", "Jumlah Total"
    ])

    print(df.to_string(index=False))

    pilihan = input("\nMasukkan ID buku (0 = batal): ").strip()

    if pilihan == "0":
        return

    if not pilihan.isdigit():
        print("ID harus berupa angka!")
        return

    buku = next((b for b in data if b[0] == int(pilihan)), None)

    if buku is None:
        print("Buku tidak ditemukan!")
        return

    print("\n========== DATA BARU ==========")
    print("Kosongkan input jika ingin mempertahankan data lama.")

    kode = input(f"Kode Buku [{buku[1]}]: ").strip() or buku[1]
    judul = input(f"Judul [{buku[2]}]: ").strip() or buku[2]
    penulis = input(f"Penulis [{buku[3]}]: ").strip() or buku[3]
    penerbit = input(f"Penerbit [{buku[4]}]: ").strip() or buku[4]
    tahun = input(f"Tahun Terbit [{buku[5]}]: ").strip()
    kategori = input(f"Kategori [{buku[6]}]: ").strip() or buku[6]
    jumlah = input(f"Jumlah Total [{buku[7]}]: ").strip()

    tahun = str(buku[5]) if not tahun else tahun
    jumlah = str(buku[7]) if not jumlah else jumlah

    if not tahun.isdigit() or not jumlah.isdigit():
        print("Tahun dan jumlah harus berupa angka!")
        return

    tahun = int(tahun)
    jumlah = int(jumlah)

    if tahun <= 0 or jumlah < 0:
        print("Tahun atau jumlah tidak valid!")
        return

    print("\n========== KONFIRMASI PERUBAHAN ==========")
    print(f"Kode Buku   : {kode}")
    print(f"Judul       : {judul}")
    print(f"Penulis     : {penulis}")
    print(f"Penerbit    : {penerbit}")
    print(f"Tahun       : {tahun}")
    print(f"Kategori    : {kategori}")
    print(f"Jumlah Total: {jumlah}")

    konfirmasi = input("\nSimpan perubahan? (Y/N): ").strip().lower()

    if konfirmasi != "y":
        print("Edit buku dibatalkan!")
        return

    berhasil, pesan = ubah_buku(
        buku[0], kode, judul, penulis,
        penerbit, tahun, kategori, jumlah
    )

    print(f"\n{pesan}")

def delete_buku():
    print("\n========== HAPUS BUKU ==========")

    data = cari_buku()

    if not data:
        print("Belum ada data buku!")
        return

    df = pd.DataFrame(data, columns=[
        "ID", "Kode Buku", "Judul", "Penulis",
        "Penerbit", "Tahun Terbit", "Kategori", "Jumlah Total"
    ])

    print(df.to_string(index=False))

    pilihan = input("\nMasukkan ID buku (0 = batal): ").strip()

    if pilihan == "0":
        return

    if not pilihan.isdigit():
        print("ID harus berupa angka!")
        return

    buku = next((b for b in data if b[0] == int(pilihan)), None)

    if buku is None:
        print("Buku tidak ditemukan!")
        return

    print("\n========== DETAIL BUKU ==========")
    print(f"Kode Buku : {buku[1]}")
    print(f"Judul     : {buku[2]}")
    print(f"Penulis   : {buku[3]}")

    konfirmasi = input("\nYakin ingin menghapus buku ini? (Y/N): ").strip().lower()

    if konfirmasi != "y":
        print("Penghapusan dibatalkan!")
        return

    berhasil, pesan = hapus_buku(buku[0])
    print(f"\n{pesan}")

def tampilkan_petugas(data):
    df = pd.DataFrame(
        data,
        columns=["ID", "Nama", "Username"]
    )

    if df.empty:
        print("Belum ada petugas terdaftar!")
    else:
        print(df.to_string(index=False))

    return df

def search_petugas():
    while True:
        keyword = input("\nMasukkan keyword (q = kembali): ").strip()

        if keyword.lower() == "q":
            return

        data = semua_petugas()

        hasil = [
            petugas for petugas in data
            if keyword.lower() in petugas[1].lower()
            or keyword.lower() in petugas[2].lower()
        ]

        print("\n========== HASIL PENCARIAN ==========")
        tampilkan_petugas(hasil)

        nav = input("\nEnter = Search lagi / q = kembali: ").strip().lower()

        if nav == "q":
            return
def input_petugas():
    print("\n========== TAMBAH PETUGAS ==========")

    nama = input("Nama     : ").strip()
    username = input("Username : ").strip()
    password = input("Password : ").strip()

    if not all([nama, username, password]):
        print("Semua kolom wajib diisi!")
        return

    print("\n========== KONFIRMASI ==========")
    print(f"Nama     : {nama}")
    print(f"Username : {username}")
    print("Password : ********")

    konfirmasi = input("\nSimpan petugas? (Y/N): ").strip().lower()

    if konfirmasi != "y":
        print("Penambahan petugas dibatalkan!")
        return

    berhasil, pesan = tambah_petugas(nama, username, password)
    print(f"\n{pesan}")

def edit_petugas():
    print("\n========== EDIT PETUGAS ==========")

    data = semua_petugas()

    if not data:
        print("Belum ada petugas terdaftar!")
        return

    tampilkan_petugas(data)

    pilihan = input("\nMasukkan ID petugas (0 = batal): ").strip()

    if pilihan == "0":
        return

    if not pilihan.isdigit():
        print("ID harus berupa angka!")
        return

    petugas = next(
        (p for p in data if p[0] == int(pilihan)),
        None
    )

    if petugas is None:
        print("Petugas tidak ditemukan!")
        return

    print("\n========== DATA BARU ==========")
    print("Kosongkan input jika ingin mempertahankan data lama.")

    nama = input(f"Nama [{petugas[1]}]: ").strip() or petugas[1]
    username = input(f"Username [{petugas[2]}]: ").strip() or petugas[2]
    password = input("Password [tidak diubah]: ").strip()

    print("\n========== KONFIRMASI ==========")
    print(f"Nama     : {nama}")
    print(f"Username : {username}")
    print(f"Password : {'Diubah' if password else 'Tidak diubah'}")

    konfirmasi = input("\nSimpan perubahan? (Y/N): ").strip().lower()

    if konfirmasi != "y":
        print("Edit petugas dibatalkan!")
        return

    berhasil, pesan = ubah_petugas(
        petugas[0], nama, username, password
    )

    print(f"\n{pesan}")

def delete_petugas():
    print("\n========== HAPUS PETUGAS ==========")

    data = semua_petugas()

    if not data:
        print("Belum ada petugas terdaftar!")
        return

    tampilkan_petugas(data)

    pilihan = input("\nMasukkan ID petugas (0 = batal): ").strip()

    if pilihan == "0":
        return

    if not pilihan.isdigit():
        print("ID harus berupa angka!")
        return

    petugas = next(
        (p for p in data if p[0] == int(pilihan)),
        None
    )

    if petugas is None:
        print("Petugas tidak ditemukan!")
        return

    print("\n========== DETAIL PETUGAS ==========")
    print(f"Nama     : {petugas[1]}")
    print(f"Username : {petugas[2]}")

    konfirmasi = input("\nYakin ingin menghapus petugas ini? (Y/N): ").strip().lower()

    if konfirmasi != "y":
        print("Penghapusan dibatalkan!")
        return

    berhasil, pesan = hapus_petugas(petugas[0])
    print(f"\n{pesan}")