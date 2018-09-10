from Model.ObservableObjList import ObservableObjList


class AssetListModel:
    def __init__(self):
        self.data = ObservableObjList()

    def __iter__(self):
        return iter(self.data.get())

    def __len__(self):
        return len(self.data.get())

    def add(self, asset):
        self.data.add(asset)

    def remove(self, asset):
        self.data.remove(asset)

    def clear(self):
        self.data.clear()

    def replace(self, assets_list):
        self.data.replace(assets_list)
