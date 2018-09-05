import requests

from Model.AssetModel import AssetStatus, Asset


class APIController:
    """

    Class responsible for connecting to API
    Getting data and parsing as Asset objects.

    This app currently is planned only to fetching data for hardware.
    """

    @staticmethod
    def parse_hardware_data(serial: str):
        """

        :param serial: serial number - one of input from user GUI
        :return Asset: object
        """

        def set_asset(resp, _asset):
            _asset.set_id(int(resp['id']))
            _asset.set_name(resp['name'])
            _asset.set_notes(resp['notes'])
            _asset.set_status(AssetStatus.get_status(resp['status_label']['id'], resp['status_label']['status_meta']))

        print('-' * 15)
        asset = Asset(serial_number=serial)

        response = None
        try:
            response = APIController.get_data_from_api(serial)

            if response is None or 'total' in response and response['total'] == 0:
                asset.set_status(AssetStatus.ASSET_NOT_FOUND)
                print('Not found: {}'.format(asset.get_id()))

            elif 'status' in response and response['status'] == 'error':
                raise KeyError('API Problem')

            else:
                set_asset(response['rows'][0], asset)
                print(asset)

        except IOError:
            asset.set_status(AssetStatus.NOT_CONNECTED)
            print('Error! Connection problem.')

        except KeyError:
            asset.set_status(AssetStatus.STATUS_NOT_FOUND)
            if response is not None and 'message' in response and response['message'] == 'Unauthorized.':
                print('Error! Problem with API authorization.')
            else:
                print('Error! API problem.')

        return asset

    @staticmethod
    def get_data_from_api(asset_serial):
        """
        Trying to obtain data from Snipe-It API by serial number.

        :param asset_serial: It's User input form Text Area EditView (GUI).
        :rtype: dict
        :return: response as json

        """
        from Main import CONFIG

        endpoint = 'hardware/byserial/'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': CONFIG.TOKEN
        }

        return requests.get(CONFIG.URL + endpoint + asset_serial, headers=headers).json()
