from View.DocumentGeneratorView import DocumentGeneratorView


class DocumentGeneratorController:
    def __init__(self, master, checkout_model, assets):
        self.checkout_model = checkout_model
        self.hardware = assets

        from DocumentGenerator import Generator
        self.__generator = Generator()

        self.__document_generator_view = DocumentGeneratorView(master)
        self.__document_generator_view.save_to_file_btn.configure(command=self.generate_doc_to_file)
        self.__document_generator_view.config()
        self.__document_generator_view.withdraw()

    def generate_doc_to_file(self):
        self.update_model_from_form()
        file_name = self.__document_generator_view.open_file_chooser()
        if file_name:
            self.__generator.generate_loan_protocol(self.checkout_model, self.hardware)
            self.__generator.save_to_file(file_name)

    def update_model_from_form(self):
        self.checkout_model.checkout_date = self.__document_generator_view.checkout_date
        self.checkout_model.check_in_date = self.__document_generator_view.check_in_date
        self.checkout_model.middle_man_name = self.__document_generator_view.middle_full_name
        self.checkout_model.client_name = self.__document_generator_view.client_full_name
        self.checkout_model.client_address = self.__document_generator_view.client_address

    def open_view(self):
        self.__document_generator_view.deiconify()
