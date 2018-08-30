from View.DocumentGeneratorView import DocumentGeneratorView


class DocumentGeneratorController:
    def __init__(self, master, model):
        self.__model = model
        self.__document_generator_view = DocumentGeneratorView(master)

        self.__document_generator_view.withdraw()
        self.update_form()

    def open_view(self):
        self.__document_generator_view.deiconify()

    def update_form(self):
        self.__document_generator_view.set_check_in_date(self.__model.get_check_in_date())
        self.__document_generator_view.set_checkout_date(self.__model.get_checkout_date())
        self.__document_generator_view.set_client_address(self.__model.get_client_address())
        self.__document_generator_view.set_client_full_name(self.__model.get_client_name())
        self.__document_generator_view.set_middle_man_name(self.__model.get_middle_man_name())
