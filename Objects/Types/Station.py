if __name__ == "__main__":
    from BaseObject import BaseObject
else:
    from .BaseObject import BaseObject
from math import e
from random import random


class Station(BaseObject):
    def __init__(self, index, parents, name, criticalDamage, count_line) -> None:
        super().__init__(index, parents, name)
        self.criticalDamage = criticalDamage
        self.currentDamage = 0
        self.count_line = count_line

        self.alive = [True for _ in range(self.count_line)]
        self.to_alive = [0 for _ in range(self.count_line)]
        self.w = [0 for _ in range(self.count_line)]

        self.total_energy = 0

    def add_energy(self, index, energy, station_ports):
        """
        Для расчета нагрузки
        """
        line = station_ports[self.name].index(index)
        self.w[line] += (abs(energy) / 30) ** 1.9 / 6
        self.total_energy += energy

    def update(self, edges):
        for line in range(self.count_line):
            if not self.alive[line] and self.to_alive[line] == 0:
                self.alive[line] = True
            elif not self.alive[line]:
                self.to_alive[line] -= 1
            else:
                error_probability = 1 / (1 + e ** (36 - 40 * self.w[line])) if self.w[line] < 1 else 1
                if random() < error_probability:
                    self.alive[line] = False
                    self.to_alive[line] = 5
                    self.w[line] = 0

        edges[self.parent].add_energy(self.total_energy)
        self.total_energy = 0


if __name__ == "__main__":
    st = Station(0, [], "a", 100)
    for i in range(1, 30):
        st.add_energy(15)
        st.update()
        print(i)
        print()
