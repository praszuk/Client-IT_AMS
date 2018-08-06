import tkinter as tk
from tkinter import N, S, E, W, Button


class EditView(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.title('Input data')

        self.text_area = tk.Text(self, height=10, width=30)
        self.text_area.focus_set()
        self.text_area.grid(columnspan=2, sticky=N + S + E + W)

        self.ok_btn = Button(self, text='OK')
        self.cancel_btn = Button(self, text='Cancel')

        self.ok_btn.grid(column=0, row=1, sticky=N + S + E + W)
        self.cancel_btn.grid(column=1, row=1, sticky=N + S + E + W)

        self.grab_set()
        # Properly expand whole grid
        col_size, row_size = self.grid_size()
        self.columnconfigure(tuple(range(col_size)), weight=1)
        self.rowconfigure(tuple(range(row_size)), weight=1)
