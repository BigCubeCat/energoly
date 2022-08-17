from .Types import Generator


class WindGenerator(Generator):
    def __init__(self, index, parents, rent_price) -> None:
        super().__init__(index, parents)
        self.setBill(rent_price)
        self.inertia = 0 # Инерция ветряка 

    def update(self):
        # TODO
        pass

