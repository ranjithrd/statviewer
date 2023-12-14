from src.aggregate.utils.utils import *
import src.aggregate.functions.batting as batting
import src.aggregate.functions.bowling as bowling
from src.aggregate.utils.split_seasons import generateDataPoints, splitAcrossSeasons
from src.data.load import allData


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

    # batting stats
    avg.update(generateDataPoints(batting.run_rate,
               matches, "batting_run_rate", ad))
    avg.update(generateDataPoints(batting.strike_rate,
               matches, "batting_strike_rate", ad))
    avg.update(generateDataPoints(
        batting.batting_average, matches, "batting_average", ad))

    # match statistics
    avg.update({
        "total_matches_played": len(matches),
        "total_matches_won": 0,
    })

    for i in matches:
        if i["win"]:
            avg["total_matches_won"] += 1

    avg.update({
        "percentage_matches_won": round(100 * (avg["total_matches_won"] / avg["total_matches_played"])),
    })

    return avg


def fetch_and_aggregate_custom_team(players, db, start="2007/08", duration=1, end="2023"):
    s = []
    for i in players:
        s.append("'" + i + "'")
    q = "(" + ",".join(s) + ")"

    yearList = matchingYears(start, duration, end, ignoreEndYear=True)
    playerQuery = """SELECT * FROM playermatches WHERE player in {0} AND year IN {1};""".format(
        q, yearList)

    c = db.cursor()
    c.execute(playerQuery)

    output = c.fetchall()
    vals = []

    for i in output:
        if i:
            vals.append(i)
        else:
            print("ignored")

    average = aggregate_custom_team(allPlayerMatchRecordToDictionary(vals))

    return average
