import mysql.connector as mysql
from aggregate.utils.utils import *
import aggregate.functions.batting as batting
import aggregate.functions.bowling as bowling
from aggregate.utils.percen

def aggregate_team(matches):
    avg = {
        "total_wins": 0,
        "bat_avg": 0,
        "cede_avg": 0,
        "wickets_avg": 0,
        "overs_bat_avg": [],
        "overs_cede_avg": [],
        "overs_wickets_sum": [],
        "balls_bat_avg": [],
        "balls_cede_avg": [],
        "balls_wickets_sum": [],
        "years": [],
        "recorded_matches": len(matches)
    }

    for _ in range(30):
        avg["overs_bat_avg"].append(0)
        avg["overs_cede_avg"].append(0)
        avg["overs_wickets_sum"].append(0)

    for _ in range(200):
        avg["balls_bat_avg"].append(0)
        avg["balls_cede_avg"].append(0)
        avg["balls_wickets_sum"].append(0)

    for k in matches:
        i = k
        avg["team"] = i["team"]

        if i["year"] not in avg["years"]:
            avg["years"].append(i["year"])

        avg["total_wins"] += 1 if i["win"] else 0
        avg["bat_avg"] += i["total_bat"]
        avg["cede_avg"] += i["total_cede"]
        avg["wickets_avg"] += i["total_wickets"]

        # stats per over no

        for j in range(len(i["overs_bat"])):
            avg["overs_bat_avg"][j] += i["overs_bat"][j]

        for j in range(len(i["overs_cede"])):
            avg["overs_cede_avg"][j] += i["overs_cede"][j]

        for j in range(len(i["overs_wickets"])):
            avg["overs_wickets_sum"][j] += i["overs_wickets"][j]

        # stats per ball no

        for j in range(len(i["balls_bat"])):
            avg["balls_bat_avg"][j] += i["balls_bat"][j]

        for j in range(len(i["balls_cede"])):
            avg["balls_cede_avg"][j] += i["balls_cede"][j]

        for j in range(len(i["balls_wickets"])):
            avg["balls_wickets_sum"][j] += i["balls_wickets"][j]

    avg["bat_avg"] /= len(matches)
    avg["cede_avg"] /= len(matches)
    avg["wickets_avg"] /= len(matches)

    for i in range(len(avg["overs_bat_avg"])):
        avg["overs_bat_avg"][i] /= len(matches)

    for i in range(len(avg["overs_cede_avg"])):
        avg["overs_cede_avg"][i] /= len(matches)

    for i in range(len(avg["balls_bat_avg"])):
        avg["balls_bat_avg"][i] /= 120

    for i in range(len(avg["balls_cede_avg"])):
        avg["balls_cede_avg"][i] /= 120

    avg.update({
        bowling_strike_rate: bowling.strike_rate(matches),
        bowling_strike_rate_percentile: 
    })

    return avg

def fetch_and_aggregate_team(team, db, start = "2007/08", duration = 1, end = "2023"):
    yearList = matchingYears(start, duration, end, ignoreEndYear=True)
    teamQuery = """SELECT * FROM teamMatches WHERE team = '{0}' AND year IN {1};"""

    c = db.cursor()
    c.execute(teamQuery.format(team, yearList))

    average = aggregate_team(allTeamMatchRecordToDictionary(c.fetchall()))

    return average