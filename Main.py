import tkinter as tk

from Configuration import AppConfig
from Controller.MainViewController import Controller

CONFIG = AppConfig()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
