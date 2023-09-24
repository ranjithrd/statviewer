from data import parseMatch
import json
import pathlib

def main():
    MATCH_DATE = "2008-04-29"

    files = pathlib.Path("latest_sample_data")

    for fileName in files.iterdir():

        if "json" not in fileName.__str__()[-7:]:
            continue

        fileData = open(fileName)
        contents = json.loads(fileData.read())

        # print(contents.deliveries)

        metadata, _, _ = parseMatch(contents)
        #print(metadata["date"])
        if metadata["date"] == MATCH_DATE:
            fileData.seek(0)
            print(fileData.read())

        fileData.close()
        



main()