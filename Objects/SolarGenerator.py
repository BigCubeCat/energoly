from .Types import Generator
from utils import constrain
from random import uniform


class SolarGenerator(Generator):
    def __init__(self, index, parents, name, rent_price, weather_sun_all, coordinate) -> None:
        super().__init__(index, parents, name)
        self.setBill(rent_price)

        self.weather_sun_all = weather_sun_all
        self.max_weather_sun = max(self.weather_sun_all)
        self.coordinate = coordinate

    def func_sin(self, weather_sun):
        return - 3.8 + 0.6 * (weather_sun/self.max_weather_sun)**2

    def spread(self, s, variable_value=0.3):
        return constrain(s + uniform(-variable_value/2, variable_value/2), 0, 15)

    def inverse_coordinates(self, x, y):
        return 19-x, 10-y

    def first_sun(self, x, y):
        return - 0.102206143125*y**2+1.088911573499*y - 0.05493164125*x**2+0.6005859425*x + 5.518798830625019

    def second_sun(self, x, y):
        x, y = self.inverse_coordinates(x, y)
        return - 0.102206143125*y**2+1.088911573499*y - 0.05493164125*x**2+0.6005859425*x + 5.939941414375021

    def dependence_on_the_position(self, x, y):
        return max(self.first_sun(x, y), self.second_sun(x, y))

    def gen_sun(self, weather_sun, x, y):
        return self.spread(weather_sun + self.func_sin(weather_sun) + (self.dependence_on_the_position(x, y)-self.dependence_on_the_position(2, 3)))

    def update(self, tick, edges, stations):
        result = self.gen_sun(self.weather_sun_all[tick], *self.coordinate)
        super().update(result, edges, stations)
        return result
