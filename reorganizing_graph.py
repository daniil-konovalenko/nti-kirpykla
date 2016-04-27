import numpy as np
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['odnoklassniki']
total_friends = set()
for user in db.user_friends.find():
    total_friends.add(user['id'])
    total_friends.add(map(friend[0] for friend in user['friends']))

