import tkinter as tk

from Controller.Controller import Controller

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
