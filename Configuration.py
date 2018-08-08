import configparser
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

        else:
            with open(AppConfig.__CONFIG_FILE, 'w') as configfile:
                configfile.write('[GENERAL]\n')
                configfile.write('template_file_path=<path to .docx document>\n')
                configfile.write('[API]\n')
                configfile.write('url=<your url to hardware API>\n')
                configfile.write('token=<api token with "Bearer" >')
                configfile.close()

            print('Please fill configuration file at: ' + AppConfig.__CONFIG_FILE)
