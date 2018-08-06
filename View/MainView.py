import tkinter as tk
from tkinter import Button
from tkinter import N, S, E, W
from tkinter.ttk import Treeview


class MainView(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('Client - IT Assets Management System')

        # tree view as table
        self.tree = self.__create_tree_view()
        self.tree.grid(column=0, row=0, columnspan=4, rowspan=9, sticky=N + S + E + W)

        # Buttons row 2 for tree view, row 3 for action on assets in tree view
        self.btn_edit = Button(self, text='Edit')
        self.btn_refresh = Button(self, text='Refresh')

        self.btn_check_in = Button(self, text='Check-in', state='disabled')
        self.btn_checkout = Button(self, text='Checkout', state='disabled')
        self.btn_generate = Button(self, text='Generate', state='disabled')
        self.btn_exit = Button(self, text='Exit')

        self.btn_edit.grid(column=0, row=9, columnspan=2, sticky=N + S + E + W)
        self.btn_refresh.grid(column=2, row=9, columnspan=2, sticky=N + S + E + W)

        self.btn_check_in.grid(column=0, row=10, sticky=N + S + E + W)
        self.btn_checkout.grid(column=1, row=10, sticky=N + S + E + W)
        self.btn_generate.grid(column=2, row=10, sticky=N + S + E + W)
        self.btn_exit.grid(column=3, row=10, sticky=N + S + E + W)

        # Properly expand whole grid
        col_size, row_size = self.grid_size()
        self.columnconfigure(tuple(range(col_size)), weight=1)
        self.rowconfigure(tuple(range(row_size)), weight=1)

    def __create_tree_view(self):
        tree = tk.ttk.Treeview(self)

        tree['show'] = 'headings'

        tree["columns"] = ('ID', 'Asset Tag', 'Serial Number', 'Status')
        tree.column("ID", width=100)
        tree.column("Asset Tag", width=100)
        tree.column("Serial Number", width=100)
        tree.column("Status", width=100)

        tree.heading("ID", text="ID")
        tree.heading("Asset Tag", text="Asset Tag")
        tree.heading("Serial Number", text="Serial Number")
        tree.heading("Status", text="Status")

        return tree

    def update_tree_view(self):
        pass
