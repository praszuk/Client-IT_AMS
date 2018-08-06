from Model.Model import Model
from View.EditView import EditView


class EditViewController:
    def __init__(self, root):
        self.root = root

        self.__edit_view_model = Model()
        self.__edit_view_model.input_data.add_callback(self.__input_data_changed)
        self.__edit_view = EditView(self.root)
        self.__edit_view.withdraw()

    def open_view(self):
        self.__edit_view.deiconify()

    def __input_data_changed(self, text):
        pass
        # self.parse_text()
        # self.main_view.update_tree_view()
