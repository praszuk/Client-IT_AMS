from Model.Model import Model
from View.View import MainView


class Controller:
    def __init__(self, root):
        self.model = Model()
        self.main_view = MainView(root)
