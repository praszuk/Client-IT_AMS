from Controller.EditViewController import EditViewController
from View.MainView import MainView


class Controller:
    def __init__(self, root):
        self.root = root

        self.main_view = MainView(root)
        self.main_view.btn_edit.config(command=self.__edit_view_launcher)

        self.edit_view_controller = EditViewController(self.main_view)

    def __edit_view_launcher(self):
        self.edit_view_controller.open_view()
