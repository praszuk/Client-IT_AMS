import time

import requests

from Model.AssetModel import Asset, AssetStatus


class ProductAPIController:

    def __init__(self):
        self.__token = None
        self.__expire_time = time.time()

    def __update_token(self):
        from Main import CONFIG

        if time.time() >= self.__expire_time:
            endpoint = 'https://cloudsso.cisco.com/as/token.oauth2'
            parameters = {
                'grant_type': CONFIG.GRANT_TYPE,
                'client_id': CONFIG.CLIENT_ID,
                'client_secret': CONFIG.CLIENT_SECRET
            }

            try:
                response = requests.post(url=endpoint, params=parameters).json()
                self.__token = response['access_token']
                self.__expire_time = time.time() + response['expires_in']

            except IOError:
                self.__token = None
                self.__expire_time = time.time()
                print('Cannot obtain TOKEN from: {}'.format(endpoint))

    def get_product_data(self, serial_number):
        self.__update_token()

        endpoint = 'https://api.cisco.com/product/v1/information/serial_numbers/'
        headers = {'Authorization': 'Bearer ' + self.__token}

        r = requests.get(endpoint + serial_number, headers=headers)

        try:
            # print('Token: {}'.format(self.__token))
            return r.json()

        except ValueError:
            print('ERROR with api: {}'.format(r.text))
            return None

    def parse_product_data(self, sn):

        response = self.get_product_data(sn)
        if response:
            # print(response)
            if 'pagination_response_record' in response and 'product_list' in response:

                if response['pagination_response_record']['total_records'] > 1:
                    print('Ambiguous serial number! Multiple assets found in database [{}]'.format(sn))
                else:
                    if 'ErrorResponse' in response['product_list'][0]:
                        print('{} [{}]'.format(
                            response['product_list'][0]['ErrorResponse']['APIError']['ErrorCode'], sn))

                    else:
                        model = response['product_list'][0]['base_pid']  # pid = asset model
                        name = response['product_list'][0]['product_name']
                        category = response['product_list'][0]['product_category']

                        # TODO name as model is temporary in internal system. It will be using until global change.
                        a = Asset(name=model, serial_number=sn, asset_tag=sn)
                        a.set_status(AssetStatus.READY_TO_ADD)
                        return a

            return response

        return None
