#! python
from Objects.SolarGenerator import SolarGenerator
from Objects.WindGenerator import WindGenerator
from Objects.SteamGenerator import SteamGenerator
from Objects.Types.Consumer import Consumer
from Objects.Types.Generator import Generator
from Objects.Types.Edge import Edge
from Objects.Types.Station import Station
from topchek import read_topology


objects = read_topology("testTopology")



for i in range(100): # Все тики
	for obj in objects:
		if isinstance(obj, Generator):
  			energy = obj.update(); # TODO: передать значение
			objects[obj.parent].update(energy)
		elif isinstance(obj, Consumer):
			energy = obj.update(0); # TODO: передать значение
			objects[obj.parent].update(energy)
		elif isinstance(obj, Edge):
			obj.update()
			objects[obj.parent] # TODO: Износ на edge

            
