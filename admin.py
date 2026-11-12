from database import hitung_statistik

def admin_dashboard():
    print("\nWelcome, Admin.\n")

    data = hitung_statistik()
    print(f"Total Buku: {data['total_buku']}")
    print(f"Buku Tersedia: {data['tersedia']}")
    print(f"Sedang dipinjam: {data['dipinjam']}")

    test = input("Go to where?: ")