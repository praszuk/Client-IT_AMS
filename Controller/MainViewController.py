from Controller.DocumentGeneratorController import DocumentGeneratorController
from Controller.EditViewController import EditViewController
from Model.CheckoutModel import CheckoutModel
from View.MainView import MainView


class Controller:
    def __init__(self, root):
        self.root = root
        self.assets = []

        self.checkout_model = CheckoutModel()
        self.main_view = MainView(root)
        self.main_view.btn_edit.config(command=self.__edit_view_launcher)
        self.main_view.btn_generate.config(command=self.__document_generator_view_launcher)

        self.edit_view_controller = EditViewController(self.main_view, self.assets)
        self.doc_gen_controller = DocumentGeneratorController(self.main_view, self.checkout_model, self.assets)

    def __edit_view_launcher(self):
        self.edit_view_controller.open_view()

    def __document_generator_view_launcher(self):
        self.doc_gen_controller.open_view()
