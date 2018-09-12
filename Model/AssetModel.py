from enum import Enum

from Model.Observable import Observable


class Asset:

    def __init__(self, id=-1, tag='', name='', notes='', serial_number=''):

        self.id = id
        self.tag = tag
        self.name = name
        self.notes = notes
        self.serial_number = serial_number
        self.__status = Observable(None)

    def __str__(self):
        return 'ID: {}\nName: {}\nSerial Number: {}\nNotes: {}\nStatus: {}' \
            .format(self.id, self.name, self.serial_number, self.notes, self.status.name)

    @property
    def status(self):
        return self.__status.get()

    @status.setter
    def status(self, status):
        if not isinstance(status, AssetStatus):
            raise ValueError("Status {} not in AssetStatus enum list.".format(status))
        else:
            self.__status.set(status)


class AssetStatus(Enum):
    READY_TO_ADD = -4  # Not in internal system but found in external system by ProductAPI
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
