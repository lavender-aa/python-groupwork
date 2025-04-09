import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Name of the SQLite database file.
DB_FILE = "books.db"

def init_db():
    """Initialize the database and create the books table if it doesn't exist."""
    connect = sqlite3.connect(DB_FILE)
    c = connect.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            authors TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)
    connect.commit()
    connect.close()

def insert_sample_books():
    """
    Insert sample books into the database if there are less than 5 books.
    This ensures that when the program starts, there is already some content.
    """
    connect = sqlite3.connect(DB_FILE)
    c = connect.cursor()
    c.execute("SELECT COUNT(*) FROM books")
    count = c.fetchone()[0]
    if count < 5:
        sample_books = [
            (1, "Python Programming", "John Doe", "Computer Science"),
            (2, "The Sci-Fi Odyssey", "Jane Smith", "Science Fiction"),
            (3, "Mystery of the Lost Key", "Alan Smithee", "Mystery"),
            (4, "Learning SQL", "Alice Brown", "Computer Science"),
            (5, "Adventure Beyond", "Bob Builder", "Other")
        ]
        for book in sample_books:
            try:
                c.execute("INSERT INTO books (id, title, authors, category) VALUES (?,?,?,?)", book)
            except sqlite3.IntegrityError:
                # Skip insertion if the id already exists.
                pass
        connect.commit()
    connect.close()

def add_book():
    """Open a window to add a new book."""
    def submit():
        try:
            book_id = int(entry_id.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Book ID must be a number.")
            return
        title = entry_title.get().strip()
        authors = entry_authors.get().strip()
        category = category_var.get()
        if not title or not authors:
            messagebox.showerror("Missing Information", "Please fill in all fields.")
            return
        connect = sqlite3.connect(DB_FILE)
        c = connect.cursor()
        try:
            c.execute("INSERT INTO books (id, title, authors, category) VALUES (?,?,?,?)", 
                      (book_id, title, authors, category))
            connect.commit()
            messagebox.showinfo("Success", "Book added successfully!")
            window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "A book with that ID already exists.")
        finally:
            connect.close()

    window = tk.Toplevel(root)
    window.title("Add Book")
    
    # Book ID
    tk.Label(window, text="Book ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_id = tk.Entry(window)
    entry_id.grid(row=0, column=1, padx=10, pady=5)
    
    # Title
    tk.Label(window, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_title = tk.Entry(window)
    entry_title.grid(row=1, column=1, padx=10, pady=5)
    
    # Authors
    tk.Label(window, text="Authors:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_authors = tk.Entry(window)
    entry_authors.grid(row=2, column=1, padx=10, pady=5)
    
    # Category selection using radio buttons.
    tk.Label(window, text="Category:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    category_var = tk.StringVar(value="Computer Science")
    categories = [("Computer Science", "Computer Science"),
                  ("Science Fiction", "Science Fiction"),
                  ("Mystery", "Mystery"),
                  ("Other", "Other")]
    col = 1
    for text, value in categories:
        tk.Radiobutton(window, text=text, variable=category_var, value=value)\
            .grid(row=3, column=col, padx=5, pady=5)
        col += 1

    tk.Button(window, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

def update_book():
    """Open a window to update a book's details."""
    def load_book():
        try:
            bid = int(entry_search.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Book ID must be a number.")
            return
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM books WHERE id=?", (bid,))
        row = c.fetchone()
        conn.close()
        if row is None:
            messagebox.showerror("Not Found", "No book found with the provided ID.")
        else:
            # Pre-fill the fields with the current details.
            entry_title.delete(0, tk.END)
            entry_title.insert(0, row[1])
            entry_authors.delete(0, tk.END)
            entry_authors.insert(0, row[2])
            category_var.set(row[3])
            update_button.config(state="normal")

    def submit_update():
        try:
            bid = int(entry_search.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Book ID must be a number.")
            return
        title = entry_title.get().strip()
        authors = entry_authors.get().strip()
        category = category_var.get()
        if not title or not authors:
            messagebox.showerror("Missing Information", "Please fill in all fields.")
            return
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("UPDATE books SET title=?, authors=?, category=? WHERE id=?",
                  (title, authors, category, bid))
        if c.rowcount == 0:
            messagebox.showerror("Error", "No book was updated.")
        else:
            conn.commit()
            messagebox.showinfo("Success", "Book updated successfully!")
            window.destroy()
        conn.close()
        
    window = tk.Toplevel(root)
    window.title("Update Book")

    # Search by Book ID to update.
    tk.Label(window, text="Enter Book ID to update:")\
        .grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_search = tk.Entry(window)
    entry_search.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(window, text="Load Book", command=load_book)\
        .grid(row=0, column=2, padx=10, pady=5)

    # Title field.
    tk.Label(window, text="Title:")\
        .grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_title = tk.Entry(window)
    entry_title.grid(row=1, column=1, columnspan=2, padx=10, pady=5)
    
    # Authors field.
    tk.Label(window, text="Authors:")\
        .grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_authors = tk.Entry(window)
    entry_authors.grid(row=2, column=1, columnspan=2, padx=10, pady=5)
    
    # Category field.
    tk.Label(window, text="Category:")\
        .grid(row=3, column=0, padx=10, pady=5, sticky="e")
    category_var = tk.StringVar(value="Computer Science")
    categories = [("Computer Science", "Computer Science"),
                  ("Science Fiction", "Science Fiction"),
                  ("Mystery", "Mystery"),
                  ("Other", "Other")]
    col = 1
    for text, value in categories:
        tk.Radiobutton(window, text=text, variable=category_var, value=value)\
            .grid(row=3, column=col, padx=5, pady=5)
        col += 1

    update_button = tk.Button(window, text="Update Book", command=submit_update, state="disabled")
    update_button.grid(row=4, column=0, columnspan=3, pady=10)

def delete_book():
    """Open a window to delete a book."""
    def submit_delete():
        try:
            bid = int(entry_id.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Book ID must be a number.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?")
        if confirm:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("DELETE FROM books WHERE id=?", (bid,))
            if c.rowcount == 0:
                messagebox.showerror("Error", "No book found with that ID.")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Book deleted successfully!")
                window.destroy()
            conn.close()

    window = tk.Toplevel(root)
    window.title("Delete Book")
    tk.Label(window, text="Enter Book ID to delete:")\
        .grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_id = tk.Entry(window)
    entry_id.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(window, text="Delete", command=submit_delete)\
        .grid(row=1, column=0, columnspan=2, pady=10)

def list_books():
    """Open a window to list all defined books using a Treeview widget."""
    window = tk.Toplevel(root)
    window.title("List of Books")
    
    tree = ttk.Treeview(window, columns=("ID", "Title", "Authors", "Category"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Authors", text="Authors")
    tree.heading("Category", text="Category")
    
    tree.column("ID", width=50)
    tree.column("Title", width=200)
    tree.column("Authors", width=150)
    tree.column("Category", width=100)
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Adding a scrollbar for convenience.
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

# Main window for the application.
root = tk.Tk()
root.title("Book Manager")

# Initialize database and insert sample books.
init_db()
insert_sample_books()

# Create the main menu buttons.
tk.Button(root, text="Add Book", width=20, command=add_book).pack(pady=5)
tk.Button(root, text="Update Book", width=20, command=update_book).pack(pady=5)
tk.Button(root, text="Delete Book", width=20, command=delete_book).pack(pady=5)
tk.Button(root, text="List Books", width=20, command=list_books).pack(pady=5)

root.mainloop()
