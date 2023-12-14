# import mysql.connector as mysql
import sqlite3

db = None

# SQLITE3 CODE
def defaultDatabase() -> sqlite3.Connection:
    return sqlite3.connect("database.db")

# MYSQL CODE
# def defaultDatabase() -> mysql.MySQLConnection:
#     return mysql.connect(host="localhost", user="root", password="mysql123", database="pyproj")
