#! python
from Objects.SolarGenerator import SolarGenerator
from Objects.WindGenerator import WindGenerator
from Objects.SteamGenerator import SteamGenerator
from Objects.Types.Consumer import Consumer
from Objects.Types.Generator import Generator
from Objects.Types.Edge import Edge
from Objects.Types.Station import Station
from topchek import read_topology

station_ports, stations, edges, objects, visit = read_topology("testTopology")
stations_name = [v for v in visit if v[0] in 'Mme']
objects_name = [v for v in visit if v[0] not in 'Mme']

weather_wind_all = [0]*100
weather_sun_all = [0]*100

score = 0

for tick in range(1): # Все тики
    print(f'Начало тика         ================== {tick} ====================')
    for obj_name in visit[::-1]:
        if obj_name[0] in 'Mme':
            for edge_id in station_ports[obj_name]:
                edge = edges[edge_id]
                edge.update(stations, station_ports)
            station_index = stations_name.index(obj_name)
            stations[station_index].update(edges)
        else:
            objects_index = objects_name.index(obj_name)
            object = objects[objects_index]
            if isinstance(object, WindGenerator):
                object.update(*[
                    weather_wind_all[tick - 3] if tick >= 3 else 0,
                    weather_wind_all[tick - 2] if tick >= 2 else 0,
                    weather_wind_all[tick - 1] if tick >= 1 else 0,
                    weather_wind_all[tick]
                             ], edges, stations)
            elif isinstance(object, SolarGenerator):
                object.update(weather_sun_all[tick], edges, stations)
            elif isinstance(object, Consumer):
                object.update(1, edges, stations)
    print('Конец тика.')

