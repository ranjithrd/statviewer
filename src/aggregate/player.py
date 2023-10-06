import mysql.connector as mysql
from aggregate.utils.utils import *
import aggregate.functions.batting as batting
import aggregate.functions.bowling as bowling
import aggregate.utils.percentile as percentile
from aggregate.utils.split_seasons import generateDataPoints, splitAcrossSeasons
from data.load import allPlayers

def aggregate_player(matches):
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
        "wickets_as_of_ball": [0]
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

    ad = groupByPlayer(allPlayers()).values()

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
    avg.update(generateDataPoints(bowling.overs_balled,
               matches, "bowling_overs_balled", ad))
    avg.update(generateDataPoints(bowling.five_wicket_hauls,
               matches, "bowling_five_wicket_hauls", ad))

    # batting stats
    avg.update(generateDataPoints(batting.run_rate,
               matches, "batting_run_rate", ad))
    avg.update(generateDataPoints(batting.strike_rate,
               matches, "batting_strike_rate", ad))
    avg.update(generateDataPoints(
        batting.batting_average, matches, "batting_average", ad))
    avg.update(generateDataPoints(batting.half_centuries,
               matches, "batting_half_centuries", ad))
    avg.update(generateDataPoints(batting.centuries,
               matches, "batting_centuries", ad))
    avg.update(generateDataPoints(batting.duck_outs,
               matches, "batting_duck_outs", ad))
    avg.update(generateDataPoints(batting.runs_scored,
               matches, "batting_runs_scored", ad))
    avg.update(generateDataPoints(batting.overs_batted,
               matches, "batting_overs_batted", ad))
    
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
        
    for i in matches:
        if i["win"]:
            avg["total_matches_won"] += 1

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

    def highest_wickets(m):
        s = []
        for i in m:
            s.append(i["total_wickets"])
        return max(s)

    avg.update({
        "highest_score": highest_score(matches),
        "highest_score_split_seasons": splitAcrossSeasons(highest_score, matches),
        "highest_wickets": highest_wickets(matches),
        "highest_wickets_split_seasons": splitAcrossSeasons(highest_wickets, matches)
    })

    return avg


def fetch_and_aggregate_player(player, db, start="2007/08", duration=1, end="2023"):
    yearList = matchingYears(start, duration, end, ignoreEndYear=True)
    playerQuery = """SELECT * FROM playermatches WHERE player = '{0}' AND year IN {1};""".format(
        player, yearList)

    c = db.cursor()
    c.execute(playerQuery)

    output = c.fetchall()
    vals = []
    # print(sorted(output, reverse=True))

    for i in output:
        # print(bool(i))
        if i:
            vals.append(i)
        else:
            print("ignored", i)

    average = aggregate_player(allPlayerMatchRecordToDictionary(vals))

    return average
