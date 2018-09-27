import logging
import tkinter as tk

from Controller.MainViewController import Controller
from Util.AutoUpdate import AutoUpdate
from Util.Configuration import AppConfig

CONFIG = AppConfig()
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    AutoUpdate.is_up_to_date()

    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
