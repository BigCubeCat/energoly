from .BaseObject import BaseObject


class Station(BaseObject):
    def __init__(self, index, parents, name, criticalDamage) -> None:
        super().__init__(index, parents, name)
        self.criticalDamage = criticalDamage
        self.currentDamage = 0

