# balls is list of all balls played

def strikeRate(matches):
    balls = []
    for i in matches:
        balls += i["balls_bat"]

    return sum(balls) / len(balls)

def economy(matches):
    balls = []
    for i in matches:
        balls += i["balls_bat"]
        
    return 6 * sum(balls) / len(balls)

def average(matches):
    balls = []
    fall_of_wickets = []
    for i in matches:
        balls += i["balls_bat"]
        fall_of_wickets += i["fall_of_wickets"]
        
    return sum(balls) / len(fall_of_wickets)

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

def five_wicket_hauls(matches):
    c = 0
    for i in matches:
        if i["total_wickets"] >= 5:
            c += 1

    return c