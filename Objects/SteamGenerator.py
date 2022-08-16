from .Types import Generator


class SteamGenerator(Generator):
    def __init__(self, index, parents, name, rent_price) -> None:
        super().__init__(index, parents, name)
        self.setBill(rent_price)

    def update(self, count_oil):
        # TODO
        bill = self.rent_price * count_oil 
        return count_oil * 10 ## TODO: 

