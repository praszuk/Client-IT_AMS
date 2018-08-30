import tkinter as tk
from tkinter import Label, Entry, Text, Button, N, S, E, W


class DocumentGeneratorView(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.protocol('WM_DELETE_WINDOW', self.withdraw)
        self.title('Protocol generator form')

        self.__check_out_date_label = Label(self, text='Checkout date: ')
        self.__check_out_date_label.grid(row=0, column=0)

        self.__check_out_date_entry = Entry(self)
        self.__check_out_date_entry.grid(row=0, column=1)

        self.__check_in_date_label = Label(self, text='Expected check-in date: ')
        self.__check_in_date_label.grid(row=1, column=0)

        self.__check_in_date_entry = Entry(self)
        self.__check_in_date_entry.grid(row=1, column=1)

        self.__middle_full_name_label = Label(self, text='Middle-man full name: ')
        self.__middle_full_name_label.grid(row=2, column=0)

        self.__middle_full_name_entry = Entry(self)
        self.__middle_full_name_entry.grid(row=2, column=1)

        self.__client_full_name_label = Label(self, text='Client full name: ')
        self.__client_full_name_label.grid(row=3, column=0)

        self.__client_full_name_entry = Entry(self)
        self.__client_full_name_entry.grid(row=3, column=1)

        self.__client_address_label = Label(self, text='Client address: ')
        self.__client_address_label.grid(row=4, column=0, columnspan=2)

        self.__client_address_text_area = Text(self, height=5)
        self.__client_address_text_area.grid(row=5, column=0, columnspan=2, sticky=N + S + E + W)

        self.__save_to_file_btn = Button(self, text='Save as...')
        self.__save_to_file_btn.grid(row=6, column=0, columnspan=2, sticky=N + S + E + W)

        # Properly expand whole grid
        col_size, row_size = self.grid_size()
        self.columnconfigure(tuple(range(col_size)), weight=1)
        self.rowconfigure(tuple(range(row_size)), weight=1)
