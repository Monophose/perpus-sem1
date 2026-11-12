import database
from system import login

def main():
    database.default_data()
    login()

if __name__ == "__main__":
    main()