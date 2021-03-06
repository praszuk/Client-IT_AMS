import tkinter as tk
from tkinter import Button
from tkinter import N, S, E, W
from tkinter.ttk import Treeview


class MainView(tk.Toplevel):
    def __init__(self, master, assets):
        self.assets = assets

        tk.Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.title('Client - IT Assets Management System')

        # tree view as table
        self.tree = self.__create_tree_view()
        self.tree.grid(column=0, row=0, columnspan=4, rowspan=9, sticky=N + S + E + W)

        # Buttons below tree view
        self.btn_edit = Button(self, text='Edit')

        self.btn_auto_add = Button(self, text='Auto-add', state='disabled')
        self.btn_refresh = Button(self, text='Refresh')

        self.btn_check_in = Button(self, text='Check-in all')
        self.btn_checkout = Button(self, text='Checkout', state='disabled')
        self.btn_generate = Button(self, text='Generate', state='disabled')
        self.btn_exit = Button(self, text='Exit')

        self.btn_edit.grid(column=0, row=9, columnspan=4, sticky=N + S + E + W)

        self.btn_auto_add.grid(column=0, row=10, columnspan=2, sticky=N + S + E + W)
        self.btn_refresh.grid(column=2, row=10, columnspan=2, sticky=N + S + E + W)

        self.btn_check_in.grid(column=0, row=11, sticky=N + S + E + W)
        self.btn_checkout.grid(column=1, row=11, sticky=N + S + E + W)
        self.btn_generate.grid(column=2, row=11, sticky=N + S + E + W)
        self.btn_exit.grid(column=3, row=11, sticky=N + S + E + W)

        # Properly expand whole grid
        col_size, row_size = self.grid_size()
        self.columnconfigure(tuple(range(col_size)), weight=1)
        self.rowconfigure(tuple(range(row_size)), weight=1)

    def __create_tree_view(self):
        tree = tk.ttk.Treeview(self)

        tree['show'] = 'headings'

        tree["columns"] = ('ID', 'Asset Name', 'Serial Number', 'Status', 'Notes')
        tree.column("ID", width=50)
        tree.column("Asset Name", width=150)
        tree.column("Serial Number", width=150)
        tree.column("Status", width=150)
        tree.column("Notes", width=200)

        tree.heading("ID", text="ID")
        tree.heading("Asset Name", text="Asset Name")
        tree.heading("Serial Number", text="Serial Number")
        tree.heading("Status", text="Status")
        tree.heading("Notes", text="Notes")

        return tree

    def update_tree_view(self):
        # Clear table
        self.tree.delete(*self.tree.get_children())

        # Fill with new rows
        for asset in self.assets:
            self.tree.insert('', 'end', values=(asset.id,
                                                asset.name,
                                                asset.serial_number,
                                                asset.status.name,
                                                asset.notes))

        if len(self.assets) > 0:
            self.btn_generate.configure(state='normal')
        else:
            self.btn_generate.configure(state='disabled')
