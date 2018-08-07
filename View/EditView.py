import tkinter as tk
from tkinter import N, S, E, W, END, Button


class EditView(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.protocol('WM_DELETE_WINDOW', self.withdraw)

        self.title('Input data')

        self.__text_area = tk.Text(self, height=10, width=30)
        self.__text_area.focus_set()
        self.__text_area.grid(columnspan=2, sticky=N + S + E + W)

        self.ok_btn = Button(self, text='OK')
        self.cancel_btn = Button(self, text='Cancel')

        self.ok_btn.grid(column=0, row=1, sticky=N + S + E + W)
        self.cancel_btn.grid(column=1, row=1, sticky=N + S + E + W)

        # Properly expand whole grid
        col_size, row_size = self.grid_size()
        self.columnconfigure(tuple(range(col_size)), weight=1)
        self.rowconfigure(tuple(range(row_size)), weight=1)

    def set_text(self, new_text):
        # '1.0' means BEGIN of text area like arr[0]
        self.__text_area.delete('1.0', END)
        self.__text_area.insert('1.0', new_text)
