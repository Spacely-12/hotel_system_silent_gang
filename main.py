import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class HotelBookingSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Booking System")
        self.geometry("800x600")
        self.frames = {}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (MainPage, AdminLoginPage, AdminPage, UserPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Hotel Booking System", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=20)
        tk.Button(self, text="Admin", command=lambda: self.controller.show_frame("AdminLoginPage")).grid(row=1, column=0, padx=20, pady=10)
        tk.Button(self, text="User", command=lambda: self.controller.show_frame("UserPage")).grid(row=1, column=1, padx=20, pady=10)

class AdminLoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Admin Login", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=20)
        tk.Label(self, text="Username").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self, text="Password").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self, text="Login", command=self.admin_login).grid(row=3, column=0, columnspan=2, pady=20)
        tk.Button(self, text="Back to Main", command=lambda: self.controller.show_frame("MainPage")).grid(row=4, column=0, columnspan=2, pady=10)

    def admin_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin123":
            self.controller.show_frame("AdminPage")
        else:
            messagebox.showerror("Error", "Invalid admin credentials.")

class AdminPage(tk.Frame):
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
        tk.Button(self, text="View Available Rooms", command=self.view_available_rooms).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self, text="View Bookings", command=self.view_bookings).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Back to Main", command=lambda: self.controller.show_frame("MainPage")).grid(row=7, column=0, columnspan=2, pady=10)

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

    def view_available_rooms(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Available Rooms", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=20)

        conn = sqlite3.connect('hotel_system.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rooms WHERE is_booked = 0')
        rooms = cursor.fetchall()
        conn.close()

        for i, room in enumerate(rooms):
            room_info = f"Room Number: {room[1]}, Type: {room[2]}, Price: {room[3]}"
            tk.Label(self, text=room_info).grid(row=i+1, column=0, padx=10, pady=5)

        tk.Button(self, text="Back to Admin Page", command=self.create_widgets).grid(row=len(rooms)+1, column=0, columnspan=2, pady=20)

    def view_bookings(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="All Bookings", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=5, pady=20)
        
        # Add headers
        headers = ["Room Number", "Type", "Price", "Booking Date", "User"]
        for i, header in enumerate(headers):
            tk.Label(self, text=header, font=("Helvetica", 10, "bold")).grid(row=1, column=i, padx=10, pady=5)

        conn = sqlite3.connect('hotel_system.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT b.room_number, b.room_type, b.price, b.booking_date, u.username
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        ORDER BY b.booking_date DESC
        ''')
        bookings = cursor.fetchall()
        conn.close()

        if not bookings:
            tk.Label(self, text="No bookings found", font=("Helvetica", 10)).grid(row=2, column=0, columnspan=5, pady=20)
        else:
            for i, booking in enumerate(bookings, start=2):
                tk.Label(self, text=booking[0]).grid(row=i, column=0, padx=10, pady=5)
                tk.Label(self, text=booking[1]).grid(row=i, column=1, padx=10, pady=5)
                tk.Label(self, text=f"${booking[2]:.2f}").grid(row=i, column=2, padx=10, pady=5)
                tk.Label(self, text=booking[3]).grid(row=i, column=3, padx=10, pady=5)
                tk.Label(self, text=booking[4]).grid(row=i, column=4, padx=10, pady=5)

        row = len(bookings) + 2 if bookings else 3
        tk.Button(self, text="Back to Admin Page", 
                command=self.create_widgets).grid(row=row, column=0, columnspan=5, pady=20)

class UserPage(tk.Frame):
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
        try:
            # Store booking details
            cursor.execute('''
            INSERT INTO bookings (user_id, room_number, room_type, price)
            VALUES (?, ?, ?, ?)
            ''', (self.user_id, room[1], room[2], room[3]))
            
            # Remove room from available rooms
            cursor.execute('DELETE FROM rooms WHERE id = ?', (room[0],))
            conn.commit()
            messagebox.showinfo("Success", f"Room {room[1]} booked successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to book room: {e}")
        finally:
            conn.close()
            self.view_available_rooms()

    def view_booking_history(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Booking History", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=4, pady=20)
        
        # Add headers
        headers = ["Room Number", "Type", "Price", "Booking Date"]
        for i, header in enumerate(headers):
            tk.Label(self, text=header, font=("Helvetica", 10, "bold")).grid(row=1, column=i, padx=10, pady=5)

        conn = sqlite3.connect('hotel_system.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT room_number, room_type, price, booking_date
        FROM bookings
        WHERE user_id = ?
        ORDER BY booking_date DESC
        ''', (self.user_id,))
        bookings = cursor.fetchall()
        conn.close()

        if not bookings:
            tk.Label(self, text="No booking history found", font=("Helvetica", 10)).grid(row=2, column=0, columnspan=4, pady=20)
        else:
            for i, booking in enumerate(bookings, start=2):
                tk.Label(self, text=booking[0]).grid(row=i, column=0, padx=10, pady=5)
                tk.Label(self, text=booking[1]).grid(row=i, column=1, padx=10, pady=5)
                tk.Label(self, text=f"${booking[2]:.2f}").grid(row=i, column=2, padx=10, pady=5)
                tk.Label(self, text=booking[3]).grid(row=i, column=3, padx=10, pady=5)

        row = len(bookings) + 2 if bookings else 3
        tk.Button(self, text="Back to Available Rooms", 
                command=self.view_available_rooms).grid(row=row, column=0, columnspan=2, pady=20)
        tk.Button(self, text="Back to Main", 
                command=lambda: self.controller.show_frame("MainPage")).grid(row=row, column=2, columnspan=2, pady=20)

if __name__ == "__main__":
    app = HotelBookingSystem()
    app.mainloop()
