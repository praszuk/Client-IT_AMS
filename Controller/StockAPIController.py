import json
import logging

import requests

from Model.AssetModel import Asset
from Model.AssetStatusModel import AssetStatus


class StockAPIController:
    """

    Class responsible for connecting to Snipe-IT API
    Getting data and parsing to objects.

    """

    HARDWARE_BY_SERIAL_ENDPOINT = '/api/v1/hardware/byserial'
    HARDWARE_ENDPOINT = '/api/v1/hardware'

    MODEL_ENDPOINT = '/api/v1/models'
    CATEGORY_ENDPOINT = '/api/v1/categories'

    @staticmethod
    def build_asset(resp, _asset):
        """

        :param resp: response from stock api (get_hardware) It must be 200 OK FOUND
        :param _asset: new created object which will be build Serial number must be set before that.

        """
        _asset.id = int(resp['id'])
        _asset.tag = resp['asset_tag']
        _asset.name = resp['name']
        _asset.model_id = int(resp['model']['id'])
        _asset.model_name = resp['model']['name']
        _asset.notes = resp['notes']
        _asset.category_id = resp['category']['id']
        _asset.category_name = resp['category']['name']
        _asset.status = AssetStatus.get_status(resp['status_label']['id'], resp['status_label']['status_meta'])
        logging.debug('Created asset: ' + str(_asset))

    @staticmethod
    def get_hardware(serial: str):
        """

        :param serial: serial number - one of input from user GUI
        :return Asset: object
        """

        asset = Asset(serial_number=serial)
        response = None

        try:
            response = StockAPIController.get_data_from_api(
                StockAPIController.HARDWARE_BY_SERIAL_ENDPOINT + '/' + serial)

            logging.debug(response)
            if response is None or 'total' in response and response['total'] == 0:
                asset.status = AssetStatus.ASSET_NOT_FOUND
                logging.info('Not found asset with sn: {}'.format(asset.serial_number))

            elif 'status' in response and response['status'] == 'error':
                raise KeyError('API Problem')

            else:
                StockAPIController.build_asset(response['rows'][0], asset)
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
            logging.debug(response)
            if response and 'total' in response and response['total'] >= 1:
                for row in response['rows']:
                    if row['name'].lower() == model_name.lower():
                        logging.debug('Model id has been found: id: {}, name: {}'.format(row['id'], model_name))

                        return row['id']

        except IOError:
            logging.error('Error! Connection problem with getting model_id.')

        except KeyError:
            logging.error('Error! Problem with getting model_id from model_name.')

        logging.info('Model with name {} not found'.format(model_name))
        return -1

    @staticmethod
    def get_category_id(category_name):
        """
        :param category_name:
        :rtype: int
        :return: int with id. If not found returns -1
        """

        try:
            response = StockAPIController.get_data_from_api(endpoint=StockAPIController.CATEGORY_ENDPOINT,
                                                            params={'search': category_name})

            logging.debug(response)
            if response and 'total' in response and response['total'] >= 1:
                for row in response['rows']:
                    if row['name'].lower() == category_name.lower():
                        logging.debug('Category id has been found: id: {}, name: {}'.format(row['id'], category_name))

                        return row['id']

        except IOError:
            logging.error('Error! Connection problem with getting category_id.')

        except KeyError:
            logging.error('Error! Problem with getting category_id from category_name.')

        logging.info('Category with name {} not found'.format(category_name))

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

        return requests.get(CONFIG.URL + endpoint, headers=headers, params=params, timeout=5).json()

    @staticmethod
    def create_data_at_api(endpoint, payload):
        """
        Send post request to Snipe-IT api, to create specific object.
        :param endpoint: url + optional data
        :param payload: dict with data
        :rtype: dict
        :return: json

        """
        from Main import CONFIG

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': CONFIG.TOKEN
        }

        return requests.post(url=CONFIG.URL + endpoint, headers=headers, data=json.dumps(payload)).json()

    @staticmethod
    def create_category(category_name):
        """
        :param category_name: unique str
        :rtype: int
        :return: id new created category or -1 if cannot create
        """

        # There is few category type asset, accessory, consumable, component but for this app we use only asset
        payload = {
            'name': category_name,
            'category_type': 'asset'
        }

        try:
            response = StockAPIController.create_data_at_api(StockAPIController.CATEGORY_ENDPOINT, payload)
            logging.debug(response)
            if response and response['status'] == 'success':

                category_id = response['payload']['id']
                logging.info('Created category: {}, with id: {}'.format(category_name, category_id))

                return category_id

            else:
                logging.error('Error with creating category {}: {}'.format(category_name, response['messages']['name']))

        except IOError:
            logging.error('Error with post request to API. Cannot create category name: ' + category_name)

        except KeyError:
            logging.error('Error with API response. Cannot create category name: ' + category_name)

        return -1

    @staticmethod
    def create_model(model_name, category_id, manufacturer_id=1, unique=True):
        """
        Be careful using it. In snipe-it you can make new model with duplicated_name

        :param model_name: PID str
        :type model_name: str

        :param category_id: id of EXISTS category
        :type category_id: int

        :param manufacturer_id: optional default it's always 1 it means first manufacturer.
        :type manufacturer_id: int

        :param unique: if it's true then check if model_name exist before try to create new then return model_id
        :type unique: bool

        :rtype: int
        :return: model_id if create or exists  or if error -1
        """

        if unique:
            model_id = StockAPIController.get_model_id(model_name)
            if model_id != -1:
                logging.warning('Error with creating model. Model_name already exists!')
                return model_id

        payload = {
            'name': model_name,
            'category_id': category_id,
            'manufacturer_id': manufacturer_id
        }

        try:
            response = StockAPIController.create_data_at_api(StockAPIController.MODEL_ENDPOINT, payload)
            logging.debug(response)
            if response and response['status'] == 'success':

                model_id = response['payload']['id']
                logging.info('Created model: {}, with id: {}'.format(model_name, model_id))

                return model_id

            else:
                logging.error('Error with creating model {}: {}'.format(model_name, response['messages']['name']))

        except IOError:
            logging.error('Error with post request to API. Cannot create model name: ' + model_name)

        except KeyError:
            logging.error('Error with API response. Cannot create model name: ' + model_name)

        return -1

    @staticmethod
    def create_hardware(asset, status_id):
        """

        :param asset: Object which is ready to add
        :param status_id: Status id which is ID from AssetStatus (enum) >= 0 DEFAULT READY TO DEPLOY

        :type asset: Asset
        :type status_id: int

        :rtype: int
        :return: id of created asset or -1 if any error
        """

        payload = {

            'model_id': asset.model_id,
            'name': asset.name,
            'serial': asset.serial_number,
            'asset_tag': asset.tag,
            'status_id': status_id,

            'company_id': 1,
            'supplier_id': 1,
            'requestable': 1

        }

        try:
            response = StockAPIController.create_data_at_api(StockAPIController.HARDWARE_ENDPOINT, payload)
            logging.debug(response)
            if response and response['status'] == 'success':

                asset_id = response['payload']['id']
                logging.info('Created asset: {}, with id: {}'.format(asset.name, asset_id))
                asset.id = asset_id

                return asset_id

            else:
                logging.error('Error with creating asset {}: {}'.format(asset.name, response['messages']))

        except IOError:
            logging.error('Error with post request to API. Cannot create asset name: ' + asset.name)

        except KeyError:
            logging.error('Error with API response. Cannot create asset name: ' + asset.name)
