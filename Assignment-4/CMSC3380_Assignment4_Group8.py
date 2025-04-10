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

def add_book(event=0):
    """Open a window to add a new book."""
    def submit(event=0):
        try:
            book_id = int(entry_id.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Book ID must be a number.", parent=window)
            return
        title = entry_title.get().strip()
        authors = entry_authors.get().strip()
        category = category_var.get()
        if not title or not authors:
            messagebox.showerror("Missing Information", "Please fill in all fields.", parent=window)
            return
        connect = sqlite3.connect(DB_FILE)
        c = connect.cursor()
        try:
            c.execute("INSERT INTO books (id, title, authors, category) VALUES (?,?,?,?)", 
                      (book_id, title, authors, category))
            connect.commit()
            messagebox.showinfo("Success", "Book added successfully!", parent=window)
            cancel()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "A book with that ID already exists.", parent=window)
        finally:
            connect.close()
    
    # used for pulling the root window back up when a toplevel is closed by hitting the x
    def cancel(event=0):
        root.deiconify()
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Add Book")
    
    # hide root, make active again on cancel/window close
    root.withdraw()
    window.protocol("WM_DELETE_WINDOW", cancel)
    
    # Book ID
    tk.Label(window, text = "Book ID:").grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "e")
    entry_id = tk.Entry(window)
    entry_id.grid(row = 0, column = 1, padx = 10, pady = 5)
    
    # Title
    tk.Label(window, text = "Title:").grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "e")
    entry_title = tk.Entry(window)
    entry_title.grid(row = 1, column = 1, padx = 10, pady = 5)
    
    # Authors
    tk.Label(window, text="Authors:").grid(row = 2, column = 0, padx = 10, pady = 5, sticky = "e")
    entry_authors = tk.Entry(window)
    entry_authors.grid(row = 2, column = 1, padx = 10, pady = 5)
    
    
    # Category selection using radio buttons.
    tk.Label(window, text = "Category:").grid(row = 3, column = 0, padx = 10, pady = 5, sticky = "e")
    category_var = tk.StringVar(value = "Computer Science")
    categories = [("Computer Science", "Computer Science"),
                  ("Science Fiction", "Science Fiction"),
                  ("Mystery", "Mystery"),
                  ("Other", "Other")]
    col = 1
    for text, value in categories:
      tk.Radiobutton(window, text = text, variable = category_var, value = value).grid(row=3, column = col, padx = 5, pady = 5)
      col += 1

    sub = tk.Button(window, text = "Submit", command = submit)
    sub.bind("<Return>", submit)
    sub.grid(row = 4, column = 0, columnspan = 2, pady = 10)
    canc = tk.Button(window, text = "Cancel", command = cancel)
    canc.bind("<Return>", cancel)
    canc.grid(row = 4, column = 1, columnspan = 2, pady = 10)

def update_book(event=0):
    """Open a window to update a book's details."""
    def load_book(event=0):
        try:
            bid = int(entry_search.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Book ID must be a number.", parent=window)
            return
        connect = sqlite3.connect(DB_FILE)
        c = connect.cursor()
        c.execute("SELECT * FROM books WHERE id=?", (bid,))
        row = c.fetchone()
        connect.close()
        if row is None:
            messagebox.showerror("Not Found", "No book found with the provided ID.", parent=window)
        else:
            # Pre-fill the fields with the current details.
            entry_title.delete(0, tk.END)
            entry_title.insert(0, row[1])
            entry_authors.delete(0, tk.END)
            entry_authors.insert(0, row[2])
            category_var.set(row[3])
            update_button.config(state="normal")

    def submit_update(event=0):
        try:
            bid = int(entry_search.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Book ID must be a number.", parent=window)
            return
        title = entry_title.get().strip()
        authors = entry_authors.get().strip()
        category = category_var.get()
        if not title or not authors:
            messagebox.showerror("Missing Information", "Please fill in all fields.", parent=window)
            return
        connect = sqlite3.connect(DB_FILE)
        c = connect.cursor()
        c.execute("UPDATE books SET title=?, authors=?, category=? WHERE id=?",
                  (title, authors, category, bid))
        if c.rowcount == 0:
            messagebox.showerror("Error", "No book was updated.", parent=window)
        else:
            connect.commit()
            messagebox.showinfo("Success", "Book updated successfully!", parent=window)
            cancel()
        connect.close()
        
    # used for pulling the root window back up when a toplevel is closed by hitting the x
    def cancel(event=0):
        root.deiconify()
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Update Book")
    
    # hide root, make active again on cancel/window close
    root.withdraw()
    window.protocol("WM_DELETE_WINDOW", cancel)

    # Search by Book ID to update.
    tk.Label(window, text="Enter Book ID to update:")\
        .grid(row = 0, column = 0, padx = 10, pady = 5, sticky = "e")
    entry_search = tk.Entry(window)
    entry_search.grid(row = 0, column = 1, padx = 10, pady = 5)
    load = tk.Button(window, text = "Load Book", command=load_book)
    load.grid(row = 0, column = 2, padx = 10, pady = 5)
    load.bind("<Return>", load_book)

    # Title field.
    tk.Label(window, text = "Title:")\
        .grid(row = 1, column = 0, padx = 10, pady = 5, sticky = "e")
    entry_title = tk.Entry(window)
    entry_title.grid(row = 1, column = 1, columnspan = 2, padx = 10, pady = 5)
    
    # Authors field.
    tk.Label(window, text = "Authors:")\
        .grid(row = 2, column = 0, padx = 10, pady = 5 , sticky = "e")
    entry_authors = tk.Entry(window)
    entry_authors.grid(row = 2, column = 1, columnspan = 2, padx = 10, pady = 5)
    
    # Category field.
    tk.Label(window, text = "Category:")\
        .grid(row = 3, column = 0, padx = 10, pady = 5, sticky = "e")
    category_var = tk.StringVar(value = "Computer Science")
    categories = [("Computer Science", "Computer Science"),
                  ("Science Fiction", "Science Fiction"),
                  ("Mystery", "Mystery"),
                  ("Other", "Other")]
    col = 1
    for text, value in categories:
      tk.Radiobutton(window, text = text, variable = category_var, value = value).grid(row = 3, column = col, padx = 5, pady = 5)
      col += 1

    update_button = tk.Button(window, text = "Update Book", command=submit_update, state="disabled")
    update_button.grid(row=4, column=0, columnspan=3, pady=10)
    update_button.bind("<Return>", submit_update)
    canc = tk.Button(window, text = "Cancel", command = cancel)
    canc.grid(row = 4, column = 1, columnspan = 3, pady = 10)
    canc.bind("<Return>", cancel)

def delete_book(event=0):
    """Open a window to delete a book."""
    def submit_delete(event=0):
        try:
            bid = int(entry_id.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Book ID must be a number.", parent=window)
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?", parent=window)
        if confirm:
            connect = sqlite3.connect(DB_FILE)
            c = connect.cursor()
            c.execute("DELETE FROM books WHERE id=?", (bid,))
            if c.rowcount == 0:
                messagebox.showerror("Error", "No book found with that ID.", parent=window)
            else:
                connect.commit()
                messagebox.showinfo("Success", "Book deleted successfully!", parent=window)
                cancel()
            connect.close()

    # used for pulling the root window back up when a toplevel is closed by hitting the x
    def cancel(event=0):
        root.deiconify()
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Delete Book")
    
    # hide root, make active again on cancel/window close
    root.withdraw()
    window.protocol("WM_DELETE_WINDOW", cancel)
    
    tk.Label(window, text="Enter Book ID to delete:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_id = tk.Entry(window)
    entry_id.grid(row=0, column=1, padx=10, pady=5)
    dele = tk.Button(window, text="Delete", command=submit_delete)
    dele.grid(row=1, column=0, columnspan=2, pady=10)
    dele.bind("<Return>", submit_delete)
    canc = tk.Button(window, text = "Cancel", command = cancel)
    canc.grid(row = 1, column = 1, columnspan = 2, pady = 10)
    canc.bind("<Return>", cancel)

def list_books(event=0):
    """Open a window to list all defined books using a Treeview widget."""
    
    # used for pulling the root window back up when a toplevel is closed by hitting the x
    def cancel(event=0):
        root.deiconify()
        window.destroy()

    window = tk.Toplevel(root)
    window.title("List of Books")
    
    # hide root, make active again on cancel/window close
    root.withdraw()
    window.protocol("WM_DELETE_WINDOW", cancel)
    
    tree = ttk.Treeview(window, columns=("ID", "Title", "Authors", "Category"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Authors", text="Authors")
    tree.heading("Category", text="Category")
    
    tree.column("ID", width=50)
    tree.column("Title", width=200)
    tree.column("Authors", width=150)
    tree.column("Category", width=100)
    
    # Adding a scrollbar for convenience.
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    tree.pack(fill=tk.BOTH, expand=True)
    
    # Cancel button
    canc = tk.Button(window, text = "Cancel", command = cancel)
    canc.pack(side='right', padx=10, pady=10)
    canc.bind("<Return>", cancel)
    
    connect = sqlite3.connect(DB_FILE)
    c = connect.cursor()
    c.execute("SELECT * FROM books")
    rows = c.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    connect.close()

# handler for quit button
def quit_program(event=0):
    root.destroy()

# Main window for the application.
root = tk.Tk()
root.title("Book Manager")

# Initialize database and insert sample books.
init_db()
insert_sample_books()

# Create the main menu buttons.
# (named for bindings)
add = tk.Button(root, text="Add Book", width=20, command=add_book)
add.pack(pady=5)
add.bind("<Return>", add_book)
update = tk.Button(root, text="Update Book", width=20, command=update_book)
update.pack(pady=5)
update.bind("<Return>", update_book)
delete = tk.Button(root, text="Delete Book", width=20, command=delete_book)
delete.pack(pady=5)
delete.bind("<Return>", delete_book)
list = tk.Button(root, text="List Books", width=20, command=list_books)
list.pack(pady=5)
list.bind("<Return>", list_books)
quit = tk.Button(root, text="Quit", width=20, command=quit_program)
quit.pack(pady=5)
quit.bind("<Return>", quit_program)

root.mainloop()
