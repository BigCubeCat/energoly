from .BaseObject import BaseObject


class Edge(BaseObject):
    def __init__(self, index, parent) -> None:
        super().__init__(index, [parent], "edge")
        self.criticalDamage = 100 # in percents
        self.currentDamage = 0

    def update(energy):
        pass # TODO: Сделать симуляцию нагрузки


