import logging

import requests


class AutoUpdate:
    FILE = 'version'
    GITHUB = 'https://raw.githubusercontent.com/praszuk/Client-IT_AMS/master/version'

    @staticmethod
    def is_up_to_date():
        """
        Checking from file and remote repository (github) whether the app is up to date.

        :raise IOError: if problem with connecting to github or reading local file
        :rtype: bool
        :return: True/False or None if there is something wrong i.e. with github path
        """

        try:
            with open(AutoUpdate.FILE, 'r') as file:
                local_version_raw = file.readline()
                local_version = int(local_version_raw.replace('.', ''))
                logging.info('Checking for update with local version: {}'.format(local_version_raw))

            response = requests.get(AutoUpdate.GITHUB)

            if response.status_code == 200:
                remote_version_raw = response.text
                remote_version = int(remote_version_raw.replace('.', ''))
                logging.info('Found remote version: {}'.format(remote_version_raw))

            else:
                logging.error('Cannot get remote version: {}, {}'.format(response.status_code, response.text))
                return None

            if remote_version == local_version:
                logging.info('App is up to date.')
                return True

            elif remote_version > local_version:
                logging.info('Update with version: {} is available.'.format(remote_version_raw))
                return False

            else:
                logging.warning('Please do not modify version file ("{}") by your own!'.format(AutoUpdate.FILE))
                return None

        except IOError as e:
            logging.error('Cannot check for updates. Error: {}'.format(e))
            return None
