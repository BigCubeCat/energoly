from .BaseObject import BaseObject


class Consumer(BaseObject):
    def __init__(self, index, parents, name) -> None:
        super().__init__(index, parents, name)
        self.bill = 0  # Счет, сколько Рублей тратит чел на Мегават электричества
        self.totatBill = 0

    def setBill(self, bill):
        self.bill = bill

    def update(self, energy, edges, stations): 
        """
        energy: Колличество энергии в Мвт потребленное потребителем за такт
        """
        # TODO: Проверить что энергия поступает из parent
        # Если не поступает - то штраф
        self.totatBill += self.bill * energy
        return abs(edges[self.parents].update(-energy, stations)) * self.bill

