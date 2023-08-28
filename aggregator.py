import mysql.connector as mysql
from data import connectToDatabase, db, importJSON
import json
from credentials import defaultDatabase

def aggregate(connection):
    db = defaultDatabase()
    cursor = db.cursor()