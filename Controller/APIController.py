from typing import List

import requests

from Model.AssetModel import AssetStatus, Asset


class APIController:
    """

    Class responsible for connecting to API
    Getting data and parsing as Asset objects.

    This app currently is planned only to fetching data for hardware.
    """

    @staticmethod
    def parse_hardware_data(text: str):
        """

        :param text: ids/serial numbers - input from user GUI
        :return List[Asset]: asset objects
        """

        def set_asset(resp, _asset):
            _asset.set_id(int(resp['id']))
            _asset.set_name(resp['name'])
            _asset.set_serial_number(resp['serial'])
            _asset.set_status(AssetStatus.get_status(resp['status_label']['id'], resp['status_label']['status_meta']))

        assets = []
        ids = text.split()

        for _id in ids:
            print('-' * 15)
            asset = Asset()

            try:
                response, index = APIController.get_data_from_api(_id)

                if response is None or 'total' in response and response['total'] == 0:
                    asset.set_id(_id)
                    asset.set_status(AssetStatus.ASSET_NOT_FOUND)
                    print('Not found: {}'.format(asset.get_id()))

                else:
                    # By Serial Number
                    if index == 0:
                        set_asset(response['rows'][0], asset)

                    # By ID (database)
                    elif index == 1:
                        set_asset(response, asset)

                    print(asset)

                assets.append(asset)

            except IOError:
                asset.set_status(AssetStatus.NOT_CONNECTED)
                print('Error! Connection problem.')

            except KeyError:
                asset.set_status(AssetStatus.STATUS_NOT_FOUND)
                print('Error! API problem.')

        return assets

    @staticmethod
    def get_data_from_api(asset_id):
        """
        Trying to obtain data from Snipe-It API.
        Firstly by serial number, secondly by database unique id.

        :param asset_id: id or serial. It's User input form Text Area EditView (GUI).
        :rtype: (dict, int)
        :return: response as json or None and index as endpoint which was used 0. hardware or 1. hardware/byserial.

        """
        from Main import CONFIG

        endpoints: List[str] = ['hardware/byserial/', 'hardware/']
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': CONFIG.TOKEN
        }

        for index, endpoint in enumerate(endpoints):
            r = requests.get(CONFIG.URL + endpoint + asset_id, headers=headers).json()
            print(r)
            if 'status' in r and r['status'] == 'error':
                if index == 0:
                    print('Asset with Serial: {} error: {}'.format(asset_id, r['messages']))
                elif index == 1:
                    print('Asset with ID: {} error: {}'.format(asset_id, r['messages']))
                continue

            return r, index

        return None, -1
