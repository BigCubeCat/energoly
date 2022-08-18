#! python
from Objects.SolarGenerator import SolarGenerator
from Objects.WindGenerator import WindGenerator
from Objects.SteamGenerator import SteamGenerator
from Objects.Types.Consumer import Consumer
from Objects.Types.Generator import Generator
from Objects.Types.Edge import Edge
from Objects.Types.Station import Station

objects = [
	Station(0, None, "M1", 50),
	Edge(1, 0, 100),
	SteamGenerator(2, 1, "f3", 10)
]


for i in range(100): # Все тики
	for obj in objects:
		if isinstance(obj, Generator):
  			energy = obj.update(); # TODO: передать значение
			objects[obj.parent].update(energy)
		elif isinstance(obj, Consumer):
			energy = obj.update(); # TODO: передать значение
			objects[obj.parent].update(energy)
		elif isinstance(obj, Edge):
			obj.update()
			objects[obj.parent] # TODO: Износ на edge

            
