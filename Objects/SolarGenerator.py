import Types


class SolarGenerator(Types.Generator):
    def __init__(self, index, parents, name, rent_price) -> None:
        super().__init__(index, parents, name)
        self.setBill(rent_price)
        self.inertia = 0 # Инерция Солнечки (ЛОЛ?) 

    def update(self):
        # TODO
        pass

