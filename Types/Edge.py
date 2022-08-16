from .BaseObject import BaseObject


class Edge(BaseObject):
    def __init__(self, index, parent, criticalDamage) -> None:
        super().__init__(index, [parent], "edge")
        self.criticalDamage = criticalDamage
        self.currentDamage = 0

    def update(energy):
        pass # TODO: Сделать симуляцию нагрузки


