stub_input = {
    "nets": [{"upflow": 20.90154792699549,  # Генерация
              "online": True,  # Включена
              "location": [],  # [(ID подстанции, № линии)]
              "downflow": 4.180309588814707,  # Потребление
              "owner": {"place": 1, "player": 1},  #
              "wear": 0,  # Износ ветки
              "broken": 0,  # Оставшееся время восстановления после аварии
              "losses": 0,  # Потери
              "id": 1}  # id
             ],
    "objs": [{"path": [[]],  # Энергорайоны | [адрес энергорайона]
              "score": {"now": {"loss": 0, "income": 0},  # Доход/расход
                        "then": [{"loss": 0, "income": 0}, {"loss": 0, "income": 0},
                                 {"loss": 0, "income": 0}, {"loss": 0, "income": 0}]},
              "trajectory": None,  # ?
              "address": ["M1"],  # Адрес
              "modules": [],  # Модули подстанции | [Cell или Diesel]
              "owner": {"place": 1, "player": 1},  #
              "power": {"now": {"online": True, "consumed": 0, "generated": 0},  # Потребление/генерация/включен
                        "then": [{"online": True, "consumed": 0, "generated": 0},
                                 {"online": True, "consumed": 0, "generated": 0}]},
              "contract": 0,  # Тариф
              "charge": {"now": 0,  # Заряд накопителя
                         "then": [0, 0]},
              "id": ["main", 1],  # (тип, номер)
              "failed": False,  # Сломан
              "class": "main",  # тип
              "topolocation": [1]}  # ?
             ],
    "conf": {"exchangeMinPrice": 2, "seedForPattern": 352, "cellModuleChargeRate": 10,
             "cellModuleDischargeRate": 10, "exchangeExternalAdvanceBuy": 5,
             "exchangeExternalLastMomentSell": 1, "wearAccumulationA": 2.3, "wearFailDuration": 5,
             "externalFailure": [20, 10, 15, 15, 5, 15], "varianceSun": 0.5, "tpsEceZeroValue": 0.4,
             "externalLimit": 50, "corridorClass2": 0.5, "class1PowerScale": 2, "tpsEcePeakValue": 0.9,
             "blockOnSandboxes": False, "wearProbabilityThreshold": 0.8, "corridorClass3B": 0.5,
             "cellObjectChargeRate": 15, "dieselFuelCost": 4, "forecastsCount": 8, "tpsInertia": 0.6,
             "tpsFuelCost": 3.5, "seedForImplementation": 216, "wearAccumulationB": 15,
             "weatherEffectsDelay": 2, "dieselMaxPower": 5, "varianceClass2": 0.5,
             "cellModuleMaintenance": 5, "failFineThreshold": 10, "varianceClass3A": 0.5,
             "class1FineRate": 8, "weatherMaxSun": 15, "tpsEcePeakPower": 8, "corridorSun": 0.5,
             "windRecoveryValue": 0.25, "tpsMaxPower": 10, "cellObjectCapacity": 100,
             "failOverpowerFine": 10, "windSummit": 0.3, "maxWindPower": 15, "dieselMaintenance": 1,
             "exchangeMaxPrice": 5, "varianceClass3B": 0.5, "class2FineRate": 4,
             "exchangeExternalAdvanceSell": 2, "minTickTime": 3, "lossesThreshold": 10,
             "exchangeExternalLastMomentBuy": 10, "class3PowerScale": 1, "varianceClass1": 0.25,
             "gameLength": 100, "cellObjectDischargeRate": 15, "wearProbabilityA": 4,
             "blockOnArbiters": False, "lossesLimit": 0.2, "wearRecoveryRate": 0.4, "maxSolarPower": 15,
             "players": [[{"place": 1, "player": 1}, "Player 1"],
                         [{"place": 1, "player": 2}, "Player 2"],
                         [{"place": 1, "player": 3}, "Player 3"],
                         [{"place": 1, "player": 4}, "Player 4"],
                         [{"place": 1, "player": 5}, "Player 5"],
                         [{"place": 1, "player": 6}, "Player 6"],
                         [{"place": 1, "player": 7}, "Player 7"],
                         [{"place": 1, "player": 8}, "Player 8"],
                         [{"place": 1, "player": 9}, "Player 9"],
                         [{"place": 1, "player": 10}, "Player 10"],
                         [{"place": 1, "player": 11}, "Player 11"]], "corridorWind": 0.5,
             "cellModuleCapacity": 50, "windBreakValue": 0.4, "corridorClass3A": 0.5,
             "weatherMaxWind": 15, "corridorClass1": 0.25, "exchangeMaxAmount": 50,
             "class2PowerScale": 1, "exchangeCommission": 0.1, "class3FineRate": 2,
             "wearProbabilityB": 8, "gameTitle": "Test-Preflight", "tpsInertiaFriction": 0.5},
    "externalFail": [False, False, False, False, False, False, False, False, False, False, False, False,
                     False, False, False, False, False, False, False, False, True, True, True, True,
                     True, True, True, True, True, True, False, False, False, False, False, False,
                     False, False, False, False, False, False, False, False, False, True, True, True,
                     True, True, True, True, True, True, True, True, True, True, True, True, False,
                     False, False, False, False, True, True, True, True, True, True, True, True, True,
                     True, True, True, True, True, True, False, False, False, False, False, False,
                     False, False, False, False, False, False, False, False, False, False, False, False,
                     False, False],  # Тики аварий
    "exchangeTicketsNow": [],  # ??????????
    "tick": 100,  # Кол-во тиков в игре
    "forecasts": {  # Прогнозы погоды из файлика с погрешностью
        "sfWind": {"forecast": [[], [0, 0, 0, 0, 0.2921963179016677, 0.8124097190852294, 1.0216344601312446,
                                     0.9272656534262635, 0.565032839536231,
                                     0.954270434877628, 0.9776119780997712, 1.3257326523854265, 1.3675174703284017,
                                     2.0834382783449907,
                                     2.1928313595975166, 2.974089822931289, 3.904555554336753, 3.707817208155308,
                                     3.699693184565978,
                                     4.06669062683965, 4.149278663157932, 4.092444085958765, 3.983314333206267,
                                     4.388586679830027,
                                     4.715704634838533, 4.2754375745540205, 4.2754375745540205, 5.235593807227881,
                                     6.6073962576184355,
                                     5.491363934581015, 7.4491179792897295, 7.061504839453841, 7.17250670139466,
                                     7.1052899770743165,
                                     6.656401075980961, 6.195337408121715, 5.912567905980184, 5.825997926335272,
                                     5.590117093244394,
                                     5.629316105624402, 5.72660145606405, 5.951597849100899, 7.479852334693108,
                                     9.82068724501251,
                                     10.764542675509874, 10.925855747798018, 10.636722181869752, 10.468481820665538,
                                     11.425335285507913,
                                     11.373867636064425, 12.061711186804422, 12.47527618571058, 12.47527618571058,
                                     12.966631134094461,
                                     12.617750573927081, 12.226342820049469, 11.65497670740443, 10.995650878159305,
                                     9.699171225207332,
                                     10.648745336919648, 10.30309830566419, 9.950796539517553, 8.970030878107504,
                                     9.239522188472474,
                                     8.56209067761494, 8.320591523324476, 8.323833773672314, 7.152620286002393,
                                     6.906525288238188,
                                     6.706966715063302, 6.565623451420434, 6.994543931411214, 7.0956401720191495,
                                     6.643471139411809,
                                     6.413561167421301, 6.224466997598062, 5.72770792611275, 5.2275897245336775,
                                     5.2275897245336775,
                                     4.989829211555913, 5.100804496715498, 4.684488972532064, 5.412969148965891,
                                     5.053875813919025,
                                     5.817909884826742, 5.2804412786903, 5.76833833183209, 6.705209070203842,
                                     6.779820823067325, 6.337329626625245,
                                     6.429787035186758, 6.85352005894405, 7.919990964076772, 9.027283920607472,
                                     8.078309179547814,
                                     7.125689066497341, 7.577165181977158, 7.7962804333772215, 7.782716382629362,
                                     7.6625763661507476], [], [], [], [], [], []], "spread": 0.5}
    },
    "userData": '',  # Графики
    "exchangeTicketsFuture": [],  # ??????????
    "topo": [[  # Энергорайоны
        {"place": 1, "player": 1}, [[1, []],
                                    [2, [{"line": 1, "id": ["main", 1]}]],
                                    [3, [{"line": 2, "id": ["main", 1]}]],
                                    [4, [{"line": 3, "id": ["main", 1]}]],
                                    [5, [{"line": 2, "id": ["main", 1]}, {"line": 1, "id": ["miniB", 1]}]],
                                    [6, [{"line": 2, "id": ["main", 1]}, {"line": 2, "id": ["miniB", 1]}]]]
    ]],
    "exchangeReceipts": [{"amount": -16.721238338180783, "owner": {"place": 1, "player": 1},  # Биржа
                          "source": {"esType": "exchange"}, "price": 1}],
    "weatherWind": {
        "done": [2.4663175124868384, 2.475413885309406, -0.2611678670598525], "incoming": [], "current": 0},
    "orders": [
        {"owner": {"place": 1, "player": 1}, "order": {"line": {"line": 2, "id": ["main", 1]}, "orderT": "lineOn"}}
    ],
    "weatherSun": {
        "done": [-0.41681411208332464, 0.02627884674634018, -0.12330687639221882], "incoming": [], "current": 0},
    "scores": [[
        {"place": 1, "player": 1},
        {"now": {"con": {"loss": 0, "income": 0},
                 "overload": {"loss": 0, "income": 0},
                 "exchange": {"loss": 0, "income": 16.721238338180783},
                 "auction": {"loss": 0, "income": 0},
                 "gen": {"loss": 20, "income": 0},
                 "total": {"loss": 23, "income": 16.721238338180783},
                 "grid": {"loss": 3, "income": 0}},
         "then": []}
    ]],
    "totalPowers": [[
        {"place": 1, "player": 1},
        {"now": {"consumedClass1": 0,
                 "cellsGenerated": 0,
                 "totalGenerated": 20.90154792699549,
                 "cellsConsumed": 0,
                 "generatedTPS": 0,
                 "hypotheticallyGenerated": 20.90154792699549,
                 "totalLost": 4.180309588814707,
                 "totalFromExternal": -16.721238338180783,
                 "diesels": 0,
                 "generatedSolar": 20.888671875,
                 "consumedClass2": 0,
                 "exchangeAdvanceBought": 0,
                 "exchangeLastMomentBought": 0,
                 "totalConsumed": 0,
                 "consumedClass3": 0,
                 "exchangeLastMomentSold": 16.721238338180783,
                 "exchangeAdvanceSold": 0,
                 "generatedWind": 0.012876051995489336,
                 "hypotheticallyConsumed": 0},
         "then": []}
    ]]
}
