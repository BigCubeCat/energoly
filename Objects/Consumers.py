import Types

class Factory(Types.Consumer):
    def __init__(self, index, parents, name) -> None:
        super().__init__(index, parents, name)


class HouseA(Types.Consumer):
    def __init__(self, index, parent, name) -> None:
        super().__init__(index, [parent], name)


class HouseB(Types.Consumer):
    def __init__(self, index, parent, name) -> None:
        super().__init__(index, [parent], name)


class Hospital(Types.Consumer):
    def __init__(self, index, parents, name) -> None:
        super().__init__(index, parents, name)

