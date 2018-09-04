import tkinter as tk

from Controller.MainViewController import Controller
from Util.Configuration import AppConfig

CONFIG = AppConfig()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
