from pymongo import MongoClient


client = MongoClient('localhost', 27017)

db = client.odnoklassniki

def get_age(user_id):
    return db.user_data.findOne({"id": user_id})["age"]



