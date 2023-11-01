import mysql.connector as mysql
import pathlib
import json

db = None  # type: mysql.MySQLConnection

TeamNames = {
    'Chennai Super Kings': 'CSK',
    'Rajasthan Royals': 'RR',
    'Mumbai Indians': 'MI',
    'Delhi Capitals': 'DC',
    'Delhi Daredevils': 'DC',
    'Kings XI Punjab': 'KXIP',
    'Kochi Tuskers Kerala': 'KTK',
    'Royal Challengers Bangalore': 'RCB',
    'Rising Pune Supergiants': 'RPS',
    'Kolkata Knight Riders': 'KKR',
    'Pune Warriors': 'RPS',
    'Deccan Chargers': 'SRH',
    'Sunrisers Hyderabad': 'SRH',
    'Punjab Kings': 'KXIP',
    'Gujarat Lions': 'GT',
    'Gujarat Titans': 'GT',
    'Lucknow Super Giants': 'LSG',
    'Rising Pune Supergiant': 'RPS'
}

CityNamesOverrides = {
    "Bengaluru": "Bangalore",
    "Dubai International Cricket Stadium": "Dubai",
    "Sharjah Cricket Stadium": "Sharjah"
}

def parseMatch(match):
    matchPlayers = match["info"]["players"]
    teams = list(matchPlayers.keys())

    identifier = ""
    if "stage" in match["info"]["event"]:
        identifier = match["info"]["event"]["stage"]
    elif "match_number" in match["info"]["event"]:
        identifier = str(match["info"]["event"]["match_number"])
    else:
        print("NO VALID ID FOR MATCH")

    winner = ""
    if "result" in match["info"]["outcome"] and match["info"]["outcome"]["result"] in "tie no result":
        winner = ""
    elif "winner" in match["info"]["outcome"]:
        winner = match["info"]["outcome"]["winner"]
    else:
        print("NO VALID WINNER")

    if "city" not in match["info"]:
        match["info"]["city"] = match["info"]["venue"]

    metadata = {
        "date": match["info"]["dates"][0],
        "year": str(match["info"]["season"]),
        "number": identifier,
        "winner": winner,
        "city": match["info"]["city"],
        "players": [],
        "teams": teams,
    }

    if metadata["city"] in CityNamesOverrides:
        metadata["city"] = CityNamesOverrides[metadata["city"]]

    metadata["match_id"] = str(metadata["year"]) + \
        "." + str(metadata["number"]) + "." + str(metadata["date"])

    PerformanceDefault = {
        "total_bat": 0,
        "total_cede": 0,
        "total_wickets": 0,

        "overs_bat": [],
        "overs_cede": [],
        "overs_wickets": [],

        "balls_bat": [],
        "balls_cede": [],
        "balls_wickets": [],

        "fall_of_wickets": [],

        "win": False,

        "over_count": 0
    }

    teamPerformance = {}
    playerPerformance = {}
    for i in matchPlayers:
        for j in matchPlayers[i]:
            if j not in metadata["players"]:
                metadata["players"].append(j)
            playerPerformance[j] = json.loads(json.dumps(PerformanceDefault))
            playerPerformance[j]["team"] = i
    for i in matchPlayers.keys():
        teamPerformance[i] = json.loads(json.dumps(PerformanceDefault))

    for inning in match["innings"]:
        battingTeam = inning["team"]
        bowlingTeam = teams[1] if teams[0] == battingTeam else teams[0]

        for over in inning["overs"]:
            overBatting = {}
            overCede = {}
            overWickets = {}

            overWicketsBatters = 0
            overWicketsPlayers = {}

            teamBat = 0
            teamCede = 0
            teamWickets = 0

            teamPerformance[battingTeam]["over_count"] += 1

            for delivery in over["deliveries"]:
                totalRuns = delivery["runs"]["total"]
                batterRuns = delivery["runs"]["batter"]

                batter = delivery["batter"]
                bowler = delivery["bowler"]

                if batter not in overBatting:
                    overBatting[batter] = 0
                if batter not in overWicketsPlayers:
                    overWicketsPlayers[batter] = 0
                if bowler not in overCede:
                    overCede[bowler] = 0
                if bowler not in overWickets:
                    overWickets[bowler] = 0

                # BATSMAN STATS
                teamPerformance[battingTeam]["total_bat"] += totalRuns
                teamPerformance[battingTeam]["balls_bat"].append(totalRuns)
                teamBat += totalRuns

                playerPerformance[batter]["total_bat"] += batterRuns
                playerPerformance[batter]["balls_bat"].append(batterRuns)
                overBatting[batter] += batterRuns

                # BOWLER STATS

                # Cede logged regardless of wickets
                teamPerformance[bowlingTeam]["total_cede"] += totalRuns
                teamPerformance[bowlingTeam]["balls_cede"].append(totalRuns)
                teamCede += totalRuns

                playerPerformance[bowler]["total_cede"] += totalRuns
                playerPerformance[bowler]["balls_cede"].append(totalRuns)
                overCede[bowler] += batterRuns

                # Wicket
                if "wickets" in delivery:
                    teamPerformance[bowlingTeam]["total_wickets"] += 1
                    teamPerformance[bowlingTeam]["balls_wickets"].append(1)
                    teamCede += totalRuns

                    playerPerformance[bowler]["total_wickets"] += 1
                    playerPerformance[bowler]["balls_wickets"].append(1)
                    overWickets[bowler] += 1

                    teamWickets += 1

                    overWicketsBatters += 1

                    player_out = delivery["wickets"][0]["player_out"]
                    if player_out not in overWicketsPlayers:
                        overWicketsPlayers[player_out] = 0
                    overWicketsPlayers[player_out] += 1
                else:
                    teamPerformance[bowlingTeam]["balls_wickets"].append(0)
                    playerPerformance[bowler]["balls_wickets"].append(0)

            for p in overBatting:
                playerPerformance[p]["overs_bat"].append(overBatting[p])

            for p in overCede:
                playerPerformance[p]["overs_cede"].append(overCede[p])

            for p in overWickets:
                playerPerformance[p]["overs_wickets"].append(overWickets[p])

            for p in overWicketsPlayers:
                playerPerformance[p]["fall_of_wickets"].append(
                    overWicketsPlayers[p])

            teamPerformance[battingTeam]["fall_of_wickets"].append(
                overWicketsBatters)
            teamPerformance[battingTeam]["overs_bat"].append(teamBat)
            teamPerformance[bowlingTeam]["overs_cede"].append(teamCede)
            teamPerformance[bowlingTeam]["overs_wickets"].append(teamWickets)

    if winner != "":
        teamPerformance[winner]["win"] = True
        for i in matchPlayers[winner]:
            playerPerformance[i]["win"] = True

    for i in playerPerformance:
        playerPerformance[i]["team"] = TeamNames[playerPerformance[i]["team"]]
        playerPerformance[i]["player"] = i
        playerPerformance[i]["year"] = metadata["year"]
        playerPerformance[i]["match_id"] = metadata["match_id"]
        p = playerPerformance[i]
        playerPerformance[i]["performance_id"] = p["team"] + \
            "." + p["player"] + "." + p["year"]
        playerPerformance[i]["player_match_id"] = metadata["match_id"] + "." + i

    for i in matchPlayers[battingTeam]:
        playerPerformance[i]["over_count"] = teamPerformance[battingTeam]["over_count"]

    # city
    for i in teamPerformance:
        teamPerformance[i]["toss_won"] = i == match["info"]["toss"]["winner"]

    namedTeamPerformances = {}
    for i in teamPerformance:
        namedTeamPerformances[TeamNames[i]] = teamPerformance[i]
        namedTeamPerformances[TeamNames[i]]["team"] = TeamNames[i]
        namedTeamPerformances[TeamNames[i]]["year"] = metadata["year"]
        namedTeamPerformances[TeamNames[i]]["match_id"] = metadata["match_id"]
        namedTeamPerformances[TeamNames[i]]["city"] = metadata["city"]
        namedTeamPerformances[TeamNames[i]
                              ]["team_match_id"] = metadata["match_id"] + "." + TeamNames[i]

    if metadata["winner"] != "":
        metadata["winner"] = TeamNames[metadata["winner"]]

    return (metadata, list(namedTeamPerformances.values()), list(playerPerformance.values()))


def importJSON(path):
    global db
    global TeamNames

    files = pathlib.Path(path)

    matchMetadata = []
    matchIds = []

    matchTeamPerformances = []
    matchPlayerPerformances = []

    for fileName in files.iterdir():
        if "json" not in fileName.__str__()[-7:]:
            continue

        fileData = open(fileName)
        contents = json.loads(fileData.read())
        fileData.close()

        metadata, fileTeamPerf, filePlayerPerf = parseMatch(contents)
        matchMetadata.append(metadata)
        matchIds.append(metadata["match_id"])
        matchTeamPerformances.extend(fileTeamPerf)
        matchPlayerPerformances.extend(filePlayerPerf)

    performancesDict = {}
    for i in matchPlayerPerformances:
        key = i["team"] + "." + i["player"] + "." + i["year"]
        if key not in performancesDict:
            performancesDict[key] = {
                "performance_id": key,
                "team": i["team"],
                "player": i["player"],
                "year": i["year"],
                "matches": [i["match_id"]]
            }
        else:
            performancesDict[key]["matches"].append(i["match_id"])
    performances = list(performancesDict.values())

    players = []
    years = []
    teams = []

    for i in matchMetadata:
        if i["year"] not in years:
            years.append(i["year"])

        for j in i["players"]:
            if j not in players:
                players.append(j)

        for j in i["teams"]:
            if TeamNames[j] not in teams:
                teams.append(TeamNames[j])

    # return (matchMetadata, matchTeamPerformances, matchPlayerPerformances, performances)
    return {
        "players": players,
        "years": years,
        "teams": teams,
        "metadata": matchMetadata,
        "teamMatches": matchTeamPerformances,
        "playerMatches": matchPlayerPerformances,
        "performances": performances
    }