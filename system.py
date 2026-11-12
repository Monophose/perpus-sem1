from database import check_login

from petugas import petugas_dashboard
from admin import admin_dashboard

def login():
    while True:
        username = input("Masukkan Username: ")
        password = input("Masukkan Password: ")

        user = check_login(username, password)

        if user is None:
            print("\nIncorrect Credential\n")
            continue

        user_id, nama, username, role = user

        if role == "admin":
            admin_dashboard()

        elif role == "petugas":
            petugas_dashboard()