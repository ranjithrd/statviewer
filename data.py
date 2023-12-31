from src.data.load import resetDatabase, dropTables, initializeDatabase, addValues, importJSON

def main():
    print("N O T E")
    print("MYSQL DATABASE MUST BE CONFIGURED TO THE BELOW FOR APP TO WORK.")
    print()
    print("user: root")
    print("password: mysql123")
    print("database: pyproj")
    print()
    print("DOWNLOAD IPL data from https://cricsheet.org and note its path.")
    print()
    print("DATABASE CANNOT LOAD WITHOUT THIS FOLDER ON YOUR SYSTEM.")
    print()
    print()
    print()
    print("Choose a function to run:")
    print("A\t Reset database and load from folder")
    print("B\t Clear all data and drop all tables")
    print("C\t Add values without clearing data")
    print("D\t Initialize database and add tables without adding data")

    print("\n")
    c = input("Choice: ").lower().strip()[0]

    if c == "a":
        folderPath = input("Enter path to DOWNLOADED CRICSHEET JSON DATA FOLDER: ")
        resetDatabase(folderPath.strip())
    
    if c == "b":
        dropTables()

    if c == "c":
        folderPath = input("Enter path to DOWNLOADED CRICSHEET JSON DATA FOLDER: ")
        importJSON(addValues(folderPath))

    if c == "d":
        initializeDatabase()

    print("\nEXITING.")
    print("Open the app or RUN gui.py to see statistics.")

if __name__ == "__main__":
    main()