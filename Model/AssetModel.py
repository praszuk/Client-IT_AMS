from enum import Enum

from Model.Observable import Observable


class Asset:

    def __init__(self, asset_id, asset_tag, serial_number):

        self.__asset_id = asset_id
        self.__asset_tag = asset_tag
        self.__serial_number = serial_number
        self.__status = Observable(None)

    def set_status(self, status):
        if not isinstance(status, AssetStatus):
            raise ValueError("Status {} not in AssetStatus enum list.".format(status))
        else:
            self.__status.set(status)

    def get_status(self):
        return self.__status.get()


class AssetStatus(Enum):
    NOT_CONNECTED = -1
    DEPLOYED = 0
    READY_TO_DEPLOY = 1
    PENDING = 2
    SCRAP = 3
    OUT_OF_DIAGNOSTIC = 4
    OUT_OF_REPAIR = 5
    BROKEN = 6
    LOST_STOLEN = 7
    PRODUCTION = 8
