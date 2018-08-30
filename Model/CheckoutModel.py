class CheckoutModel:

    def __init__(self):
        self.__checkout_date = ''
        self.__check_in_date = ''
        self.__middle_man_name = ''
        self.__client_name = ''
        self.__client_address = ''

    def get_checkout_date(self):
        return self.__checkout_date

    def get_check_in_date(self):
        return self.__check_in_date

    def get_middle_man_name(self):
        return self.__middle_man_name

    def get_client_name(self):
        return self.__client_name

    def get_client_address(self):
        return self.__client_address

    def set_checkout_date(self, new_date):
        self.__checkout_date = new_date

    def set_check_in_date(self, new_date):
        self.__check_in_date = new_date

    def set_middle_man_name(self, name):
        self.__middle_man_name = name

    def set_client_name(self, name):
        self.__client_name = name

    def set_client_address(self, address):
        self.__client_address = address
