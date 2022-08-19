if __name__ == "__main__":
    from BaseObject import BaseObject
else:
    from .BaseObject import BaseObject


class Edge(BaseObject):
    def __init__(self, index, parent) -> None:
        super().__init__(index, parent, "edge")
        self.criticalDamage = 100  # in percents
        self.currentDamage = 0

    def update(self, energy, stations):
        abs_energy = abs(energy)
        # Считаем потери
        looses = min(30, abs_energy)
        looses_percent = (looses / 30)
        total_looses = abs_energy * looses_percent * 0.25
        energy -= total_looses
        # Добавляем энергии на станцию
        stations[self.parent].add_energy(energy)
        return energy


