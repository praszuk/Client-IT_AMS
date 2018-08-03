from Model.Model import Model
from View.MainView import MainView


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.main_view = MainView(root)
