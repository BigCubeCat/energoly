if __name__ == "__main__":
    from BaseObject import BaseObject
else:
    from .BaseObject import BaseObject


class Edge(BaseObject):
    def __init__(self, index, parent) -> None:
        super().__init__(index, parent, "edge")
        self.criticalDamage = 100  # in percents
        self.currentDamage = 0

        self.total_energy = 0

    def add_energy(self, energy):
        self.total_energy += energy
        return energy

    def update(self, stations, station_ports):
        abs_energy = abs(self.total_energy)

        # Считаем потери
        looses = min(30, abs_energy)
        looses_percent = (looses / 30)
        total_looses = abs_energy * looses_percent * 0.25
        self.total_energy -= total_looses

        # Добавляем энергии на станцию
        stations[self.parent].add_energy(self.index, self.total_energy, station_ports)
        self.total_energy = 0
        # return self.total_energy
