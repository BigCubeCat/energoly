from Objects.SolarGenerator import SolarGenerator
from Objects.WindGenerator import WindGenerator
from Objects.SteamGenerator import SteamGenerator
from Objects.Battery import Battery
from Objects.Consumers import Factory, HouseA, HouseB, Hospital
from Objects.Types.Edge import Edge
from Objects.Stations import StationA, StationB, MainStation

from loadModel import load_model


model = [load_model()]


def initObject(index_, parent, name):
    match name[0]:
        case 's':
            return SolarGenerator(index_, parent, name, 10, (2, 3))
        case 'a':
            return WindGenerator(index_, parent, name, 10, (1100, -250), 1, model)
        case 't':
            return SteamGenerator(index_, parent, name, 10)
        case 'b':
            return Hospital(index_, parent, name)
        case 'd':
            return HouseB(index_, parent, name)
        case 'h':
            return HouseA(index_, parent, name)
        case 'f':
            return Factory(index_, parent, name)
        case 'e':
            return StationA(index_, parent, name)
        case 'm':
            return StationB(index_, parent, name)
        case 'M':
            return MainStation(index_, name)
        case 'c':
            return Battery(index_, parent, name)


def add_from_graph(item, newDict, station_ports, stations, edges, objects, visit):
    elem = item[0]
    connection = item[1]
    name_parent = item[1][0]
    if elem in visit:
        return station_ports, stations, edges, objects, visit

    if not (name_parent in visit):
        detail_parent = newDict[name_parent]
        station_ports, stations, edges, objects, visit = add_from_graph(
            (name_parent, detail_parent), newDict, station_ports, stations, edges, objects, visit
        )

    edge_index = station_ports[connection[0]][connection[1] - 1]

    if elem.startswith('e') or elem.startswith('m'):
        stations.append(initObject(len(edges), edge_index, elem))

        # на данный момент зарегестрированна подстанция, но не кабели от нее
        count_new_edges = 3 if elem.startswith('e') else 2
        station_ports[elem] = []
        for e in range(count_new_edges):
            new_edge_index = len(edges)
            edges.append(Edge(new_edge_index, len(stations) - 1))
            station_ports[elem].append(new_edge_index)
    else:
        objects.append(initObject(len(objects), edge_index, elem))

    visit.append(elem)
    return station_ports, stations, edges, objects, visit


def createObjList(topology):
    newDict = {i['address']: (i['station'], i['line']) for i in topology}
    itemses = tuple(newDict.items())
    print(f"{itemses=}")

    parents_name = {detail[0] for detail in newDict.values()}
    main_station_name = [parent for parent in parents_name if parent.startswith('M')][0]
    stations = [MainStation(0, main_station_name)]  # Пока только главная подстанция
    edges = [Edge(0, 0), Edge(1, 0), Edge(2, 0)]  # Провода от главной подстанции
    objects = []
    # В каждой массив, каждый элемент которого - id подключенного к нему edge в массиве edges
    station_ports = {main_station_name: [0, 1, 2]}

    visit = [main_station_name]
    for item in itemses:
        station_ports, stations, edges, objects, visit = add_from_graph(item, newDict, station_ports, stations, edges, objects, visit)

    print(station_ports)
    print(*[str(e) for e in edges], sep="\n")
    print()
    print(*[s for s in stations], sep="\n")
    print()
    print(*[o for o in objects], sep="\n")
    print()
    return stations, edges, objects