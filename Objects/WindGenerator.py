import Types


class WindGeneration(Types.Generator):
    def __init__(self, index, parents, name, rent_price) -> None:
        super().__init__(index, parents, name)
        self.setBill(rent_price)
        self.inertia = 0 # Инерция ветряка 

    def update(self):
        # TODO
        pass

