import logging

from Controller.ProductAPIController import ProductAPIController
from Controller.StockAPIController import StockAPIController
from Model.AssetListModel import AssetListModel
from Model.AssetModel import AssetStatus
from Model.EditViewModel import EditViewModel
from View.EditView import EditView


class EditViewController:
    def __init__(self, root, assets: AssetListModel):
        self.root = root
        self.assets = assets

        self.__product_api_controller = ProductAPIController()

        self.__model = EditViewModel()
        self.__model.input_data.add_callback(self.__input_data_changed)

        self.__edit_view = EditView(self.root)
        self.__edit_view.withdraw()

        self.__edit_view.set_text(self.__model.get_text())  # set default text
        self.__edit_view.cancel_btn.config(command=self.__cancel_edit)
        self.__edit_view.ok_btn.config(command=self.__ok_edit)

    def open_view(self):
        self.__edit_view.deiconify()

    def update_assets(self, serials):
        assets = []

        for serial in serials:
            asset = StockAPIController.get_hardware(serial)
            if asset and asset.status == AssetStatus.ASSET_NOT_FOUND or asset.status == AssetStatus.NOT_CONNECTED:
                logging.info('Asset not found, getting data from product info api...')
                asset = self.__product_api_controller.parse_product_data(serial)
            else:
                logging.info('Asset exist in local database, skipping query to product info api.')

            if asset:
                assets.append(asset)

        return assets

    def __cancel_edit(self):
        self.__edit_view.set_text('\n'.join(self.__model.input_data.get()))  # recently text
        self.__edit_view.withdraw()

    def __ok_edit(self):
        serials = self.__edit_view.get_text().strip().split()  # model as list
        self.__model.set_text(serials)
        self.__edit_view.set_text('\n'.join(self.__model.input_data.get()))  # Reformat (like whitespaces)
        self.__edit_view.withdraw()

    def __input_data_changed(self, serials):
        self.assets.replace(self.update_assets(serials))
