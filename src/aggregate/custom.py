import mysql.connector as mysql
from aggregate.utils.utils import *
import aggregate.functions.batting as batting
import aggregate.functions.bowling as bowling
import aggregate.utils.percentile as percentile
from aggregate.utils.split_seasons import generateDataPoints, splitAcrossSeasons
from data.load import allData

def aggregate_custom_team(matches):
    print(len(matches))
    avg = {}

    ad = groupByTeams(allData()).values()

    # bowling stats
    avg.update(generateDataPoints(bowling.strike_rate,
               matches, "bowling_strike_rate", ad))
    avg.update(generateDataPoints(
        bowling.economy, matches, "bowling_economy", ad))
    avg.update(generateDataPoints(
        bowling.average, matches, "bowling_average", ad))
    # avg.update(generateDataPoints(bowling.runs_conceded,
    #            matches, "bowling_runs_conceded", ad))
    # avg.update(generateDataPoints(bowling.wickets_taken,
    #            matches, "bowling_wickets_taken", ad))
    # avg.update(generateDataPoints(bowling.overs_balled,
    #            matches, "bowling_overs_balled", ad))
    # avg.update(generateDataPoints(bowling.five_wicket_hauls,
    #            matches, "bowling_five_wicket_hauls", ad))

    # batting stats
    avg.update(generateDataPoints(batting.run_rate,
               matches, "batting_run_rate", ad))
    avg.update(generateDataPoints(batting.strike_rate,
               matches, "batting_strike_rate", ad))
    avg.update(generateDataPoints(
        batting.batting_average, matches, "batting_average", ad))
    # avg.update(generateDataPoints(batting.half_centuries,
    #            matches, "batting_half_centuries", ad))
    # avg.update(generateDataPoints(batting.centuries,
    #            matches, "batting_centuries", ad))
    # avg.update(generateDataPoints(batting.duck_outs,
    #            matches, "batting_duck_outs", ad))
    # avg.update(generateDataPoints(batting.runs_scored,
    #            matches, "batting_runs_scored", ad))
    # avg.update(generateDataPoints(batting.overs_batted,
    #            matches, "batting_overs_batted", ad))
    
    # match statistics
    avg.update({
        "total_matches_played": len(matches),
        "total_matches_won": 0,
        # "percentage_matches_won_city": {},
        # "matches_played_city": {}
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
    # def highest_score(m):
    #     s = []
    #     for i in m:
    #         s.append(i["total_bat"])
    #     return max(s)

    # def highest_wickets(m):
    #     s = []
    #     for i in m:
    #         s.append(i["total_wickets"])
    #     return max(s)

    # avg.update({
    #     "highest_score": highest_score(matches),
    #     "highest_score_split_seasons": splitAcrossSeasons(highest_score, matches),
    #     "highest_wickets": highest_wickets(matches),
    #     "highest_wickets_split_seasons": splitAcrossSeasons(highest_wickets, matches)
    # })

    return avg


def fetch_and_aggregate_custom_team(players, db, start="2007/08", duration=1, end="2023"):
    s = []
    for i in players:
        s.append("'" + i + "'")
    q = "(" + ",".join(s) + ")"

    yearList = matchingYears(start, duration, end, ignoreEndYear=True)
    playerQuery = """SELECT * FROM playermatches WHERE player in {0} AND year IN {1};""".format(
        q, yearList)

    print(playerQuery)

    c = db.cursor()
    c.execute(playerQuery)

    output = c.fetchall()
    vals = []
    # print(sorted(output, reverse=True))

    print(output)

    for i in output:
        # print(bool(i))
        if i:
            vals.append(i)
        else:
            print("ignored", i)

    average = aggregate_custom_team(allPlayerMatchRecordToDictionary(vals))

    return average
