import csv
import json

TeamNames = {
    "CSK": "CSK",
    "RR": "RR",
    "MI": "MI",
    "DC": "SRH",
    "DD": "DC",
    "KXIP": "KXIP",
    "KTK": "KTK",
    "RCB": "RCB",
    "RPS": "RPS",
    "PWI": "RPS",
    "KKR": "KKR",
    "DC": "SRH",
    "PK": "KXIP",
    "GT": "GT",
    "GL": "GT",
    "LSG": "LSG",
    "SRH": "SRH"
}

def main():
    file = open("team_ranking.csv")
    a = csv.reader(file)
    
    data = {}

    keys = []

    for i in a:
        if i[1] == "Team":
            keys = i[2:]
            continue

        # data.append(i)
        # print(i)

        actualKey = TeamNames[i[1]]
        values = i[2:]

        valuesDict = {}
        for a, b in zip(keys, values):
            valuesDict[a] = b

        data[actualKey] = valuesDict


    # print(json.dumps(data, indent=4))
    file.close()

    file = open("final_rankings.json", "w")
    json.dump(data, file)
    file.close()

main()