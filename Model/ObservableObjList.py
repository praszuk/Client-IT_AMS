class ObservableObjList:
    def __init__(self, initial_list=None):
        self.__data = list() if not initial_list else initial_list
        self.__callbacks = {}

    def add_callback(self, func):
        self.__callbacks[func] = 1

    def del_callback(self, func):
        del self.__callbacks[func]

    def __do_callbacks(self):
        for func in self.__callbacks:
            func()

    def get(self):
        return self.__data

    def add(self, obj):
        self.__data.append(obj)
        self.__do_callbacks()

    def remove(self, obj):
        self.__data.remove(obj)
        self.__do_callbacks()

    def clear(self):
        self.__data.clear()

    def replace(self, obj_list):
        self.__data.clear()
        self.__data = list(obj_list)
        self.__do_callbacks()
