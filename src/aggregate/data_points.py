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
    "highest_wickets_split_seasons": ["bowling", True, "single", "highest_wickets"],
    # Average match statistics
    "wickets_as_of_ball": ["bowling", True, "single", "ind"],
    "bat_as_of_ball": ["bowling", True, "single", "ind"],
    "cede_as_of_ball": ["bowling", True, "single", "ind"],
}

generatedSplitPoints = {
    # Batting statistics
    "batting_strike_rate": ["batting", True, "single", "ind"],
    "batting_economy": ["batting", True, "single", "ind"],
    "batting_average": ["batting", True, "single", "ind"],
    "batting_runs_scored": ["batting", True, "single", "ind"],
    "batting_overs_batted": ["batting", True, "single", "ind"],

    # Bowling statistics
    "bowling_strike_rate": ["bowling", True, "single", "ind"],
    "bowling_economy": ["bowling", True, "single", "ind"],
    "bowling_average": ["bowling", True, "single", "ind"],
    "bowling_wickets_taken": ["bowling", True, "single", "ind"],
    "bowling_overs_balled": ["bowling", True, "single", "ind"],
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

# print(json.dumps(dataPoints))

def dataPointsWhere(dp, index, isValue):
    a = []
    for i in dp:
        if dp[i][index] == isValue:
            a.append(i)

    return a