import tkinter as tk
from tkinter import messagebox
import mysql.connector

class LibraryManagementSystem:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("700x500")
        self.root.config(bg="violet")

        # Database
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="library"
        )
        self.create_tables()

        # GUI Components
        self.label_title = tk.Label(root, text="Library Management System", font=("Helvetica", 16))
        self.label_title.place(x=200,y=10)

        # Login Section
        self.label_username = tk.Label(root, text="Username:")
        self.label_username.place(x=100,y=50)
        self.entry_username = tk.Entry(root)
        self.entry_username.place(x=200,y=50)

        self.label_password = tk.Label(root, text="Password:")
        self.label_password.place(x=100,y=90)
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.place(x=200,y=90)

        self.btn_login = tk.Button(root, text="Login", command=self.login)
        self.btn_login.place(x=120,y=120)

        # Register Section
        self.btn_register = tk.Button(root, text="Register", command=self.register)
        self.btn_register.place(x=210,y=120)

        # Book Management Section
        self.label_management_title = tk.Label(root, text="Book Management:")
        self.label_management_title.place(x=100,y=180)

        #Add_Book
        self.btn_add_book = tk.Button(root, text="Add Book", command=self.add_book)
        self.btn_add_book.place(x=100,y=220)

        self.label_book_title = tk.Label(root, text="Book title:")
        self.label_book_title.place(x=200, y=220)
        self.entry_book_title = tk.Entry(root)
        self.entry_book_title.place(x=270, y=220)

        self.label_author = tk.Label(root, text="Author:")
        self.label_author.place(x=400, y=220)
        self.entry_author= tk.Entry(root)
        self.entry_author.place(x=450, y=220)

        #View_Book
        self.btn_view_books = tk.Button(root, text="View Books", command=self.view_books)
        self.btn_view_books.place(x=100,y=280)

        #Issue_Book
        self.btn_issue_book = tk.Button(root, text="Issue Book", command=self.issue_book)
        self.btn_issue_book.place(x=100,y=340)
        self.label_issue_book = tk.Label(root, text="Issue BookID:")
        self.label_issue_book.place(x=200, y=340)
        self.entry_issue_id = tk.Entry(root)
        self.entry_issue_id.place(x=280, y=340)

        #Remove_Book
        self.btn_remove_book = tk.Button(root, text="Remove Book", command=self.remove_book)
        self.btn_remove_book.place(x=100,y=400)
        self.label_remove_book = tk.Label(root, text="Remove BookID:")
        self.label_remove_book.place(x=200, y=400)
        self.entry_remove_id = tk.Entry(root)
        self.entry_remove_id.place(x=300, y=400)

        #Exit
        self.btn_exit = tk.Button(root, text="LogOut", command=root.destroy)
        self.btn_exit.place(x=100,y=460)

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                          (id INT AUTO_INCREMENT PRIMARY KEY,
                           username VARCHAR(255) UNIQUE,
                           password VARCHAR(255))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                          (id INT AUTO_INCREMENT PRIMARY KEY,
                           title VARCHAR(255),
                           author VARCHAR(255),
                           status VARCHAR(10) DEFAULT 'Available')''')
        self.conn.commit()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get();

        if username and password:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Success", f"Welcome, {username}!")
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

    def register(self):
        new_username = self.entry_username.get()
        new_password = self.entry_password.get()

        if new_username and new_password:
            cursor = self.conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, new_password))
                self.conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        else:
            messagebox.showerror("Error", "Please enter both new username and password.")

    def add_book(self):
        title = self.entry_book_title.get()
        author = self.entry_author.get()

        if title and author:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
            self.conn.commit()
            messagebox.showinfo("Success", "Book added successfully!")
        else:
            messagebox.showerror("Error", "Please enter both book title and author.")

    def view_books(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        if books:
            result_text = ""
            for book in books:
                result_text += f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {book[3]}\n"
            messagebox.showinfo("Books", result_text)
        else:
            messagebox.showinfo("Books", "No books available.")

    def issue_book(self):
        book_id = self.entry_issue_id.get()

        if book_id:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE books SET status='Issued' WHERE id=%s", (book_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Book issued successfully!")
        else:
            messagebox.showerror("Error", "Please enter the book ID.")

    def remove_book(self):
        book_id = self.entry_remove_id.get()

        if book_id:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Book removed successfully!")
        else:
            messagebox.showerror("Error", "Please enter the book ID.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()