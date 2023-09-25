from aggregate.team import fetch_and_aggregate_team
from data.load import resetDatabase
from data.credentials import defaultDatabase


def main():
    # TEST RESET DB
    # resetDatabase("latest_sample_data")

    # TEST AGGREGATE
    db = defaultDatabase()
    avg = fetch_and_aggregate_team("RCB", db, duration=7)
    print(avg)

main()