from src.test_gui import main

main()

# import json
# from src.aggregate.team import fetch_and_aggregate_team
# from src.aggregate.player import fetch_and_aggregate_player
# from src.aggregate.custom import fetch_and_aggregate_custom_team
# from src.data.load import resetDatabase
# from src.data.credentials import defaultDatabase


# def main():
#     # TEST RESET DB
#     # resetDatabase("latest_sample_data")

#     # TEST AGGREGATE
#     db = defaultDatabase()
#     # avg = fetch_and_aggregate_team("RCB", db, end="2023")
#     # avg = fetch_and_aggregate_player("MA Wood", db, end="2023")
#     avg = fetch_and_aggregate_custom_team(["MA Wood", "V Kohli", "Mohammed Siraj"], db, end="2023")
#     # print(json.dumps(avg, indent=2))
#     json.dump(avg, open("sample_data/testpy.json", "w"))


# main()