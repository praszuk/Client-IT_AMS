from enum import Enum

from Model.Observable import Observable


class Asset:

    def __init__(self, _id=-1, name='', notes='', serial_number=''):

        self.__id = _id
        self.__name = name
        self.__notes = notes
        self.__serial_number = serial_number
        self.__status = Observable(None)

    def __str__(self):
        return 'ID: {}\nName: {}\nSerial Number: {}\nNotes: {}\nStatus: {}' \
            .format(self.__id, self.__name, self.__serial_number, self.__notes, self.__status.get().name)

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_notes(self):
        return self.__notes

    def get_serial_number(self):
        return self.__serial_number

    def get_status(self):
        return self.__status.get()

    def set_id(self, _id):
        self.__id = _id

    def set_name(self, name):
        self.__name = name

    def set_notes(self, notes):
        self.__notes = notes

    def set_serial_number(self, serial):
        self.__serial_number = serial

    def set_status(self, status):
        if not isinstance(status, AssetStatus):
            raise ValueError("Status {} not in AssetStatus enum list.".format(status))
        else:
            self.__status.set(status)


class AssetStatus(Enum):
    NOT_CONNECTED = -3
    STATUS_NOT_FOUND = -2
    ASSET_NOT_FOUND = -1

    DEPLOYED = 0
    READY_TO_DEPLOY = 1
    PENDING = 2
    SCRAP = 3
    OUT_OF_DIAGNOSTIC = 4
    OUT_OF_REPAIR = 5
    BROKEN = 6
    LOST_STOLEN = 7
    PRODUCTION = 8

    @staticmethod
    def get_status(_id, meta):
        if _id > 1 or _id < 0:
            return AssetStatus(_id)

        elif _id == 1:
            if meta == 'deployable':
                return AssetStatus(1)
            elif meta == 'deployed':
                return AssetStatus(0)

        else:
            return AssetStatus(-2)
