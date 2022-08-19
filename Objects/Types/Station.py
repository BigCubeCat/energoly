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
        self.w = 0

    def add_energy(self, energy): 
        """
        Для расчета нагрузки
        """
        self.w += (energy / 30) ** 1.9 / 6
        self.w = min(1, self.w)
        print(self.w)

    def update(self):
        error_probability = 1 / (1 + e ** (36 - 40 * self.w))
        print(error_probability)


if __name__ == "__main__":
    st = Station(0, [], "a", 100)
    for i in range(1, 30):
        st.add_energy(15)
        st.update()
        print(i)
        print()
