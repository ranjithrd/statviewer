from src.data.credentials import defaultDatabase

db = defaultDatabase()

def dbPlayers():
    c = db.cursor()
    c.execute("SELECT * FROM players;")
    r = []
    for i in c.fetchall():
        r.append(i[0])

    return r

def dbTeams():
    c = db.cursor()
    c.execute("SELECT * FROM teams;")
    r = []
    for i in c.fetchall():
        r.append(i[0])

    return r