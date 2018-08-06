import tkinter as tk


class EditView(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.text_area = tk.Text(self, height=10, width=30)
        self.text_area.focus_set()
        self.text_area.grab_set()
        self.text_area.grid()
