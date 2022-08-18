import json
import sys

from utils import load_model

from Objects.SolarGenerator import SolarGenerator
from Objects.WindGenerator import WindGenerator
from Objects.SteamGenerator import SteamGenerator
from Objects.Battery import Battery
from Objects.Consumers import Factory, HouseA, HouseB, Hospital
from Objects.Types.Edge import Edge
from Objects.Stations import StationA, StationB, MainStation

obj_types = [
    ("e", "Миниподстанции А"),
    ("m", "Миниподстанции Б"),
    ("h", "Дома А"),
    ("d", "Дома Б"),
    ("f", "Заводы"),
    ("b", "Больницы"),
    ("c", "Накопители"),
    ("s", "СЭС"),
    ("a", "ВЭС"),
    ("t", "ТЭС"),
]
model = [load_model()]


def fail(*args):
    print("Ошибка:", *args)
    exit(1)


def fail_n(i, *args):
    print("Ошибка в элементе", i, ":", *args)
    exit(1)


def verify(d):
    object_list = list()
    if not isinstance(d, list):
        fail("Ошибка формата: должен быть список.")
    objs = set()
    topo = dict()
    main_station = None
    for i, v in enumerate(d):
        # Python — язык с динамической типизацией...
        if not isinstance(v, dict):
            fail_n(i, "Должен быть словарь.")
        address = v.get("address")
        if not isinstance(address, str):
            fail_n(i, "Должен быть ключ 'address' со строковым значением.")
        if address in objs:
            fail("Адрес", address, "повторился в элементе", i)
        if len(address) != 2 or address[0] not in "hemsafbdct":
            fail_n(i, "Неизвестный объект", address)

        station = v.get("station")
        if not isinstance(station, str):
            fail_n(i, "Должен быть ключ 'station' со строковым значением.")
        line = v.get("line")
        if not isinstance(line, int):
            fail_n(i, "Должен быть ключ 'line' с целочисленным значением.")

        if station[0] == "M":
            if main_station is None:
                main_station = station
            elif station != main_station:
                fail("Две главных подстанции –", station, "и", main_station)
        elif station[0] == 'm':
            if not (1 <= line <= 2):
                fail_n(i, "На подстанции", station, "нет ветки с номером", line)
        elif station[0] == 'e':
            if not (1 <= line <= 3):
                fail_n(i, "На подстанции", station, "нет ветки с номером", line)
        else:
            fail_n(i, "Подстанции", station, "не существует")

        objs.add(address)
        topo.setdefault((station, line), set()).add(address)

    if main_station is None:
        fail("Нет главной подстанции")

    for ((st, sl), line_objs) in topo.items():
        f_prod, f_gen = False, False
        for x in line_objs:
            if x[0] in "hdfb":
                f_prod = True
            elif x[0] in "sat":
                f_gen = True
            elif x[0] in "cme":
                pass
            else:
                fail("Объекта", x, "не существует")
        if f_prod and f_gen:
            fail(f"На ветке {st}-{sl} смешаны потребление и накопление")

    # А проверку на разные ветки больницы делайте сами ;)
    print(objs)
    print("Главная подстанция:", main_station)
    for (c, name) in obj_types:
        xs = sorted(x for x in objs if x[0] == c)
        if xs:
            print(name + ":", " ".join(xs))
    print()
    topos = sorted(topo.items(), key=lambda x: ("Mme".find(x[0][0][0]), x[0]))
    for ((st, sl), objs) in topos:
        print(f"{st}-{sl}:", " ".join(sorted(objs)))


def generate(s: str, filename="topo"):
    d = []
    main_station = None
    for i, l in enumerate(s.splitlines()):
        try:
            line, toks = l.split(":")
        except ValueError:
            fail_n(i, "ожидалось двоеточие")
        try:
            station, line = line.split("-")
        except ValueError:
            fail_n(i, "ожидался дефис в обозначении линии")
        try:
            line = int(line)
        except ValueError:
            fail_n(i, "некорректный номер линии")

        if station[0] == "M":

            if main_station is None:
                main_station = station
            elif station != main_station:
                fail("Две главных подстанции –", station, "и", main_station)
        elif station[0] == 'm':
            if not (1 <= line <= 2):
                fail_n(i, "На подстанции", station, "нет ветки с номером", line)
        elif station[0] == 'e':
            if not (1 <= line <= 3):
                fail_n(i, "На подстанции", station, "нет ветки с номером", line)
        else:
            fail_n(i, "Подстанции", station, "не существует")

        for obj in toks.split():
            d.append({
                "station": station,
                "line": line,
                "address": obj
            })
    verify(d)
    with open(filename + ".json", "w") as fout:
        json.dump(d, fout, indent=2)


def initObject(index_, parent, name):
    match name[0]:
        case 's':
            return SolarGenerator(index_, parent, name, 10, [1]*100, (2, 3))
        case 'a':
            return WindGenerator(index_, parent, name, 10, [1]*100, (1100, -250), 1, model)
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
            return MainStation(index_, parent, name)
        case 'c':
            return Battery(index_, parent, name)



def getObjList(topology):
    # get main station name
    str_topology = str(topology)
    m_index = str_topology.index('M')
    main_station_name = "M" + str_topology[m_index + 1]
    stations = [MainStation(0, main_station_name)] # Пока только главная подстанция
    edges = [Edge(0, 0), Edge(1, 0), Edge(2, 0)] # Провода от главной подстанции
    objects = []

    newDict = {i['address']: (i['station'], i['line']) for i in topology}
    print(newDict)

    itemses = tuple(newDict.items())
    print(f"{itemses=}")
    print(len(itemses))
    # В каждой массив, каждый элемент которого - id подключенного к нему edge в массиве edges
    station_ports = {main_station_name: [0, 1, 2]}  
    for elem, connection in newDict.items():
        if elem.startswith('e') or elem.startswith('m'):
            edge_index = station_ports[connection[0]][connection[1] - 1] # получение номера линии в edges
            station_object = initObject(len(edges), edge_index, elem)
            stations.append(station_object)
            # на данный момент зарегестрированна подстанция, но не кабели от нее
            count_new_edges = 3 if elem.startswith('e') else 2
            station_ports[elem] = []
            for e in range(count_new_edges):
                new_edge_index = len(edges)
                edges.append(Edge(new_edge_index, len(stations) - 1))
                station_ports[elem].append(new_edge_index)
    for elem, connection in newDict.items():
        if not (elem.startswith('e') or elem.startswith('m')):
            edge_index = station_ports[connection[0]][connection[1] - 1] # получение номера линии в edges
            objects.append(initObject(len(objects), edge_index, elem))
    print(station_ports)
    print(*[str(e) for e in edges], sep="\n")
    print()
    print(*[s for s in stations], sep="\n")
    print()
    print(*[o for o in objects], sep="\n")
    print()
    return stations, edges, objects


def read_topology(filename):
    try:
        with open(filename) as fin:
            d = json.load(fin)
        verify(d) # Проверка топологии на корректность
        return getObjList(d) # Наше ВСЕ!

    except (FileNotFoundError, IsADirectoryError):
        fail("Файл", filename, "не найден")
    except json.decoder.JSONDecodeError as e:
        fail(e)


if __name__ == "__main__":
    read_topology(sys.args[-1], None)

