from Model.Observable import Observable


class Model:
    def __init__(self):
        self.input_data = Observable(0)

    def set_text(self, new_text):
        self.input_data.set(new_text)
