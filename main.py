#! python
from Objects.SolarGenerator import SolarGenerator
from Objects.WindGenerator import WindGenerator
from Objects.SteamGenerator import SteamGenerator
from Objects.Types.Consumer import Consumer
from Objects.Types.Generator import Generator
from Objects.Types.Edge import Edge
from Objects.Types.Station import Station
from topchek import read_topology


stations, edges, objects = read_topology("testTopology")

score = 0

for tick in range(1): # Все тики
    for obj in objects:
        try:
            if isinstance(obj, Consumer):
                score += obj.update(1, edges, stations) # TODO: Расчет энергии! Выдать потребление из прогноза на текущем тике
            else:
                obj.update(tick, edges, stations)
        except Exception as error:
            print(error)
    for station in stations:
        station.update()

