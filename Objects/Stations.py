from .Types import Station


class MainStation(Station):
    def __init__(self, index, name) -> None:
        super().__init__(index, 0, name, 200, 3)

class StationA(Station):
    def __init__(self, index, parent, name) -> None:
        super().__init__(index, parent, name, 200, 3)

class StationB(Station):
    def __init__(self, index, parent, name) -> None:
        super().__init__(index, parent, name, 200, 2)

