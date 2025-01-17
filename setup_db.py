import sqlite3

def setup_database():
    conn = sqlite3.connect('hotel_system.db')
    cursor = conn.cursor()

    # Drop existing tables to refresh schema
    cursor.execute('DROP TABLE IF EXISTS bookings')
    cursor.execute('DROP TABLE IF EXISTS rooms')
    cursor.execute('DROP TABLE IF EXISTS users')

    # Create users table
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Create rooms table
    cursor.execute('''
    CREATE TABLE rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number TEXT UNIQUE NOT NULL,
        room_type TEXT NOT NULL,
        price REAL NOT NULL,
        is_booked INTEGER DEFAULT 0
    )
    ''')

    # Create bookings table
    cursor.execute('''
    CREATE TABLE bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        room_number TEXT NOT NULL,
        room_type TEXT NOT NULL,
        price REAL NOT NULL,
        booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
