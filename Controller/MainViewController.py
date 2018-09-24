import logging
import webbrowser
from sys import exit

from Controller.DocumentGeneratorController import DocumentGeneratorController
from Controller.EditViewController import EditViewController
from Controller.StockAPIController import StockAPIController
from Model.AssetListModel import AssetListModel
from Model.AssetStatusModel import AssetStatus
from Model.CheckoutModel import CheckoutModel
from View.MainView import MainView


class Controller:
    def __init__(self, root):
        self.root = root

        self.assets = AssetListModel()
        self.assets_to_add = AssetListModel()

        self.checkout_model = CheckoutModel()
        self.main_view = MainView(root, self.assets)

        self.main_view.tree.bind('<<TreeviewSelect>>', self.__on_select)
        self.main_view.tree.bind('<Double-Button-1>', self.__open_browser)

        self.main_view.btn_auto_add.config(command=self.__auto_add)
        self.main_view.btn_check_in.config(command=self.__check_in)
        self.main_view.btn_edit.config(command=self.__edit_view_launcher)
        self.main_view.btn_generate.config(command=self.__document_generator_view_launcher)
        self.main_view.btn_refresh.config(command=self.__refresh_assets)
        self.main_view.btn_exit.config(command=Controller.__close_app)

        self.assets.data.add_callback(self.main_view.update_tree_view)

        self.edit_view_controller = EditViewController(self.main_view, self.assets)
        self.doc_gen_controller = DocumentGeneratorController(self.main_view, self.checkout_model, self.assets)

    def __edit_view_launcher(self):
        self.edit_view_controller.open_view()

    def __check_in(self):
        for asset in self.assets:
            StockAPIController.check_in(asset)
        self.__refresh_assets()

    def __document_generator_view_launcher(self):
        self.doc_gen_controller.open_view()

    def __refresh_assets(self):
        serials = [asset.serial_number for asset in self.assets]
        self.assets.replace(self.edit_view_controller.update_assets(serials))

    def __on_select(self, event):
        self.assets_to_add.clear()

        selection = self.main_view.tree.selection()
        for item in selection:
            asset = self.assets.get_by_serial_number(self.main_view.tree.item(item)['values'][2])

            if asset.status == AssetStatus.READY_TO_ADD:
                self.assets_to_add.add(asset)

        if len(self.assets_to_add) > 0:
            self.main_view.btn_auto_add.config(state='normal')
        else:
            self.main_view.btn_auto_add.config(state='disable')

    def __open_browser(self, event):
        from Main import CONFIG
        selection = self.main_view.tree.selection()

        if len(selection) == 1:
            asset_id = self.main_view.tree.item(selection[0])['values'][0]
            if asset_id != -1:
                webbrowser.open('{}/{}/{}'.format(CONFIG.URL, 'hardware', asset_id))

    def __auto_add(self):
        for asset in self.assets_to_add:

            category_id = StockAPIController.get_category_id(asset.category_name)
            if category_id == -1:
                category_id = StockAPIController.create_category(asset.category_name)

            asset.category_id = category_id

            if category_id == -1:
                logging.error('Error. Cannot create category in auto-add process for asset: {}'.format(str(asset)))
                continue

            model_id = StockAPIController.get_model_id(asset.model_name)
            if model_id == -1:
                model_id = StockAPIController.create_model(asset.model_name, category_id)

            asset.model_id = model_id

            if model_id == -1:
                logging.error('Error. Cannot create model in auto-add process for asset: {}'.format(str(asset)))
                continue

            asset_id = StockAPIController.create_hardware(asset, 1)
            if asset_id == -1:
                logging.error('Error. Cannot create asset in auto-add process for asset: {}'.format(str(asset)))

            else:
                logging.info('Created asset with id: {}, asset: {}'.format(asset_id, str(asset)))

        self.main_view.btn_auto_add.config(state='disable')
        self.__refresh_assets()

    @staticmethod
    def __close_app():
        logging.info('Closing app')
        exit(0)
