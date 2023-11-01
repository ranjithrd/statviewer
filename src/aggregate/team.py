import mysql.connector as mysql
from src.aggregate.utils.utils import *
import src.aggregate.functions.batting as batting
import src.aggregate.functions.bowling as bowling
import src.aggregate.utils.percentile as percentile
from src.aggregate.utils.split_seasons import generateDataPoints, splitAcrossSeasons
from src.data.load import allData

def aggregate_team(matches):
    print(len(matches))
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
        "balls_wickets_avg": [],
        "balls_wickets_sum": [],
        "years": [],
        "recorded_matches": len(matches),
        "wickets_as_of_ball": [0],
        "bat_as_of_ball": [0],
        "cede_as_of_ball": [0]
    }

    for _ in range(30):
        avg["overs_bat_avg"].append(0)
        avg["overs_cede_avg"].append(0)
        avg["overs_wickets_sum"].append(0)

    for _ in range(200):
        avg["balls_bat_avg"].append(0)
        avg["balls_cede_avg"].append(0)
        avg["balls_wickets_sum"].append(0)
        avg["balls_wickets_avg"].append(0)

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
            avg["balls_wickets_avg"][j] += i["balls_wickets"][j]

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

    for i in range(len(avg["balls_wickets_avg"])):
        avg["balls_wickets_avg"][i] /= len(matches)

    for j in range(200):
        avg["wickets_as_of_ball"].append(
            avg["wickets_as_of_ball"][-1] + round(avg["balls_wickets_avg"][j], 2))

    for j in range(200):
        avg["bat_as_of_ball"].append(
            avg["bat_as_of_ball"][-1] + round(avg["balls_bat_avg"][j], 2))
    
    for j in range(200):
        avg["cede_as_of_ball"].append(
            avg["cede_as_of_ball"][-1] + round(avg["cede_as_of_ball"][j], 2))

    ad = groupByTeams(allData()).values()

    # bowling stats
    avg.update(generateDataPoints(bowling.strike_rate,
               matches, "bowling_strike_rate", ad))
    avg.update(generateDataPoints(
        bowling.economy, matches, "bowling_economy", ad))
    avg.update(generateDataPoints(
        bowling.average, matches, "bowling_average", ad))
    avg.update(generateDataPoints(bowling.runs_conceded,
               matches, "bowling_runs_conceded", ad))
    avg.update(generateDataPoints(bowling.wickets_taken,
               matches, "bowling_wickets_taken", ad))

    # batting stats
    avg.update(generateDataPoints(batting.run_rate,
               matches, "batting_run_rate", ad))
    avg.update(generateDataPoints(batting.strike_rate,
               matches, "batting_strike_rate", ad))
    avg.update(generateDataPoints(
        batting.batting_average, matches, "batting_average", ad))
    avg.update(generateDataPoints(batting.runs_scored,
               matches, "batting_runs_scored", ad))
    
    # match statistics
    avg.update({
        "total_matches_played": len(matches),
        "total_matches_won": 0,
        "percentage_matches_won_city": {},
        "matches_played_city": {}
    })

    def percentage_matches(m):
        total_matches = 0
        won = 0
        for i in m:
            total_matches += 1
            won += int(i["win"])

        return round(100 * won / total_matches, 2)

    def percentage_when_matches_won(m):
        total_matches = 0
        toss_won = 0
        for i in m:
            total_matches += 1
            toss_won += int(i["toss_won"])

        return round(100 * toss_won / total_matches, 2)
    
    def percentage_when_matches_lost(m):
        return 100 - percentage_when_matches_won(m)
    
    avg.update({
        "percentage_matches_won_toss_won": percentage_when_matches_won(matches),
        "percentage_matches_won_toss_won_split_seasons": splitAcrossSeasons(percentage_when_matches_won, matches),
        "percentage_matches_won_toss_lost": percentage_when_matches_lost(matches),
        "percentage_matches_won_toss_lost_split_seasons": splitAcrossSeasons(percentage_when_matches_lost, matches)
    })
        
    for i in matches:
        if i["city"] not in avg["percentage_matches_won_city"]:
            avg["percentage_matches_won_city"][i["city"]] = 0
            avg["matches_played_city"][i["city"]] = 0

        avg["matches_played_city"][i["city"]] += 1

        if i["win"]:
            avg["total_matches_won"] += 1
            avg["percentage_matches_won_city"][i["city"]] += 1

    for i in avg["percentage_matches_won_city"]:
        avg["percentage_matches_won_city"][i] = round(100 * (avg["percentage_matches_won_city"][i] / avg["matches_played_city"][i]), 2)

    avg.update({
        "percentage_matches_won": round(100 * (avg["total_matches_won"] / avg["total_matches_played"]), 2),
        "percentage_matches_won_split_seasons": splitAcrossSeasons(percentage_matches, matches)
    })

    # record statistics
    def highest_score(m):
        s = []
        for i in m:
            s.append(i["total_bat"])
        return max(s)

    def lowest_cede(m):
        s = [10e100]
        for i in m:
            if i["total_cede"] > 0 and i["over_count"] >= 20:
                s.append(i["total_cede"])
        return min(s)

    avg.update({
        "highest_score": highest_score(matches),
        "highest_score_split_seasons": splitAcrossSeasons(highest_score, matches),
        "lowest_cede": lowest_cede(matches),
        "lowest_cede_split_seasons": splitAcrossSeasons(lowest_cede, matches)
    })

    # season statistics
    avg.update({
        "finals_qualified": 0,
        "semifinals_qualified": 0,
        "seasons_won": 0
    })

    for i in matches:
        if "Qualifier" in i["match_id"]:
            avg["semifinals_qualified"] += 1
        if ".Final." in i["match_id"]:
            avg["finals_qualified"] += 1
            if i["win"] == True:
                avg["seasons_won"] += 1

    return avg


def fetch_and_aggregate_team(team, db, start="2007/08", duration=1, end="2023"):
    yearList = matchingYears(start, duration, end, ignoreEndYear=True)
    teamQuery = """SELECT * FROM teamMatches WHERE team = '{0}' AND year IN {1};""".format(
        team, yearList)

    c = db.cursor()
    c.execute(teamQuery)

    output = c.fetchall()
    vals = []

    for i in output:
        if i:
            vals.append(i)
        else:
            print("ignored")

        
    if len(vals) == 0:
        return {}

    average = aggregate_team(allTeamMatchRecordToDictionary(vals))

    return average
