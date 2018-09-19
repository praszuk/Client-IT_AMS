from Model.AssetStatusModel import AssetStatus
from Model.Observable import Observable


class Asset:

    def __init__(self, id=-1, tag='', model_id=-1, model_name='', category_id=-1, category_name='',
                 name='', notes='', serial_number=''):

        self.id = id
        self.tag = tag
        self.name = name
        self.notes = notes
        self.serial_number = serial_number
        self.model_id = model_id
        self.model_name = model_name
        self.category_id = category_id
        self.category_name = category_name
        self.__status = Observable(None)

    def __str__(self):
        d = dict(self.__dict__)
        d['_Asset__status'] = str(self.status)

        return str(d)

    @property
    def status(self):
        return self.__status.get()

    @status.setter
    def status(self, status):
        if not isinstance(status, AssetStatus):
            raise ValueError("Status {} not in AssetStatus enum list.".format(status))
        else:
            self.__status.set(status)
