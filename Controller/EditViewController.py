from Model.EditViewModel import EditViewModel
from View.EditView import EditView


class EditViewController:
    def __init__(self, root):
        self.root = root

        self.__model = EditViewModel()
        self.__model.input_data.add_callback(self.__input_data_changed)

        self.__edit_view = EditView(self.root)
        self.__edit_view.withdraw()

        self.__edit_view.set_text(self.__model.get_text())  # set default text
        self.__edit_view.cancel_btn.config(command=self.__cancel_edit)
        self.__edit_view.ok_btn.config(command=self.__ok_edit)

    def open_view(self):
        self.__edit_view.deiconify()

    def __cancel_edit(self):
        self.__edit_view.set_text(self.__model.input_data.get())  # recently text
        self.__edit_view.withdraw()

    def __ok_edit(self):
        self.__model.set_text(self.__edit_view.get_text())
        self.__edit_view.withdraw()

    def __input_data_changed(self, text):
        print('Time to parse data from user')
        pass
        # self.parse_text()
        # self.main_view.update_tree_view()
