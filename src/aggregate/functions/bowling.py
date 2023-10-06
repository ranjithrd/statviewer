import math

def strike_rate(matches):
    balls = []
    wickets = 0
    for i in matches:
        balls += i["balls_cede"]
        wickets += i["total_wickets"]

    if wickets == 0:
        wickets = 1

    return round(len(balls) / wickets, 2)

def economy(matches):
    balls = []
    for i in matches:
        balls += i["balls_cede"]
        
    if len(balls) == 0:
        return 0

    return round(6 * (sum(balls) / len(balls)), 2)

def average(matches):
    balls = 0
    fall_of_wickets = 0
    for i in matches:
        balls += i["total_cede"]
        fall_of_wickets += i["total_wickets"]

    if fall_of_wickets == 0:
        fall_of_wickets = 1
        
    return round(balls / fall_of_wickets, 2)

def runs_conceded(matches):
    r = 0
    for i in matches:
        r += i["total_cede"]

    return r

def wickets_taken(matches):
    w = 0
    for i in matches:
        w += i["total_wickets"]

    return w

def overs_balled(matches):
    overs = []
    for i in matches:
        overs += i["overs_cede"]
        
    return len(overs)


def five_wicket_hauls(matches):
    c = 0
    for i in matches:
        if i["total_wickets"] >= 5:
            c += 1

    return c