import tkinter as tk
from tkinter.ttk import Treeview


class MainView(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)

        tree = tk.ttk.Treeview(self)
        tree['show'] = 'headings'
        tree["columns"] = ("one", "two", "three")
        tree.column("one", width=20)
        tree.column("two", width=100)
        tree.column("three", width=100)

        tree.heading("one", text="ID")
        tree.heading("two", text="Asset TAG")
        tree.heading("three", text="Serial Number")

        for i in range(20):
            tree.insert("", i, values=("a{}".format(i), "b", "c"))

        for child in tree.get_children():
            if tree.item(child)["values"][1] == 'b':
                tree.set(child, '1', 'd')

        tree.pack()
