import json
import sys
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


def getObjList(topology):
	
	for i in topology:
		if i["station"][0] == "M":
			main_station_number = int(i["station"][1])
			break
	topology.append({'address': f'M{main_station_number}', 'station': f'M{main_station_number}', 'line': None})

	objList, edges = list(), list()
	
	newDict = {i['address']:(i['station'], i['line']) for i in topology}
	
	itemses = tuple(newDict.items())
	print(itemses)
	for index_, i in enumerate(itemses):
		ind = len(newDict) + len(edges) 
		
		station = i[1][0]
		parent = itemses.index( (station, newDict[station]) )
		#print(i, parent, station)
		edges.append( Edge(ind,  parent, 100))


		match i[0][0]:
			case 's':
				objList.append( SolarGenerator(index_, parent, i[0], 10, None, None) )
			case 'a':
				objList.append( WindGenerator(index_, parent, i[0], 10, None, None, None) )
			case 't':
				objList.append( SteamGenerator(index_, parent, i[0], 10) )
			case 'b':
				objList.append( Hospital(index_, parent, i[0]) )
			case 'd':
				objList.append( HouseB(index_, parent, i[0]) )
			case 'h':
				objList.append( HouseA(index_, parent, i[0]) )
			case 'f':
				objList.append( Factory(index_, parent, i[0]) )
			case 'e':
				objList.append( StationA(index_, parent, i[0], 100) )
			case 'm':
				objList.append( StationB(index_, parent, i[0], 100) )
			case 'M':
				objList.append( MainStation(index_, parent, i[0], 100) )
			case 'c':
				objList.append( Battery(index_, parent, i[0]) ) 
  
	for i in objList + edges:
		print(i)
	return objList + edges
	
def main():
    print(sys.argv)
    if len(sys.argv) == 2:
        filename = sys.argv[-1]
        try:
            with open(filename) as fin:
                d = json.load(fin)
            verify(d)
            
            return getObjList(d)
        except (FileNotFoundError, IsADirectoryError):
            fail("Файл", filename, "не найден")
        except json.decoder.JSONDecodeError as e:
            fail(e)
        
    if len(sys.argv) == 3 and sys.argv[1] == "generate":
        filename = sys.argv[-1]
        try:
            with open(filename) as fin:
                d = fin.read()
            generate(d, filename)
            return
        except (FileNotFoundError, IsADirectoryError):
            fail("Файл", filename, "не найден")
    fail(sys.argv[0], "<topology.json>")


if __name__ == "__main__":
    main()
