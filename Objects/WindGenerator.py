from .Types import Generator


class WindGenerator(Generator):
    def __init__(self, index, parents, name, rent_price, weather_wind_all, coordinate, power_wind, model) -> None:
        super().__init__(index, parents, name)
        self.setBill(rent_price)

        self.model = model
        self.weather_sun_all = weather_wind_all
        self.coordinate = coordinate
        self.power_wind = power_wind

    def update(self, tick, edges, stations):
        data = [
            self.weather_sun_all[tick - 3] ** 5 if tick >= 3 else 0,
            self.weather_sun_all[tick - 2] ** 5 if tick >= 2 else 0,
            self.weather_sun_all[tick - 1] ** 5 if tick >= 1 else 0,
            self.weather_sun_all[tick] ** 5,
            self.coordinate[0],
            self.coordinate[1],
            self.power_wind
        ]
        data_normal = [[0]*7, data]
        result = self.model[0].predict(data_normal)[1]
        super().update(result, edges, stations)
        return result
