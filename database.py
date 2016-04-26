from pymongo import MongoClient


client = MongoClient('localhost', 27017)

db = client.odnoklassniki

def get_age(user_id):
    return db.user_data.findOne({"id": user_id})["age"]


def get_friends(user_id):
    result = db.user_friends.findOne({"id": user_id})
    if result:
        return result
    else:
        return None
    