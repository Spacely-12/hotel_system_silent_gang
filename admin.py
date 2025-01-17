import tkinter as tk
from tkinter import messagebox
import sqlite3

class AdminInterface(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Admin - Add Rooms", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self, text="Room Number").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.room_number_entry = tk.Entry(self)
        self.room_number_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self, text="Room Type").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.room_type_entry = tk.Entry(self)
        self.room_type_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(self, text="Price").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self, text="Add Room", command=self.add_room).grid(row=4, column=0, columnspan=2, pady=20)
        tk.Button(self, text="View Bookings", command=self.view_bookings).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Back to Main", command=lambda: self.controller.show_frame("MainPage")).grid(row=6, column=0, columnspan=2, pady=10)

    def add_room(self):
        room_number = self.room_number_entry.get()
        room_type = self.room_type_entry.get()
        price = self.price_entry.get()

        conn = sqlite3.connect('hotel_system.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO rooms (room_number, room_type, price)
            VALUES (?, ?, ?)
            ''', (room_number, room_type, price))
            conn.commit()
            messagebox.showinfo("Room Added", f"Room {room_number} added successfully.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Room number already exists.")
        conn.close()

    def view_bookings(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="All Bookings", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=20)

        conn = sqlite3.connect('hotel_system.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT rooms.room_number, rooms.room_type, rooms.price, bookings.booking_date, users.username
        FROM bookings
        JOIN rooms ON bookings.room_id = rooms.id
        JOIN users ON bookings.user_id = users.id
        ''')
        bookings = cursor.fetchall()
        conn.close()

        for i, booking in enumerate(bookings):
            booking_info = f"Room Number: {booking[0]}, Type: {booking[1]}, Price: {booking[2]}, Date: {booking[3]}, User: {booking[4]}"
            tk.Label(self, text=booking_info).grid(row=i+1, column=0, columnspan=2, padx=10, pady=5)

        tk.Button(self, text="Back to Main", command=lambda: self.controller.show_frame("MainPage")).grid(row=len(bookings)+1, column=0, columnspan=2, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminInterface(root)
    root.mainloop()
