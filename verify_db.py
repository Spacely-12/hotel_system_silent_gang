import sqlite3

def verify_database():
    conn = sqlite3.connect('hotel_system.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    users_table = cursor.fetchone()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rooms'")
    rooms_table = cursor.fetchone()

    conn.close()

    if users_table and rooms_table:
        print("Tables 'users' and 'rooms' exist in the database.")
    else:
        print("Tables 'users' and/or 'rooms' do not exist in the database.")

if __name__ == "__main__":
    verify_database()
