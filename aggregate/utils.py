import json

def teamMatchRecordToDictionary(i):
    return {
        "team_match_id": i[0],
        "match_id": i[1],
        "year": i[2],
        "team": i[3],
        "win": i[4],
        "total_bat": i[5],
        "total_cede": i[6],
        "total_wickets": i[7],
        "overs_bat": json.loads(i[8]),
        "overs_cede": json.loads(i[9]),
        "overs_wickets": json.loads(i[10]),
        "balls_bat": json.loads(i[11]),
        "balls_cede": json.loads(i[12]),
        "balls_wickets": json.loads(i[13]),
        "fall_of_wickets": json.loads(i[14])
    }

def allTeamMatchRecordToDictionary(i):
    a = []
    for j in i:
        a.append(teamMatchRecordToDictionary(j))

    return a

def matchingYears(start_year, duration = 1, end_year = "", ignoreEndYear = False):
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
        16: "2023",
    }

    orderInverse = {}
    for i in order:
        orderInverse[order[i]] = i

    if duration == 1 and end_year == "":
        return "('%s')"%(start_year)
    else:
        start = orderInverse[start_year]
        if duration != 1 and ignoreEndYear:
            end = start + duration
        else:
            end = orderInverse[end_year]

        r = range(start, end + 1)
        ret = []
        for i in r:
            ret.append("'" + str(order[i]) + "'")

        return "(" + ",".join(ret) + ")"

# output "('2011', '2012', '2013')"
# sample input: matchingYears("2007/08", 7, "2023", ignoreEndYear=True)