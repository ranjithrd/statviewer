# from ..src.data import parseMatch
import json
import pathlib

def main():
    MATCH_DATE = "2008-04-29"

    years = []

    files = pathlib.Path("/Users/ranjithrd/Documents/statviewer/odis_male_json")

    c = 0


    for fileName in files.iterdir():

        if "json" not in fileName.__str__()[-7:]:
            continue

        fileData = open(fileName)
        contents = json.loads(fileData.read())

        season = contents["info"]["dates"][0][:4]
        if season not in years:
            years.append(season)

        # print(contents.deliveries)

        # metadata, _, _ = parseMatch(contents)
        # #print(metadata["date"])
        # if metadata["date"] == MATCH_DATE:
        #     fileData.seek(0)
        #     print(fileData.read())

        # fileData.close()
            
        if "event" in contents["info"] and "match_type_number" not in contents["info"]["event"]:
            c += 1
            print(season)

        fileData.close()

    # print(sorted(years))

    print("C IS ", c)
    # print(len(files.))

    d1, d2 = {}, {}
    c = 0
    while c < 22:
        d1[c + 1] = str(2002 + c)
        d2[c + 1] = 2002 + c
        c += 1

    print(json.dumps(d1))
    print(json.dumps(d2))

    print(json.dumps({
        "order": d1,
        "split_seasons_convert_to": d2
    }))

main()