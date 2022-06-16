import bson
import pandas as pd
from bson.objectid import ObjectId

def get_database():
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://star:Qwerty123456@starrankcluster.eotzt.mongodb.net"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['Prod']


def distribution_record(row):
    first = {
        "star5": int(row['5a']),
        "star4": int(row['4a']),
        "star3": int(row['3a']),
        "star2": int(row['2a']),
        "star1": int(row['1a']),
        "name": "",
        "url": ""
    }

    second = {
        "star5": int(row['5b']),
        "star4": int(row['4b']),
        "star3": int(row['3b']),
        "star2": int(row['2b']),
        "star1": int(row['1b']),
        "name": "",
        "url": ""
    }

    return {
        "_id": ObjectId(),
        "first": first,
        "second": second,
        "category": "",
        "site": "",
        "type": ""
    }


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    df = pd.read_csv('output_file_describe_figures (3).csv')

    # Get the database
    db = get_database()
    collection = db['distribution-pairs']

    for index, row in df.iterrows():
        record = distribution_record(row)
        collection.insert_one(record)
