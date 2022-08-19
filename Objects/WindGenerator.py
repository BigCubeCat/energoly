from .Types import Generator
from utils import constrain


class WindGenerator(Generator):
    def __init__(self, index, parents, name, rent_price, coordinate, power_wind, model) -> None:
        super().__init__(index, parents, name)
        self.setBill(rent_price)

        self.model = model
        self.coordinate = coordinate
        self.power_wind = power_wind
        self.breaking = False

    def update(self, weather_wind_prev3, weather_wind_prev2, weather_wind_prev1, weather_wind, edges, stations):
        data = [
            weather_wind_prev3,
            weather_wind_prev2,
            weather_wind_prev1,
            weather_wind,
            self.coordinate[0],
            self.coordinate[1],
            self.power_wind
        ]
        data_normal = [[0]*7, data]
        result = self.model[0].predict(data_normal)[1]

        if result < 15/0.86:
            if not self.breaking or result < 15*0.875/0.86:
                result = constrain(result, 0, 15)
                self.breaking = False
            else:
                result = 0
        else:
            self.breaking = True
            result = 0

        super().update(result, edges, stations)
        return result
