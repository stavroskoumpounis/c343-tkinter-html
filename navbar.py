import tkinter as tk
from tkinter import PhotoImage


class Navbar(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.logo = PhotoImage(file="logo.png").subsample(3, 3)  # Adjust the subsample values to resize the logo
        self.logo_container = tk.Label(self, bg="lightblue")
        self.logo_label = tk.Label(self.logo_container, image=self.logo, bg="lightblue")
        self.logo_label.pack()
        self.logo_container.pack(side=tk.LEFT, padx=5)

        self.menu_entry = tk.Entry(self)
        self.menu_entry.insert(0, "Menu")
        self.menu_entry.config(state="readonly")
        self.menu_entry.pack(side=tk.LEFT, padx=5)

        self.about_entry = tk.Entry(self)
        self.about_entry.insert(0, "About")
        self.about_entry.config(state="readonly")
        self.about_entry.pack(side=tk.LEFT, padx=5)

        self.dynamic_entries_frame = tk.Frame(self)
        self.dynamic_entries_frame.pack(side=tk.LEFT, padx=5)

        self.add_btn = tk.Button(self, text="+", command=self.add_entry)
        self.add_btn.pack(side=tk.RIGHT, anchor="e", padx=5)

        self.additional_entries = []

    def add_entry(self):
        if len(self.additional_entries) < 2:
            new_entry = tk.Entry(self.dynamic_entries_frame)
            new_entry.insert(0, f"Entry {len(self.additional_entries) + 1}")
            new_entry.pack(side=tk.LEFT, padx=5)
            new_entry.focus_set()
            new_entry.bind("<FocusOut>", lambda _: new_entry.config(state="readonly"))
            self.additional_entries.append(new_entry)
        else:
            print("Maximum number of entries reached")
