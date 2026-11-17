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


def cari_buku(keyword=""):
    conn = connection()
    try:
        pola = f"%{keyword}%"

        query = """
            SELECT id, kode_buku, judul, penulis,
                   penerbit, tahun_terbit, kategori, jumlah_total
            FROM buku
            WHERE kode_buku LIKE ?
               OR judul LIKE ?
               OR penulis LIKE ?
               OR kategori LIKE ?
            ORDER BY judul ASC
        """

        hasil = conn.execute(
            query,
            (pola, pola, pola, pola)
        ).fetchall()

        return hasil

    finally:
        conn.close()


def hitung_stok_tersedia(buku_id):
    conn = connection()
    try:
        total = conn.execute(
            "SELECT jumlah_total FROM buku WHERE id = ?",
            (buku_id,)
        ).fetchone()

        if total is None:
            return 0

        dipinjam = conn.execute(
            """
            SELECT COUNT(*)
            FROM peminjaman
            WHERE buku_id = ? AND status = 'Dipinjam'
            """,
            (buku_id,)
        ).fetchone()[0]

        return total[0] - dipinjam

    finally:
        conn.close()


def simpan_peminjaman(nama, buku_id, tanggal_pinjam, tanggal_kembali):
    conn = connection()

    try:
        with conn:
            total = conn.execute(
                "SELECT jumlah_total FROM buku WHERE id = ?",
                (buku_id,)
            ).fetchone()

            if total is None:
                return False, "Buku tidak ditemukan!"

            dipinjam = conn.execute(
                """
                SELECT COUNT(*)
                FROM peminjaman
                WHERE buku_id = ? AND status = 'Dipinjam'
                """,
                (buku_id,)
            ).fetchone()[0]

            if total[0] - dipinjam <= 0:
                return False, "Stok buku habis!"

            aktif = conn.execute(
                """
                SELECT COUNT(*)
                FROM peminjaman
                WHERE nama_peminjam = ? AND status = 'Dipinjam'
                """,
                (nama,)
            ).fetchone()[0]

            if aktif >= 3:
                return False, "Peminjam sudah mencapai batas 3 buku!"

            duplikat = conn.execute(
                """
                SELECT COUNT(*)
                FROM peminjaman
                WHERE nama_peminjam = ?
                AND buku_id = ?
                AND status = 'Dipinjam'
                """,
                (nama, buku_id)
            ).fetchone()[0]

            if duplikat > 0:
                return False, "Peminjam masih meminjam buku ini!"

            conn.execute(
                """
                INSERT INTO peminjaman
                (nama_peminjam, buku_id, tanggal_pinjam, tanggal_kembali)
                VALUES (?, ?, ?, ?)
                """,
                (nama, buku_id, tanggal_pinjam, tanggal_kembali)
            )

        return True, "Peminjaman berhasil disimpan!"

    finally:
        conn.close()

def semua_peminjaman(status=None):
    conn = connection()

    try:
        query = """
            SELECT
                p.id,
                p.nama_peminjam,
                b.kode_buku,
                b.judul,
                p.tanggal_pinjam,
                p.tanggal_kembali,
                p.status
            FROM peminjaman p
            JOIN buku b ON p.buku_id = b.id
        """

        if status:
            query += " WHERE p.status = ?"
            data = conn.execute(
                query + " ORDER BY p.id DESC",
                (status,)
            ).fetchall()
        else:
            data = conn.execute(
                query + " ORDER BY p.id DESC"
            ).fetchall()

        return data

    finally:
        conn.close()

def kembalikan_buku(peminjaman_id):
    conn = connection()

    try:
        with conn:
            cur = conn.execute(
                """
                UPDATE peminjaman
                SET status = 'Dikembalikan'
                WHERE id = ? AND status = 'Dipinjam'
                """,
                (peminjaman_id,)
            )

        return cur.rowcount > 0

    finally:
        conn.close()

def tambah_buku(kode, judul, penulis, penerbit, tahun, kategori, jumlah_total):
    conn = connection()

    try:
        with conn:
            conn.execute(
                """
                INSERT INTO buku
                (kode_buku, judul, penulis, penerbit,
                 tahun_terbit, kategori, jumlah_total)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (kode, judul, penulis, penerbit,
                 tahun, kategori, jumlah_total)
            )

        return True, "Buku berhasil ditambahkan!"

    except sqlite3.IntegrityError:
        return False, "Kode buku sudah digunakan atau data tidak valid!"

    finally:
        conn.close()


def kode_buku_sudah_ada(kode, abaikan_id=None):
    conn = connection()
    try:
        if abaikan_id is None:
            baris = conn.execute(
                "SELECT id FROM buku WHERE UPPER(kode_buku) = UPPER(?)",
                (kode,)
            ).fetchone()
        else:
            baris = conn.execute(
                """SELECT id FROM buku
                   WHERE UPPER(kode_buku) = UPPER(?)
                   AND id != ?""",
                (kode, abaikan_id)
            ).fetchone()

        return baris is not None
    finally:
        conn.close()

def ubah_buku(buku_id, kode, judul, penulis, penerbit, tahun, kategori, jumlah_total):
    conn = connection()
    try:
        with conn:
            lama = conn.execute(
                "SELECT kode_buku FROM buku WHERE id = ?",
                (buku_id,)
            ).fetchone()

            if lama is None:
                return False, "Buku tidak ditemukan."

            dipinjam = conn.execute(
                """SELECT COUNT(*) FROM peminjaman
                   WHERE buku_id = ? AND status = 'Dipinjam'""",
                (buku_id,)
            ).fetchone()[0]

            if dipinjam > 0 and kode.upper() != lama[0].upper():
                return False, (
                    "Kode buku tidak bisa diubah karena "
                    "buku ini sedang dipinjam."
                )

            if jumlah_total < dipinjam:
                return False, (
                    f"Jumlah total tidak boleh lebih kecil "
                    f"dari jumlah buku yang sedang dipinjam ({dipinjam})."
                )

            conn.execute(
                """UPDATE buku
                   SET kode_buku = ?, judul = ?, penulis = ?,
                       penerbit = ?, tahun_terbit = ?,
                       kategori = ?, jumlah_total = ?
                   WHERE id = ?""",
                (kode, judul, penulis, penerbit, tahun,
                 kategori, jumlah_total, buku_id)
            )

        return True, "Data buku berhasil diubah."

    except sqlite3.IntegrityError:
        return False, "Kode buku sudah digunakan atau data tidak valid!"

    finally:
        conn.close()

def hapus_buku(buku_id):
    conn = connection()
    try:
        with conn:
            buku = conn.execute(
                "SELECT id FROM buku WHERE id = ?",
                (buku_id,)
            ).fetchone()

            if buku is None:
                return False, "Buku tidak ditemukan!"

            dipinjam = conn.execute(
                """SELECT COUNT(*) FROM peminjaman
                   WHERE buku_id = ? AND status = 'Dipinjam'""",
                (buku_id,)
            ).fetchone()[0]

            if dipinjam > 0:
                return False, (
                    f"Buku tidak bisa dihapus karena masih "
                    f"dipinjam ({dipinjam} buku)."
                )

            conn.execute(
                "DELETE FROM buku WHERE id = ?",
                (buku_id,)
            )

        return True, "Buku berhasil dihapus!"

    finally:
        conn.close()


def semua_petugas():
    conn = connection()
    try:
        data = conn.execute(
            """SELECT id, nama, username
               FROM users
               WHERE role = 'petugas'
               ORDER BY nama"""
        ).fetchall()

        return data

    finally:
        conn.close()

def validasi_username(username):
    if not username:
        return "Username tidak boleh kosong!"
    if len(username) < 3:
        return "Username minimal 3 karakter!"
    if not username.replace("_", "").isalnum():
        return "Username hanya boleh berisi huruf, angka, dan underscore!"
    return None


def validasi_password(password):
    if len(password) < 8:
        return "Password minimal 8 karakter!"
    return None


def username_sudah_ada(username, abaikan_id=None):
    conn = connection()
    try:
        if abaikan_id is None:
            baris = conn.execute(
                "SELECT id FROM users WHERE LOWER(username) = LOWER(?)",
                (username,)
            ).fetchone()
        else:
            baris = conn.execute(
                """SELECT id FROM users
                   WHERE LOWER(username) = LOWER(?) AND id != ?""",
                (username, abaikan_id)
            ).fetchone()

        return baris is not None
    finally:
        conn.close()

def tambah_petugas(nama, username, password):
    pesan = validasi_username(username) or validasi_password(password)

    if pesan:
        return False, pesan

    if not nama.strip():
        return False, "Nama tidak boleh kosong!"

    if username_sudah_ada(username):
        return False, "Username sudah dipakai!"

    conn = connection()
    try:
        with conn:
            conn.execute(
                """INSERT INTO users (nama, username, password, role)
                   VALUES (?, ?, ?, 'petugas')""",
                (nama, username, password_encryption(password))
            )

        return True, "Petugas berhasil ditambahkan!"

    except sqlite3.IntegrityError:
        return False, "Username sudah dipakai atau data tidak valid!"

    finally:
        conn.close()

def ubah_petugas(user_id, nama, username, password=""):
    pesan = validasi_username(username)

    if pesan is None and password != "":
        pesan = validasi_password(password)

    if pesan:
        return False, pesan

    if not nama.strip():
        return False, "Nama tidak boleh kosong!"

    if username_sudah_ada(username, abaikan_id=user_id):
        return False, "Username sudah dipakai!"

    conn = connection()
    try:
        with conn:
            if password:
                cur = conn.execute(
                    """UPDATE users
                       SET nama = ?, username = ?, password = ?
                       WHERE id = ? AND role = 'petugas'""",
                    (nama, username, password_encryption(password), user_id)
                )
            else:
                cur = conn.execute(
                    """UPDATE users
                       SET nama = ?, username = ?
                       WHERE id = ? AND role = 'petugas'""",
                    (nama, username, user_id)
                )

        if cur.rowcount == 0:
            return False, "Petugas tidak ditemukan!"

        return True, "Data petugas berhasil diubah!"

    except sqlite3.IntegrityError:
        return False, "Username sudah dipakai atau data tidak valid!"

    finally:
        conn.close()

def hapus_petugas(user_id):
    conn = connection()
    try:
        with conn:
            cur = conn.execute(
                "DELETE FROM users WHERE id = ? AND role = 'petugas'",
                (user_id,)
            )

        if cur.rowcount == 0:
            return False, "Petugas tidak ditemukan!"

        return True, "Petugas berhasil dihapus!"

    finally:
        conn.close()