import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import re

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название книги:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.author_entry = tk.Entry(self.root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.genre_entry = tk.Entry(self.root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.pages_entry = tk.Entry(self.root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления книги
        tk.Button(self.root, text="Добавить книгу", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица книг
        self.tree = ttk.Treeview(self.root, columns=("Автор", "Жанр", "Страниц"), show="headings")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страниц", text="Страниц")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Фильтры
        filter_frame = tk.Frame(self.root)
        filter_frame.grid(row=6, column=0, columnspan=2, pady=5)

        tk.Label(filter_frame, text="Фильтр по жанру:").pack(side="left", padx=5)
        self.genre_filter = ttk.Combobox(filter_frame, state="readonly")
        self.genre_filter.pack(side="left", padx=5)
        self.genre_filter.bind("<<ComboboxSelected>>", self.apply_filters)

        tk.Label(filter_frame, text="Страниц больше:").pack(side="left", padx=5)
        self.pages_filter = tk.Entry(filter_frame, width=6)
        self.pages_filter.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filters).pack(side="left", padx=5)

        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Сохранить данные", command=self.save_data).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Очистить список", command=self.clear_books).pack(side="left", padx=5)

        self.update_tree()
        self.update_filters()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if not pages.isdigit() or int(pages) <= 0:
            messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        self.books.append(book)
        self.update_tree()

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in self.books:
            self.tree.insert("", "end", values=(book["author"], book["genre"], book["pages"]))

    def apply_filters(self, event=None):
        genre = self.genre_filter.get()
        pages_str = self.pages_filter.get()

        filtered_books = self.books

        if genre and genre != "Все":
            filtered_books = [b for b in filtered_books if b["genre"] == genre]

        if pages_str.isdigit():
            pages_val = int(pages_str)
            filtered_books = [b for b in filtered_books if b["pages"] > pages_val]

        for i in self.tree.get_children():
            self.tree.delete(i)

        for book in filtered_books:
            self.tree.insert("", "end", values=(book["author"], book["genre"], book["pages"]))

    def update_filters(self):
        genres = sorted(set(b["genre"] for b in self.books))
        self.genre_filter["values"] = ["Все"] + genres
        self.genre_filter.set("Все")

    def save_data(self):
         data = {"books": self.books}
         with open("books_data.json", "w", encoding="utf-8") as f:
             json.dump(data, f, ensure_ascii=False, indent=4)
         messagebox.showinfo("Успех", "Данные сохранены в books_data.json")

    def load_data(self):
         if os.path.exists("books_data.json"):
             try:
                 with open("books_data.json", "r", encoding="utf-8") as f:
                     data = json.load(f)
                     self.books = data.get("books", [])
             except Exception as e:
                 messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {e}")

    def clear_books(self):
         if messagebox.askyesno("Подтверждение", "Очистить весь список книг?"):
             self.books = []
             self.update_tree()
             self.update_filters()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()