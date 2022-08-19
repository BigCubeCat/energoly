from .BaseObject import BaseObject


class Generator(BaseObject):
    def __init__(self, index, parents, name) -> None:
        super().__init__(index, parents, name)
        self.bill = 0  # Счет, сколько Рублей тратит чел на Мегават электричества
        self.totatBill = 0

    def setBill(self, bill):
        self.bill = bill

    def update(self, edges, stations): 
        # TODO: Проверить что энергия поступает из parent
        # Если не поступает - то штраф
        self.totatBill += self.bill
        return edges[self.parents[0]].update(energy, stations) # У генератора рента не зависит от результата
        # TODO: calulate energy
