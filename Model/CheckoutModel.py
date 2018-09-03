from Model.Observable import Observable


class CheckoutModel:

    def __init__(self):
        self.__checkout_date = Observable('')
        self.__check_in_date = Observable('')
        self.__middle_man_name = Observable('')
        self.__client_name = Observable('')
        self.__client_address = Observable('')

    @property
    def checkout_date(self):
        return self.__checkout_date.get()

    @checkout_date.setter
    def checkout_date(self, value):
        self.__checkout_date.set(value)

    @property
    def check_in_date(self):
        return self.__check_in_date.get()

    @check_in_date.setter
    def check_in_date(self, value):
        self.__check_in_date.set(value)

    @property
    def middle_man_name(self):
        return self.__middle_man_name.get()

    @middle_man_name.setter
    def middle_man_name(self, value):
        self.__middle_man_name.set(value)

    @property
    def client_name(self):
        return self.__client_name.get()

    @client_name.setter
    def client_name(self, value):
        self.__client_name.set(value)

    @property
    def client_address(self):
        return self.__client_address.get()

    @client_address.setter
    def client_address(self, value):
        self.__client_address.set(value)
