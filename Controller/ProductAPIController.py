import logging
import time

import requests

from Model.AssetModel import Asset, AssetStatus


class ProductAPIController:
    __OAUTH_URL = 'https://cloudsso.cisco.com/as/token.oauth2'
    __PRODUCT_URL = 'https://api.cisco.com/product/v1/information/serial_numbers/'

    def __init__(self):
        self.__token = None
        self.__expire_time = time.time()

    def __update_token(self):
        from Main import CONFIG

        if time.time() >= self.__expire_time:
            parameters = {
                'grant_type': CONFIG.GRANT_TYPE,
                'client_id': CONFIG.CLIENT_ID,
                'client_secret': CONFIG.CLIENT_SECRET
            }

            try:
                response = requests.post(url=ProductAPIController.__OAUTH_URL, params=parameters).json()
                self.__token = response['access_token']
                self.__expire_time = time.time() + response['expires_in']
                logging.debug('Obtained token. Expiration time: {} seconds'.format(response['expires_in']))
            except IOError:
                self.__token = None
                self.__expire_time = time.time()
                logging.error('Cannot obtain TOKEN from: {}'.format(ProductAPIController.__OAUTH_URL))

    def get_data_from_api(self, serial_number):
        self.__update_token()

        headers = {'Authorization': 'Bearer ' + self.__token}
        r = requests.get(ProductAPIController.__PRODUCT_URL + serial_number, headers=headers)
        try:
            return r.json()

        except ValueError:
            logging.error('ERROR with api: {} Cannot get data from ProductAPI.'.format(r.text))
            return None

    def parse_product_data(self, sn):

        response = self.get_data_from_api(sn)
        if response:
            # print(response)
            if 'pagination_response_record' in response and 'product_list' in response:

                if response['pagination_response_record']['total_records'] > 1:
                    logging.warning('Ambiguous serial number! Multiple assets found in database [{}]'.format(sn))
                else:
                    if 'ErrorResponse' in response['product_list'][0]:
                        logging.error('{} [{}]'.format(
                            response['product_list'][0]['ErrorResponse']['APIError']['ErrorCode'], sn))

                    else:
                        model = response['product_list'][0]['base_pid']  # pid = asset model
                        name = response['product_list'][0]['product_name']
                        category = response['product_list'][0]['product_category']

                        # TODO name as model is temporary in internal system. It will be using until global change.
                        a = Asset(name=model, serial_number=sn, tag=sn, model_name=model, category_name=category)
                        a.status = AssetStatus.READY_TO_ADD

                        return a

        return None
