from .Types import Consumer

class Factory(Consumer):
    def __init__(self, index, parents) -> None:
        super().__init__(index, parents)


class HouseA(Consumer):
    def __init__(self, index, parent) -> None:
        super().__init__(index, [parent])


class HouseB(Consumer):
    def __init__(self, index, parent) -> None:
        super().__init__(index, [parent])


class Hospital(Consumer):
    def __init__(self, index, parents) -> None:
        super().__init__(index, parents)

