from View.DocumentGeneratorView import DocumentGeneratorView


class DocumentGeneratorController:
    def __init__(self, master, model):
        self.__model = model
        self.__document_generator_view = DocumentGeneratorView(master, model)
        self.__document_generator_view.config()
        self.__document_generator_view.withdraw()

    def open_view(self):
        self.__document_generator_view.deiconify()
