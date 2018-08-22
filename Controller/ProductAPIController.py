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
