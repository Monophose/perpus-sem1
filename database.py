import sqlite3
import hashlib

def connection():
    conn = sqlite3.connect("perpustakaan.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def password_encryption(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def default_data():
    conn = connection()
    try:
        with conn:
            conn.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nama TEXT NOT NULL,
                            username TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            role TEXT NOT NULL CHECK (role IN ('admin', 'petugas'))
                        )""")
            conn.execute("""
                        CREATE TABLE IF NOT EXISTS buku (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            kode_buku TEXT NOT NULL UNIQUE,
                            judul TEXT NOT NULL,
                            penulis TEXT,
                            penerbit TEXT,
                            tahun_terbit INTEGER,
                            kategori TEXT,
                            jumlah_total INTEGER NOT NULL DEFAULT 0 CHECK (jumlah_total >= 0)
                        )""")
            conn.execute("""
                        CREATE TABLE IF NOT EXISTS peminjaman (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nama_peminjam TEXT NOT NULL,
                            buku_id INTEGER NOT NULL,
                            tanggal_pinjam TEXT NOT NULL,
                            tanggal_kembali TEXT NOT NULL,
                            status TEXT NOT NULL DEFAULT 'Dipinjam'
                                CHECK (status IN ('Dipinjam', 'Dikembalikan')),
                            FOREIGN KEY (buku_id) REFERENCES buku (id) ON DELETE CASCADE
                        )""")

            if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
                conn.execute("INSERT INTO users (nama, username, password, role) VALUES (?,?,?,?)",
                                ("Administrator", "admin", password_encryption("admin123"), "admin"))
                conn.execute("INSERT INTO users (nama, username, password, role) VALUES (?,?,?,?)",
                                ("Petugas Perpustakaan", "petugas", password_encryption("petugas123"), "petugas"))

            if conn.execute("SELECT COUNT(*) FROM buku").fetchone()[0] == 0:
                contoh = [
                    ("BK001", "Belajar Python Dasar", "Budi Santoso", "Informatika", 2021, "Pemrograman", 5),
                    ("BK002", "Basis Data untuk Pemula", "Siti Aminah", "Gramedia", 2020, "Database", 3),
                    ("BK003", "Laskar Pelangi", "Andrea Hirata", "Bentang", 2005, "Novel", 4),
                    ("BK004", "Algoritma dan Logika", "Rudi Hartono", "Erlangga", 2019, "Pemrograman", 2),
                    ("BK005", "Sejarah Indonesia", "Ahmad Fauzi", "Pustaka", 2018, "Sejarah", 6),
                ]
                conn.executemany(
                    "INSERT INTO buku (kode_buku, judul, penulis, penerbit, tahun_terbit, kategori, jumlah_total) "
                    "VALUES (?,?,?,?,?,?,?)", contoh)
    finally:
        conn.close()

def check_login(username, password):
    conn = connection()
    try:
        password = password_encryption(password)

        user = conn.execute("""
            SELECT id, nama, username, role
            FROM users
            WHERE username = ? AND password = ?
            """, (username, password)).fetchone()

        return user

    finally:
        conn.close()

def hitung_statistik():
    conn = connection()
    try:
        total = conn.execute("SELECT COALESCE(SUM(jumlah_total), 0) FROM buku").fetchone()[0]
        dipinjam = conn.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dipinjam'").fetchone()[0]
        dikembalikan = conn.execute("SELECT COUNT(*) FROM peminjaman WHERE status = 'Dikembalikan'").fetchone()[0]
        return {
            "total_buku": total,
            "tersedia": total - dipinjam,
            "dipinjam": dipinjam,
            "dikembalikan": dikembalikan,
            "total_peminjaman": dipinjam + dikembalikan,
            "total_petugas": conn.execute("SELECT COUNT(*) FROM users WHERE role = 'petugas'").fetchone()[0]
        }
    finally:
        conn.close()