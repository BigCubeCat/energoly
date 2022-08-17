from .Types import Station


class MainStation(Station):
	def __init__(self, index, parents, name, criticalDamage) -> None:
		super().__init__(index, parents, name, criticalDamage, 3)

class StationA(Station):
	def __init__(self, index, parents, name, criticalDamage) -> None:
		super().__init__(index, parents, name, criticalDamage, 3)

	
class StationB(Station):
	def __init__(self, index, parents, name, criticalDamage) -> None:
		super().__init__(index, parents, name, criticalDamage, 2)
