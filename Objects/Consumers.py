from .Types import Consumer

class Factory(Consumer):
    def __init__(self, index, parents, name) -> None:
        super().__init__(index, parents, name)


class HouseA(Consumer):
    def __init__(self, index, parent, name) -> None:
        super().__init__(index, [parent], name)


class HouseB(Consumer):
    def __init__(self, index, parent, name) -> None:
        super().__init__(index, [parent], name)


class Hospital(Consumer):
    def __init__(self, index, parents, name) -> None:
        super().__init__(index, parents, name)

