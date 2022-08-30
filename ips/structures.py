import sys
import json
import traceback
import math
import urllib.request
from collections import namedtuple, UserList
from argparse import Namespace
from copy import deepcopy

__all__ = [
    "Powerstand", "Object", "Line", "Powerline",
    "Historic", "Receipt", "ExchangeReceipt",
    "Diesel", "Cell",
]

def pretty_bool(v):
    return 'вкл.' if v else 'выкл.'


def pretty_agent(ag):
    return f'{ag["place"]}.{ag["player"]}'


def pretty_source(ag):
    if ag == "exchange":
        return 'контракт c оператором'
    elif ag == 'overload':
        return 'штраф за перегрузку'
    return f'контракт с игроком {ag["place"]}.{ag["player"]}'


def unsource(src):
    tag = src["esType"]
    if tag == "player":
        return src["owner"]
    return tag


def safe_tail(data):
    if len(data):
        return None
    return data[-1]


def safe_head(data):
    if len(data):
        return None
    return data[0]


Historic = namedtuple("Historic", ("now", "then"))
Historic.__str__ = lambda self: f"{self.now} (было {safe_tail(self.then)})"

Receipt = namedtuple("Receipt", ("income", "loss"))
Receipt.__str__ = lambda self: f"(+{self.income} ₽, -{self.loss} ₽)"
Receipt.__add__ = lambda self, x: __add_receipt(self, x)


def __add_receipt(self, x):
    if isinstance(x, Receipt):
        return Receipt(self.income + x.income, self.loss + x.loss)
    raise TypeError(x)


ExchangeReceipt = namedtuple("ExchangeReceipt", ("source", "flux", "price"))
ExchangeReceipt.__str__ = \
    lambda self: f"{pretty_source(self.source)} " \
                 f"({self.flux:.2f} МВт, {self.price:.2f} ₽/МВт)"

Forecasts = namedtuple("Forecasts", ("hospital", "factory", "houseA", "houseB", "sun", "wind"))

TotalPower = namedtuple("TotalPower", ("generated", "consumed", "external", "losses"))

Power = namedtuple("Line", ("generated", "consumed", "online"))
Power.__str__ = lambda self: f"{pretty_bool(self.online)} " \
                             f"(+{self.generated} МВт⋅ч -{self.consumed} МВт⋅ч)"
Power.total = lambda self: self.generated - self.consumed

Object = namedtuple("Object", ("id", "type", "contract", "address", "path",
                               "score", "power", "charge", "modules"))
Object.__str__ = lambda self: f"{self.type} ({self.power.now}, {self.score.now})"

Line = namedtuple("Line", ("id", "line"))
Line.__str__ = lambda self: f"{self.id}-{self.line}"

Powerline = namedtuple("Powerline", ("location", "online", "upflow", "downflow", "losses"))
Powerline.__str__ = lambda self: f"{self.location} ({pretty_bool(self.online)})"

Diesel = namedtuple("Diesel", ("power",))
Diesel.__str__ = lambda self: f"Дизель ({self.power})"

Cell = namedtuple("Diesel", ("charge", "delta"))
Cell.__str__ = lambda self: f"Аккумулятор ({self.charge})"

station_types = {"miniA", "miniB", "main"}
storage_types = {"miniA", "storage", "main"}


def make_module(m):
    if m["type"] == "cell":
        return Cell(m["charge"], m["delta"])
    if m["type"] == "diesel":
        return Diesel(m["power"])
    raise NotImplementedError("неизвестный модуль")


def make_historic(d, fn):
    return Historic(fn(**d["now"]), [fn(**x) for x in d["then"][::-1]])


def make_historic_(d, fn):
    return Historic(fn(d["now"]), [fn(x) for x in d["then"][::-1]])


def make_object(d, stations, storages):
    obj = Object(
        id=d["id"],
        address=tuple(d["address"]),
        contract=d["contract"],
        path=tuple(tuple(Line(tuple(l["id"]), l["line"]) for l in a) for a in d["path"]),
        score=make_historic(d["score"], Receipt),
        power=make_historic(d["power"], Power),
        charge=make_historic_(d["charge"], float),
        modules=tuple(make_module(m) for m in d["modules"]),
        type=d["class"]
    )
    if obj.type in station_types:
        stations[obj.address[0]] = obj.id
    if obj.type in storage_types:
        storages[obj.address[0]] = obj.id
    return obj


def make_powerline(d):
    d["location"] = tuple(Line(tuple(l["id"]), l["line"]) for l in d["location"])
    del d["owner"]
    return Powerline(**d)


def from_chipping(d):
    return Historic(d["current"], d["done"][::-1])


class ForecastSet(UserList):
    def __init__(self, *args, spread):
        super().__init__(*args)
        self.spread = spread


def make_forecast_set(d):
    return ForecastSet((tuple(row) for row in d["forecast"]),
                       spread=d["spread"])


class Powerstand:

    GRAPH_COUNT = 4

    def __init__(self, data, bloat_fields=False):
        self.__orders = orders = []
        self.__station_index = dict()
        self.__storage_index = dict()
        self.__user_data = [[] for _ in range(self.GRAPH_COUNT)]
        self.raw_data = data  # NOTE: deepcopy не делается, потому что долго и бесполезно

        # ИНВАРИАНТ: приходит состояние, подчищенное для конкретного игрока

        self.tick = data['tick']
        self.gameLength = data['conf']['gameLength']
        self.scoreDelta = Receipt(**data["scores"][0][1]["now"]["total"])

        self.fails = data['externalFail']

        self.wind = from_chipping(data['weatherWind'])
        self.sun = from_chipping(data['weatherSun'])

        self.objects = [make_object(obj, self.__station_index, self.__storage_index) 
                        for obj in data["objs"]]
        self.networks = {i+1: make_powerline(pl) for (i, pl) in enumerate(data["nets"])}
        raw_fc = data["forecasts"]
        self.forecasts = Forecasts(
            make_forecast_set(raw_fc["sfClass1"]),
            make_forecast_set(raw_fc["sfClass2"]),
            make_forecast_set(raw_fc["sfClass3A"]),
            make_forecast_set(raw_fc["sfClass3B"]),
            make_forecast_set(raw_fc["sfSun"]),
            make_forecast_set(raw_fc["sfWind"]),
        )

        self.exchange = [ExchangeReceipt(unsource(d["source"]), d["amount"], d["price"])
                         for d in data["exchangeReceipts"]]

        raw_tp = data["totalPowers"][0][1]["now"]
        self.total_power = TotalPower(raw_tp["totalGenerated"], raw_tp["totalConsumed"],
                                      raw_tp["totalFromExternal"], raw_tp["totalLost"])

        if bloat_fields:
            self.scoreTotal = sum(map(lambda x: Receipt(**x["total"]),
                                  data["scores"][0][1]["then"]),
                                  self.scoreDelta)
            self.topo = {c.location: i for (i, c) in self.networks.items()}

        self.orders = Namespace(
            diesel=lambda address, power: self.__set_diesel(address, power),
            charge=lambda address, power: self.__change_cell(address, power, True),
            discharge=lambda address, power: self.__change_cell(address, power, False),
            sell=lambda amount, price: self.__outstanding(amount, price, True),
            buy=lambda amount, price: self.__outstanding(amount, price, False),
            line_on=lambda address, line: self.__set_line(address, line, True),
            line_off=lambda address, line: self.__set_line(address, line, False),
            add_graph=lambda idx, values: self.__add_graph(idx, values),
            # debug functions
            get=lambda: orders.copy(),
            humanize=lambda: self.__humanize_orders(),
        )

    def __check_address(self, address):
        return address in self.__station_index

    def __set_diesel(self, address, power):
        try:
            power = float(power)
            if power < 0:
                self.__warn_tb("Отрицательное значение энергии на дизеле. "
                               "Приказ не принят.", cut=3)
                return
        except ValueError:
            self.__warn_tb("Для приказа на дизель нужен float-совместимый "
                           "тип. Приказ не принят.", cut=3)
            return
        if not self.__check_address(address):
            self.__warn_tb("Такой подстанции не существует. "
                           "Приказ не принят.", cut=3)
            return
        self.__orders.append({"orderT": "diesel", "address": address, "power": power})

    def __change_cell(self, address, power, charge=True):
        try:
            power = float(power)
            if power < 0:
                self.__warn_tb("Отрицательное значение энергии в приказе на аккумулятор. "
                               "Приказ не принят.", cut=3)
                return
        except ValueError:
            self.__warn_tb("Для приказа на аккумулятор нужен float-совместимый "
                           "тип. Приказ не принят.", cut=3)
            return
        if address not in self.__storage_index:
            self.__warn_tb("Такого накопителя/подстанции не существует. "
                           "Приказ не принят.", cut=3)
            return
        order = "charge" if charge else "discharge"
        self.__orders.append({"orderT": order, "address": address, "power": power})

    def __outstanding(self, amount, price, sell=True):
        try:
            amount = float(amount)
            if amount < 0:
                self.__warn_tb("Неположительное значение энергии в заявке на биржу. "
                               "Приказ не принят.", cut=3)
                return
        except ValueError:
            self.__warn_tb("Для заявки на биржу нужно float-совместимое "
                           "значение энергии. Приказ не принят.", cut=3)
            return
        try:
            price = float(price)
            if price < 0:
                self.__warn_tb("Неположительное значение стоимости в заявке на биржу. "
                               "Приказ не принят.", cut=3)
                return
        except ValueError:
            self.__warn_tb("Для заявки на биржу нужно float-совместимое "
                           "значение стоимости. Приказ не принят.", cut=3)
            return
        order = "sell" if sell else "buy"
        self.__orders.append({"orderT": order, "amount": amount, "price": price})

    def __set_line(self, address, line, value=True):
        try:
            line_obj = self.__station_index[address]
        except KeyError:
            self.__warn_tb("Запрос на линию несуществующей подстанции. "
                           "Приказ не принят.", cut=3)
            return
        order = "lineOn" if value else "lineOff"
        self.__orders.append({"orderT": order, "line": {"id": line_obj, "line": line},
                              "address": address})
        pass

    def __commit(self):
        self.__orders.append({"orderT": "userData", "data": self.__user_data})
        data = json.dumps(self.__orders).encode()
        request = urllib.request.urlopen("http://localhost:26000/orders", data=data)
        if request.getcode() != 200:
            raise ConnectionRefusedError("Couldn't send data to server")
        return 0

    def get_orders(self):
        return self.__humanize_orders()

    def get_user_data(self):
        return deepcopy(self.__user_data)

    def save_and_exit(self):
        sys.exit(self.__commit())

    @staticmethod
    def safe_float(v):
        try:
            v = float(v)
            if not math.isfinite(v):
                Powerstand.__warn_tb("Неконечное число в графике. "
                                     "Заменено на 0.", cut=5)
                return 0
            return v
        except ValueError:
            Powerstand.__warn_tb("Несовместимое с float значение в графике. "
                                 "Заменено на 0.", cut=5)
            return 0
        
    def __add_graph(self, idx, values):
        if not (0 <= idx < self.GRAPH_COUNT):
            self.__warn_tb("Неверный номер плоскости для добавления графика. "
                           "Приказ не принят.", cut=3)
            return
        values = [Powerstand.safe_float(x)
                  for x in values[:self.gameLength]]
        self.__user_data[idx].append(values)

    @staticmethod
    def __warn_tb(error, warning=False, cut=2):
        level = "Предупреждение" if warning else "Ошибка"
        print("".join(traceback.format_list(traceback.extract_stack()[:-cut])) +
              f"{level}: {error}", file=sys.stderr, flush=True)

    def __humanize_orders(self):
        return [self.humanize_order(o) for o in self.__orders]

    @staticmethod
    def humanize_order(order):
        type = order["orderT"]
        if type == "lineOn":
            return f"включение линии {order['line']['line']} " \
                   f"на подстанции {order['address']}"
        if type == "lineOff":
            return f"выключение линии {order['line']['line']} " \
                   f"на подстанции {order['address']}"
        if type == "sell":
            return f"заявка на продажу {order['amount']:.2f} МВт⋅ч за {order['price']:.2f} ₽"
        if type == "buy":
            return f"заявка на покупку {order['amount']:.2f} МВт⋅ч за {order['price']:.2f} ₽"
        if type == "diesel":
            return f"установка мощности дизелей {order['address']} в {order['power']:.2f} МВт"
        if type == "charge":
            return f"зарядка аккумуляторов {order['address']} на {order['power']:.2f} МВт⋅ч"
        if type == "discharge":
            return f"разрядка аккумуляторов {order['address']} на {order['power']:.2f} МВт⋅ч"
        if type == "userData":
            return "отправить графики"
        else:
            return "неизвестный приказ"
