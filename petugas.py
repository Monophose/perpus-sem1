from database import hitung_statistik

def data_buku():
    print("data_buku")

def peminjaman():
    print("peminjaman")

def pengembalian():
    print("pengembalian")

def riwayat():
    print("riwayat")

def petugas_dashboard():
    print("\nWelcome, Petugas.\n")

    data = hitung_statistik()
    print(f"Total Buku: {data['total_buku']}")
    print(f"Buku Tersedia: {data['tersedia']}")
    print(f"Sedang dipinjam: {data['dipinjam']}")

    print("\nMenu:")
    print("1. Data Buku")
    print("2. Peminjaman")
    print("3. Pengembalian")
    print("4. Riwayat")

    nav = int(input("\nNavigasi ke-(1-4): "))

    if nav == 1:
        data_buku()
    elif nav == 2:
        peminjaman()
    elif nav == 3:
        pengembalian()
    elif nav == 4:
        riwayat()
    else:
        print("error")

