def run_rate(matches):
    r, o = 0, 0
    for i in matches:
        r += i["total_bat"]
        o += i["over_count"]

    if o == 0:
        return 0

    return round(r / o, 2)

def strike_rate(matches):
    r, b = 0, 0
    for i in matches:
        r += i["total_bat"]
        b += len(i["balls_bat"])

    if b == 0:
        return 0

    return round(100 * (r / b), 2)

def batting_average(matches):
    r, w = 0, 0
    for i in matches:
        # if sum(i["fall_of_wickets"]) < 1:
        #     continue
        r += i["total_bat"]
        w += sum(i["fall_of_wickets"])

    if w == 0:
        w = 1

    return round(r / w, 2)

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

def overs_batted(matches):
    o = 0
    for i in matches:
        o += len(i["overs_bat"])

    return o