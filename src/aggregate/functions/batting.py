def run_rate(matches):
    r, o = 0, 0
    for i in matches:
        r += i["total_bat"]
        o += i["over_count"]

    return r / o

def strike_rate(matches):
    r, b = 0, 0
    for i in matches:
        r += i["total_bat"]
        b += len(i["balls_bat"])

    return 100 * (r / b)

def batting_average(matches):
    r, w = 0, 0
    for i in matches:
        r += i["total_bat"]
        w += sum(i["fall_of_wickets"])

    return r / w

def half_centuries(matches):
    h = 0
    for i in matches:
        if i["total_bat"] >= 50:
            h += 1

    return h

def centuries(matches):
    h = 0
    for i in matches:
        if i["total_bat"] >= 100:
            h += 1

    return h

def duck_outs(matches):
    h = 0
    for i in matches:
        if i["total_bat"] == 0 and sum(i["fall_of_wickets"]) > 0:
            h += 1

    return h

def runs_scored(matches):
    r = 0
    for i in matches:
        r += i["total_bat"]

    return r