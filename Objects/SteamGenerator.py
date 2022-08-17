from .Types import Generator
from .utils import constrain

class SteamGenerator(Generator):
    def __init__(self, index, parents, name, rent_price) -> None:
        super().__init__(index, parents, name)
        self.setBill(rent_price)
        self.previousPower = 0

    def efficiency_TPS(self, count_fuel, a=-1/128, b=1/8, c=0.4):
        return a*count_fuel ** 2 + b * count_fuel + c
    
    def inertia_TPS(self, prew_power, factor=0.6, decrease=0.5): 
        return factor * (prew_power - decrease)

    def power_TPS(self, prew_power, count_fuel): 
        return count_fuel * constrain(self.efficiency_TPS(count_fuel), 0.4, 0.9) + self.inertia_TPS(prew_power)

    def update(self, power):

        result = self.power_TPS(self.previousPower, power)
        self.previousPower = result
        return result

