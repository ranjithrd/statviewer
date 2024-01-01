import json

order = {
    1: "2007/08",
    2: "2009",
    3: "2009/10",
    4: "2011",
    5: "2012",
    6: "2013",
    7: "2014",
    8: "2015",
    9: "2016",
    10: "2017",
    11: "2018",
    12: "2019",
    13: "2020/21",
    14: "2021",
    15: "2022",
    16: "2023"
}

split_seasons_convert_to = {
    1: 2007,
    2: 2009,
    3: 2010,
    4: 2011,
    5: 2012,
    6: 2013,
    7: 2014,
    8: 2015,
    9: 2016,
    10: 2017,
    11: 2018,
    12: 2019,
    13: 2020,
    14: 2021,
    15: 2022,
    16: 2023
}

defaultStart = "2007/08"
defaultEnd = "2023"

numOvers = 30
numBalls = 120

try:
    f = open("constants.json", "r")
    data = json.loads(f.read())

    if "order" in data:
        order = data["order"]
        newOrder = {}
        for i in order:
            newOrder[int(i)] = order[i]
        order = newOrder
    if "split_seasons_convert_to" in data:
        split_seasons_convert_to = data["split_seasons_convert_to"] 
        newS = {}
        for i in split_seasons_convert_to:
            newS[int(i)] = split_seasons_convert_to[i]
        split_seasons_convert_to = newS

    if "defaultStart" in data:
        defaultStart = data["defaultStart"]
        defaultEnd = data["defaultEnd"]

    if "numOvers" in data:
        numOvers = data["numOvers"]
        numBalls = data["numBalls"]

    print(order)
except:
    print("constants.json does not exist")