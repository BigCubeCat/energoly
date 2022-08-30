if __name__ == "__main__":
    from BaseObject import BaseObject
else:
    from .BaseObject import BaseObject
from math import e


class Station(BaseObject):
    def __init__(self, index, parents, name, criticalDamage) -> None:
        super().__init__(index, parents, name)
        self.criticalDamage = criticalDamage
        self.currentDamage = 0

        self.alive = True
        self.x = 0

    def add_energy(self, energy): 
        """
        Для расчета нагрузки
        """
        self.x += energy / 30

    def update(self):
        w = (self.x ** 1.9) / 6
        error_probability = 1 / (1 + e ** (36 - 40 * w))
        print(error_probability)


if __name__ == "__main__":
    for i in range(1, 30):
        st = Station(0, [], "a", 100)
        print(i)
        for j in range(5):
            st.add_energy(i)
        st.update()
        print()
