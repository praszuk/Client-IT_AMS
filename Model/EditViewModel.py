from Model.Observable import Observable


class EditViewModel:

    def __init__(self):
        self.input_data = Observable('')

    def get_text(self):
        return self.input_data.get()

    def set_text(self, new_text):
        self.input_data.set(new_text)
