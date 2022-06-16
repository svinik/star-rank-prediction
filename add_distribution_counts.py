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
    return client['StarRankDB']


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    db = get_database()
    pairs_collection = db['distribution-pairs']
    results_collection = db['results']

    counts = {}

    for document in pairs_collection.find():
        counts[str(document['_id'])] = 0

    for document in results_collection.find({"experiment_completed": True}):
        for decision in document['pages']['evaluation_page']['decisions_arr']:
            counts[decision['id']] = counts[decision['id']] + 1

    for document in pairs_collection.find():
        pairs_collection.update_one({'_id': document['_id']}, {'$set': {'count': counts[str(document['_id'])]}}, upsert=True)
