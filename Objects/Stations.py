from .Types import Station


class MainStation(Station):
    def __init__(self, index, name) -> None:
        super().__init__(index, [], name, 200)

class StationA(Station):
    def __init__(self, index, parents, name) -> None:
        super().__init__(index, parents, name, 200)

class StationB(Station):
    def __init__(self, index, parents, name) -> None:
        super().__init__(index, parents, name, 200)

