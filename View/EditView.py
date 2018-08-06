import tkinter as tk
from tkinter import N, S, E, W


class EditView(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

        self.text_area = tk.Text(self, height=10, width=30)
        self.text_area.focus_set()
        self.text_area.grid(sticky=N + S + E + W)

        self.grab_set()

        # Properly expand whole grid
        col_size, row_size = self.grid_size()
        self.columnconfigure(tuple(range(col_size)), weight=1)
        self.rowconfigure(tuple(range(row_size)), weight=1)
