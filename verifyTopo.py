import json
from utils import fail, fail_n


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
