if __name__ == "__main__":
    from BaseObject import BaseObject
else:
    from .BaseObject import BaseObject
from math import e
from random import random


class Station(BaseObject):
    def __init__(self, index, parents, name, criticalDamage) -> None:
        super().__init__(index, parents, name)
        self.criticalDamage = criticalDamage
        self.currentDamage = 0

        self.alive = True
        self.to_alive = 0
        self.w = 0

    def add_energy(self, energy): 
        """
        Для расчета нагрузки
        """
        self.w += (abs(energy) / 30) ** 1.9 / 6

    def update(self):
        if not self.alive and self.to_alive == 0:
            self.alive = True
        elif not self.alive:
            self.to_alive -= 1
        else:
            error_probability = 1 / (1 + e ** (36 - 40 * self.w)) if self.w < 1 else 1
            if random() < error_probability:
                self.alive = False
                self.to_alive = 5


if __name__ == "__main__":
    st = Station(0, [], "a", 100)
    for i in range(1, 30):
        st.add_energy(15)
        st.update()
        print(i)
        print()
