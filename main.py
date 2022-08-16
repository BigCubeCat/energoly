#! python
import random
import Types
from Objects.WindGenerator import *

station = Types.Station(index=0, parents=[], name="main", criticalDamage=50);
edge = Types.Edge(index=1, parent=station.index, criticalDamage=5)
factory = Types.Consumer(index=2, parents=[1], name="fA")


## Типа аукцион
factory.setBill(10)
if __name__ == "__main__":
    for i in range(100):
        factory.update(random.randint(1, 10))
    print(factory.totatBill)

