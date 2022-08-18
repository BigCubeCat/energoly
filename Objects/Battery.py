from .Types import Consumer
from .Types import Generator

class Battery(Consumer, Generator):
    def __init__(self, index, parent, name):
        super().__init__(index, parent, name)
        self.energyCount = 0
