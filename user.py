import tkinter as tk
from tkinter import messagebox
import sqlite3

class UserInterface(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="User - Hotel Booking", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self, text="Username").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self, text="Password").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=20)
        tk.Button(self, text="Register", command=self.register).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Back to Main", command=lambda: self.controller.show_frame("MainPage")).grid(row=5, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('hotel_system.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
        ''', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.user_id = user[0]
            messagebox.showinfo("Login", f"User {username} logged in successfully.")
            self.view_available_rooms()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('hotel_system.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
            ''', (username, password))
            conn.commit()
            messagebox.showinfo("Register", f"User {username} registered successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        conn.close()

    def view_available_rooms(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Available Rooms", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=20)

        conn = sqlite3.connect('hotel_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rooms')
        rooms = cursor.fetchall()
        conn.close()

        for i, room in enumerate(rooms):
            room_info = f"Room Number: {room[1]}, Type: {room[2]}, Price: {room[3]}"
            tk.Label(self, text=room_info).grid(row=i+1, column=0, padx=10, pady=5)
            book_button = tk.Button(self, text="Book", command=lambda r=room: self.book_room(r))
            book_button.grid(row=i+1, column=1, padx=10, pady=5)

        tk.Button(self, text="View Booking History", command=self.view_booking_history).grid(row=len(rooms)+1, column=0, columnspan=2, pady=20)
        tk.Button(self, text="Back to Main", command=lambda: self.controller.show_frame("MainPage")).grid(row=len(rooms)+2, column=0, columnspan=2, pady=10)

    def book_room(self, room):
        conn = sqlite3.connect('hotel_system.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO bookings (user_id, room_id) VALUES (?, ?)
        ''', (self.user_id, room[0]))
        cursor.execute('''
        DELETE FROM rooms WHERE id = ?
        ''', (room[0],))
        conn.commit()
        conn.close()
        messagebox.showinfo("Room Booked", f"Room {room[1]} booked successfully.")
        self.view_available_rooms()

    def view_booking_history(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Booking History", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=20)

        conn = sqlite3.connect('hotel_system.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT rooms.room_number, rooms.room_type, rooms.price, bookings.booking_date
        FROM bookings
        JOIN rooms ON bookings.room_id = rooms.id
        WHERE bookings.user_id = ?
        ''', (self.user_id,))
        bookings = cursor.fetchall()
        conn.close()

        for i, booking in enumerate(bookings):
            booking_info = f"Room Number: {booking[0]}, Type: {booking[1]}, Price: {booking[2]}, Date: {booking[3]}"
            tk.Label(self, text=booking_info).grid(row=i+1, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self, text="Back to Available Rooms", command=self.view_available_rooms).grid(row=len(bookings)+1, column=0, columnspan=2, pady=20)
        tk.Button(self, text="Back to Main", command=lambda: self.controller.show_frame("MainPage")).grid(row=len(bookings)+2, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()

