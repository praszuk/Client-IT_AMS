import tkinter as tk

from Configuration import AppConfig
from Controller.MainViewController import Controller
from View.DocumentGeneratorView import DocumentGeneratorView

CONFIG = AppConfig()

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    DocumentGeneratorView(root)
    app = Controller(root)
    root.mainloop()
