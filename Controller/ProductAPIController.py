import requests


class ProductAPIController:

    def __init__(self):
        self.__token = None

    def __update_token(self):
        from Main import CONFIG

        endpoint = 'https://cloudsso.cisco.com/as/token.oauth2'
        parameters = {
            'grant_type': CONFIG.GRANT_TYPE,
            'client_id': CONFIG.CLIENT_ID,
            'client_secret': CONFIG.CLIENT_SECRET
        }
        print(parameters)
        r = requests.post(url=endpoint, params=parameters)
        print(r.text)
        print(r.raw)

        self.__token = r.json()['access_token']

    def get_product_data(self, serial_number):
        self.__update_token()

        endpoint = 'https://api.cisco.com/product/v1/information/serial_numbers/' + serial_number
        headers = {'Authorization': 'Bearer ' + self.__token}
        r = requests.get(endpoint, headers=headers)
        try:
            print(r.json())
        except:
            pass
