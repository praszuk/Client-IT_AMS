import configparser
import logging

from pathlib import Path


class AppConfig:
    __CONFIG_FILE = '.config.txt'

    def __init__(self):

        cfg = configparser.ConfigParser()

        if Path(AppConfig.__CONFIG_FILE).is_file():
            cfg.read(AppConfig.__CONFIG_FILE)

            self.TEMPLATE_FILE_PATH = cfg.get('GENERAL', 'template_file_path').strip()

            self.URL = cfg.get('API', 'url').strip()
            self.TOKEN = cfg.get('API', 'token').strip()

            self.GRANT_TYPE = cfg.get('PRODUCT_INFO_API', 'grant_type')
            self.CLIENT_ID = cfg.get('PRODUCT_INFO_API', 'client_id')
            self.CLIENT_SECRET = cfg.get('PRODUCT_INFO_API', 'client_secret')

        else:
            with open(AppConfig.__CONFIG_FILE, 'w') as configfile:
                configfile.write('[GENERAL]\n')
                configfile.write('template_file_path=<path to .docx document>\n')
                configfile.write('[API]\n')
                configfile.write('url=<your url to hardware API>\n')
                configfile.write('token=<api token with "Bearer" >')
                configfile.write('[PRODUCT_INFO_API]')
                configfile.write('grant_type=client_credentials')
                configfile.write('client_id=<client_id>')
                configfile.write('client_secret=<client_secret>')
                configfile.close()

            logging.warning('Please fill configuration file at: ' + AppConfig.__CONFIG_FILE)
