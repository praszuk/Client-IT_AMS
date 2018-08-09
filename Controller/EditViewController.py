import requests

from Model.AssetModel import Asset, AssetStatus
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
        assets = self.parse_data(text)
        # self.root.update_tree_view(assets)

    @staticmethod
    def parse_data(text):
        from Main import CONFIG

        assets = []
        ids = text.split()
        for _id in ids:
            print('-' * 15)
            asset = Asset()

            try:
                endpoint = 'hardware/'
                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': CONFIG.TOKEN
                }

                response = requests.get(CONFIG.URL + endpoint + _id, headers=headers).json()

                if 'status' in response:
                    if response['status'] == 'error':
                        asset.set_id(_id)
                        asset.set_status(AssetStatus.ASSET_NOT_FOUND)
                        print('Not found: {}'.format(asset.get_id()))

                else:
                    asset.set_id(int(response['id']))
                    asset.set_name(response['name'])
                    asset.set_serial_number(response['serial'])
                    asset.set_status(AssetStatus.get_status(response['status_label']['id'],
                                                            response['status_label']['status_meta']))
                    print(asset)

                assets.append(asset)

            except IOError:
                asset.set_status(AssetStatus.NOT_CONNECTED)
                print('Error! Connection problem.')

            except KeyError:
                asset.set_status(AssetStatus.STATUS_NOT_FOUND)
                print('Error! API problem.')

        return assets
