import logging

import requests

from Model.AssetModel import AssetStatus, Asset


class StockAPIController:
    """

    Class responsible for connecting to Snipe-IT API
    Getting data and parsing to objects.

    """

    HARDWARE_ENDPOINT = 'hardware/byserial'
    MODEL_ENDPOINT = 'models'

    @staticmethod
    def parse_hardware_data(serial: str):
        """

        :param serial: serial number - one of input from user GUI
        :return Asset: object
        """

        def set_asset(resp, _asset):
            _asset.id = int(resp['id'])
            _asset.tag = resp['asset_tag']
            _asset.name = resp['name']
            _asset.model_id = int(resp['model']['id'])
            _asset.model_name = resp['model']['name']
            _asset.notes = resp['notes']
            _asset.status = AssetStatus.get_status(resp['status_label']['id'], resp['status_label']['status_meta'])

        asset = Asset(serial_number=serial)
        response = None

        try:
            response = StockAPIController.get_data_from_api(StockAPIController.HARDWARE_ENDPOINT + '/' + serial)

            if response is None or 'total' in response and response['total'] == 0:
                asset.status = AssetStatus.ASSET_NOT_FOUND
                logging.info('Not found asset with sn: {}'.format(asset.serial_number))

            elif 'status' in response and response['status'] == 'error':
                raise KeyError('API Problem')

            else:
                set_asset(response['rows'][0], asset)
                logging.info(str(asset))

        except IOError:
            asset.status = AssetStatus.NOT_CONNECTED
            logging.error('Error! Connection problem. Cannot create asset.')

        except KeyError:
            asset.status = AssetStatus.STATUS_NOT_FOUND
            if response is not None and 'message' in response and response['message'] == 'Unauthorized.':
                logging.error('Error! Problem with API authorization. Cannot create asset.')
            else:
                logging.error('Error! API problem. Cannot create asset.')

        return asset

    @staticmethod
    def get_model_id(model_name):
        """
        :param model_name: Model/PID
        :rtype: int
        :return: int with id. If not found returns -1
        """

        try:
            response = StockAPIController.get_data_from_api(endpoint=StockAPIController.MODEL_ENDPOINT,
                                                            params={'search': model_name})

            if response is None or 'total' in response and response['total'] == 0:
                logging.info('Model with name {} not found'.format(model_name))

            elif 'total' in response and response['total'] >= 1:
                for row in response['rows']:
                    if row['name'] == model_name:
                        return row['id']

        except IOError:
            logging.error('Error! Connection problem with getting model_id.')

        except KeyError:
            logging.error('Error! Problem with getting model_id from model_name.')

        return -1

    @staticmethod
    def get_data_from_api(endpoint, params=None):
        """
        Trying to obtain data from Snipe-It API.

        :param endpoint: end of url with optional data i.e. 'hardware/byserial/123' where /123 must be included in str
        :param params: standard request dictionary
        :rtype: dict
        :return: response as json or None

        """
        from Main import CONFIG

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': CONFIG.TOKEN
        }
        if not params:
            params = {}

        return requests.get(CONFIG.URL + endpoint, headers=headers, params=params).json()
