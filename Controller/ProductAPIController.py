import time

import requests


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
            print('Token: {}'.format(self.__token))
            print(r.json())

        except ValueError:
            print('ERROR with api: {}'.format(r.text))
            return None
