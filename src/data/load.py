import json
import mysql.connector as mysql
from data.parse import importJSON
from data.credentials import defaultDatabase
from aggregate.utils.utils import allTeamMatchRecordToDictionary, allPlayerMatchRecordToDictionary

allTeamMatches = []
allPlayerMatches = []


def initializeDatabase():
    db = defaultDatabase()
    cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        match_id VARCHAR(50) PRIMARY KEY,
        date DATE,
        year VARCHAR(10),
        number VARCHAR(20),
        winner VARCHAR(25)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS performances (
        performance_id VARCHAR(50) PRIMARY KEY,
        team VARCHAR(25),
        year VARCHAR(25),
        player VARCHAR(45)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teamMatches(
        team_match_id VARCHAR(50) PRIMARY KEY,
        match_id VARCHAR(50) REFERENCES matches(match_id),
        year VARCHAR(25),
        team VARCHAR(25),
        win BOOLEAN,
        total_bat INTEGER,
        total_cede INTEGER,
        total_wickets INTEGER,
        overs_bat LONGTEXT,
        overs_cede LONGTEXT,
        overs_wickets LONGTEXT,
        balls_bat LONGTEXT,
        balls_cede LONGTEXT,
        balls_wickets LONGTEXT,
        fall_of_wickets LONGTEXT,
        over_count INTEGER,
        city VARCHAR(50),
        toss_won BOOLEAN
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS playerMatches(
        player_match_id VARCHAR(100) PRIMARY KEY,
        match_id VARCHAR(50) REFERENCES matches(match_id),
        performance_id VARCHAR(50) REFERENCES performances(performance_id),
        year VARCHAR(25),
        player VARCHAR(45),
        team VARCHAR(25),
        win BOOLEAN,
        total_bat INTEGER,
        total_cede INTEGER,
        total_wickets INTEGER,
        overs_bat LONGTEXT,
        overs_cede LONGTEXT,
        overs_wickets LONGTEXT,
        balls_bat LONGTEXT,
        balls_cede LONGTEXT,
        balls_wickets LONGTEXT,
        fall_of_wickets LONGTEXT,
        over_count INTEGER
    );
    ''')


def addValues(folderOutput):
    db = defaultDatabase()

    cursor = db.cursor()

    existingMetadataCursor = db.cursor()
    existingMetadataCursor.execute("SELECT match_id FROM matches;")
    existingMetadataValues = list(existingMetadataCursor.fetchall())
    for i in folderOutput["metadata"]:
        # print((i,) in existingMetadataValues)
        print(i["match_id"])
        cursor.execute("""INSERT INTO matches VALUES ('{}', '{}', '{}', '{}', '{}');""".format(
            i["match_id"], i["date"], i["year"], i["number"], i["winner"]))

    for i in folderOutput["teamMatches"]:
        # print(i)
        cursor.execute("""INSERT INTO teamMatches VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {})"""
                       .format(
                           i["team_match_id"],
                           i["match_id"],
                           i["year"],
                           i["team"],
                           1 if i["win"] else 0,
                           i["total_bat"],
                           i["total_cede"],
                           i["total_wickets"],
                           json.dumps(i["overs_bat"]),
                           json.dumps(i["overs_cede"]),
                           json.dumps(i["overs_wickets"]),
                           json.dumps(i["balls_bat"]),
                           json.dumps(i["balls_cede"]),
                           json.dumps(i["balls_wickets"]),
                           json.dumps(i["fall_of_wickets"]),
                           i["over_count"],
                           i["city"],
                           1 if i["toss_won"] else 0
                       ))

    for i in folderOutput["playerMatches"]:
        # print(i)
        cursor.execute("""INSERT INTO playerMatches VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
                       .format(
                           i["player_match_id"],
                           i["match_id"],
                           i["performance_id"],
                           i["year"],
                           i["player"],
                           i["team"],
                           1 if i["win"] else 0,
                           i["total_bat"],
                           i["total_cede"],
                           i["total_wickets"],
                           json.dumps(i["overs_bat"]),
                           json.dumps(i["overs_cede"]),
                           json.dumps(i["overs_wickets"]),
                           json.dumps(i["balls_bat"]),
                           json.dumps(i["balls_cede"]),
                           json.dumps(i["balls_wickets"]),
                           json.dumps(i["fall_of_wickets"]),
                           i["over_count"]
                       ))

    for i in folderOutput["performances"]:
        # print(i)
        cursor.execute("""INSERT INTO performances VALUES('{}', '{}', '{}', '{}')""".format(
            i["performance_id"], i["team"], i["year"], i["player"]))

    db.commit()

    print("Added values for", folderOutput)


def clearValues():
    db = defaultDatabase()
    cursor = db.cursor()

    cursor.execute("DELETE FROM playerMatches;")
    cursor.execute("DELETE FROM teamMatches;")
    cursor.execute("DELETE FROM performances;")
    cursor.execute("DELETE FROM matches;")

    db.commit()

    print("Deleted all values")


def dropTables():
    db = defaultDatabase()
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS playerMatches;")
    cursor.execute("DROP TABLE IF EXISTS teamMatches;")
    cursor.execute("DROP TABLE IF EXISTS performances;")
    cursor.execute("DROP TABLE IF EXISTS matches;")


def resetDatabase(p):
    dropTables()
    initializeDatabase()

    clearValues()
    addValues(importJSON(p))


def allData():
    global allTeamMatches

    if len(allTeamMatches) < 10:
        db = defaultDatabase()
        c = db.cursor()
        c.execute("SELECT * FROM teamMatches;")
        allTeamMatches = allTeamMatchRecordToDictionary(c.fetchall())
        db.close()

    return allTeamMatches


def allPlayers():
    global allPlayerMatches

    if len(allPlayerMatches) < 10:
        db = defaultDatabase()
        c = db.cursor()
        c.execute("SELECT * FROM playerMatches;")
        allPlayerMatches = allPlayerMatchRecordToDictionary(c.fetchall())
        db.close()

    return allPlayerMatches