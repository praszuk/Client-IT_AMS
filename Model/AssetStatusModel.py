from enum import Enum


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
