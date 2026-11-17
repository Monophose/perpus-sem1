import database

from petugas import petugas_dashboard
from admin import admin_dashboard

def login():
    while True:
        username = input("Masukkan Username: ")
        password = input("Masukkan Password: ")

        user = database.check_login(username, password)

        if user is None:
            print("\nIncorrect Credential\n")
            continue

        user_id, nama, username, role = user

        if role == "admin":
            admin_dashboard(username)

        elif role == "petugas":
            petugas_dashboard(username)

def main():
    database.default_data()
    login()

if __name__ == "__main__":
    main()