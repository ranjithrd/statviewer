import json

# FORMAT
# [BATTING/BOWLING/COMMON, IS_SHOWN_CURRENTLY, SINGLE DATAPOINT/SPLIT/PERCENTILE/PERCENTILE SPLIT, INDEPENDENT/DEPENDENT ON OTHER DATAPOINT]

dataPoints = {
    # Team statistics
    "total_matches_played": ["common", True, "single", "ind"],
    "total_matches_won": ["common", True, "single", "ind"],
    "percentage_matches_won": ["common", True, "single", "ind"],
    "percentage_matches_won_split_seasons": ["common", True, "split_season", "percentage_matches_won"],
    # Record statistics
    "highest_score": ["batting", True, "single", "ind"],
    "highest_score_split_seasons": ["batting", True, "split_seasons", "highest_score"],
    "highest_wickets": ["bowling", True, "single", "ind"],
    "highest_wickets_split_seasons": ["bowling", True, "split_seasons", "highest_wickets"],
    # Average match statistics
    "wickets_as_of_ball": ["bowling", True, "line", "ind"],
    "bat_as_of_ball": ["bowling", True, "line", "ind"],
    "cede_as_of_ball": ["bowling", True, "line", "ind"],
}

generatedSplitPoints = {
    # Batting statistics
    "batting_run_rate": ["batting", True, "single", "ind"],
    "batting_strike_rate": ["batting", True, "single", "ind"],
    "batting_average": ["batting", True, "single", "ind"],
    "batting_runs_scored": ["batting", True, "single", "ind"],
    "batting_overs_batted": ["batting", True, "single", "ind"],

    # Bowling statistics
    "bowling_strike_rate": ["bowling", True, "single", "ind"],
    "bowling_economy": ["bowling", True, "single", "ind"],
    "bowling_average": ["bowling", True, "single", "ind"],
    "bowling_wickets_taken": ["bowling", True, "single", "ind"],
    "bowling_overs_bowled": ["bowling", True, "single", "ind"],
}

generatedNonSplitPoints = {
    # Batting statistics
    "batting_half_centuries": ["batting", True, "single", "ind"],
    "batting_centuries": ["batting", True, "single", "ind"],
    "batting_duck_outs": ["batting", True, "single", "ind"],

    # Bowling statistics
    "bowling_five_wicket_hauls": ["bowling", True, "single", "ind"]
}

for i in generatedSplitPoints:
    gi_type, gi_shown, _, _ = generatedSplitPoints[i]
    dataPoints[i] = generatedSplitPoints[i]
    dataPoints[i + "_split_seasons"] = [gi_type, gi_shown, "split_seasons", i]
    dataPoints[i + "_percentile"] = [gi_type, gi_shown, "percentile", i]
    dataPoints[i + "_percentile_split_seasons"] = [gi_type, gi_shown, "percentile_split_seasons", i]

for i in generatedNonSplitPoints:
    gi_type, gi_shown, _, _ = generatedNonSplitPoints[i]
    dataPoints[i] = generatedNonSplitPoints[i]
    dataPoints[i + "_percentile"] = [gi_type, gi_shown, "percentile", i]

for i in dataPoints:
    if dataPoints[i][3] == "ind":
        dataPoints[i][3] = i

def dataPointsWhere(dp, index, isValue):
    a = []
    for i in dp:
        if dp[i][index] == isValue:
            a.append(i)

    return a

teamDataPoints = dict(dataPoints)

deleted = ["bowling_five_wicket_hauls", "batting_half_centuries", "batting_centuries", "batting_duck_outs", "highest_wickets", "batting_overs_batted", "bowling_overs_bowled"]
k = list(teamDataPoints.keys())
for i in k:
    for j in deleted:
        if j in i:
            if i in teamDataPoints:
                del teamDataPoints[i]

for i in ["percentage_matches_won_toss_won", "percentage_matches_won_toss_lost", "lowest_cede"]:
    gi_type, gi_shown, _, _ = "common", True, 0, 0
    teamDataPoints[i] = ["common", True, "single", "ind"]
    teamDataPoints[i + "_split_seasons"] = [gi_type, gi_shown, "split_seasons", i]

teamDataPoints.update({
    # Match statistics
    "percentage_matches_won_city": ["common", True, "bar", "ind"],
    # Season Statistics
    "finals_qualified": ["common", True, "single", "ind"],
    "semifinals_qualified": ["common", True, "single", "ind"],
    "seasons_won": ["common", True, "single", "ind"]
})

for i in teamDataPoints:
    if teamDataPoints[i][3] == "ind":
        teamDataPoints[i][3] = i



customTeamDataPoints = {
    "percentage_matches_won": ["common", True, "single", "percentage_matches_won"]
}

for i in ["bowling_strike_rate", "bowling_economy", "bowling_average"]:
    customTeamDataPoints[i] = ["bowling", True, "single", i]
    customTeamDataPoints[i + "_percentile"] = ["bowling", True, "percentile", i]

for i in ["batting_run_rate", "batting_strike_rate", "batting_average"]:
    customTeamDataPoints[i] = ["batting", True, "single", i]
    customTeamDataPoints[i + "_percentile"] = ["batting", True, "percentile", i]
