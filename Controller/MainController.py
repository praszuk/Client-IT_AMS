from Model.Model import Model
from View.EditView import EditView
from View.MainView import MainView


class Controller:
    def __init__(self, root):
        self.root = root

        self.model = Model()
        self.model.input_data.add_callback(self.input_data_changed)

        self.main_view = MainView(root)
        self.main_view.btn_edit.config(command=self.edit_input)

    def input_data_changed(self, text):
        pass
        # self.parse_text()
        # self.main_view.update_tree_view()

    def edit_input(self):
        edit_view = EditView(self.root)
