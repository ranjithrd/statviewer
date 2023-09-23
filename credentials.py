import mysql.connector as mysql

def defaultDatabase() -> mysql.MySQLConnection:
    return mysql.connect(host="localhost", user="root", password="mysql123", database="pyproj")
    pass

