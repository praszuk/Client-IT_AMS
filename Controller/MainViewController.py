from sys import exit

from Controller.DocumentGeneratorController import DocumentGeneratorController
from Controller.EditViewController import EditViewController
from Model.AssetListModel import AssetListModel
from Model.CheckoutModel import CheckoutModel
from View.MainView import MainView


class Controller:
    def __init__(self, root):
        self.root = root
        self.assets = AssetListModel()

        self.checkout_model = CheckoutModel()
        self.main_view = MainView(root, self.assets)

        self.main_view.btn_edit.config(command=self.__edit_view_launcher)
        self.main_view.btn_generate.config(command=self.__document_generator_view_launcher)
        self.main_view.btn_refresh.config(command=self.__refresh_assets)
        self.main_view.btn_exit.config(command=Controller.__close_app)

        self.assets.data.add_callback(self.main_view.update_tree_view)

        self.edit_view_controller = EditViewController(self.main_view, self.assets)
        self.doc_gen_controller = DocumentGeneratorController(self.main_view, self.checkout_model, self.assets)

    def __edit_view_launcher(self):
        self.edit_view_controller.open_view()

    def __document_generator_view_launcher(self):
        self.doc_gen_controller.open_view()

    def __refresh_assets(self):
        serials = [asset.serial_number for asset in self.assets]
        self.assets.replace(self.edit_view_controller.update_assets(serials))

    @staticmethod
    def __close_app():
        exit(0)
