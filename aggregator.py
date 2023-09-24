import mysql.connector as mysql
from data import connectToDatabase, db, importJSON
import json
from credentials import defaultDatabase
from aggregate.utils import *
    

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

    return avg


def aggregate_teams(team1, team2, db, start = "2007/08", duration = 1, end = "2023"):
    yearList = matchingYears(start, duration, end, ignoreEndYear=True)
    teamQuery = """SELECT * FROM teamMatches WHERE team = '{0}' AND year IN {1};"""

    print(teamQuery.format(team1, yearList))

    c1 = db.cursor()
    c1.execute(teamQuery.format(team1, yearList))
    avg1 = aggregate_team(allTeamMatchRecordToDictionary(c1.fetchall()))
    print(json.dumps(avg1, indent=2))

    c2 = db.cursor()
    c2.execute(teamQuery.format(team2, yearList))
    avg2 = aggregate_team(allTeamMatchRecordToDictionary(c2.fetchall()))
    print(json.dumps(avg2, indent=2))

    open("team1.json", "w").write(json.dumps(avg1))
    open("team2.json", "w").write(json.dumps(avg2))


def aggregate(team=False, season_start=False, season_end=False, season_duration=False, match=False, ):
    db = defaultDatabase()

    aggregate_teams("RCB", "CSK", db, duration=7)

    # cursor = db.cursor()

    # cursor.execute("SELECT * FROM performances;")

    # print(cursor.fetchall())


aggregate("")
