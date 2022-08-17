from .Types import Generator
from .utils import constrain
from math import pi

class SolarGenerator(Generator):
    def __init__(self, index, parents, rent_price) -> None:
        super().__init__(index, parents)
        self.setBill(rent_price)

    def update(self):
        # TODO
        func_sin = lambda x, day_tick=48: 0.3 * sin(x * 4*pi/day_tick) - 3.5
        """
        spread = lambda s, variable_value=0.3: constrain(s + uniform(-variable_value/2, variable_value/2), 0, 15)

        inverse_coordinates = lambda x, y: (19-x, 10-y)
        first_sun = lambda x, y: - 0.102206143125*y**2+1.088911573499*y - 0.05493164125*x**2+0.6005859425*x + 5.518798830625019
        second_sun = lambda x, y: - 0.102206143125*y**2+1.088911573499*y - 0.05493164125*x**2+0.6005859425*x + 5.939941414375021
        dependence_on_the_position = lambda x, y: max(first_sun(x, y), second_sun(*inverse_coordinates(x, y)))

        gen_sun = lambda weather_sun, tick, x, y: spread(weather_sun + func_sin(tick) + (dependence_on_the_position(x, y)-dependence_on_the_position(2, 3)))

        s = [gen_sun(select[tick], tick, *(2, 3)) for tick in range(0, 100)]
        print(s)
        """
        pass

