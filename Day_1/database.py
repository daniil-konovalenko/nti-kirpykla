from pymongo import MongoClient
from ast import literal_eval
import os

client = MongoClient('localhost', 27017)

db = client.odnoklassniki_day2

user_friends = db.user_friends
user_data = db.user_data


def get_age(user_id):
    return db.user_data.find_one({"_id": user_id})["birth_date"]


def get_location(user_id):
    result = db.user_data.find_one({"_id": user_id})
    if result:
        return result["location_id"]
    else:
        return None


def get_friends(user_id):
    result = db.user_friends.find_one({"_id": user_id})
    if result:
        return result['friends']
    else:
        return []

def get_csv_filenames(base_folder):
    csv_filenames = []

    for root, dirs, filenames in os.walk(base_folder):
        csv_filenames.extend([os.path.join(root, filename)
                              for filename in filenames if filename.startswith("part")])
    return csv_filenames

def graph_to_db(collection, filename):
    with open(filename) as file:
        counter = 0
        for line in file:
            user_id, friends_string = line.strip().split('\t')
            user_id = int(user_id)
            friends_set = literal_eval(friends_string)
            friend_list = sorted(list(friends_set))
            user = {"_id": user_id, "friends": friend_list}
            collection.insert(user)
            counter += 1
            if counter % 1000 == 0:
                print("Inserted {} users".format(counter))


def demography_to_db(collection, filename):
    with open(filename) as file:
        counter = 0
        for line in file:
            (user_id,
             create_date,
             birth_date,
             gender,
             country_id,
             location_id,
             login_region,
             is_core) = line.strip().split('\t')

            user_id, location_id = map(int, (user_id, location_id))

            user = {'_id': user_id,
                    'location_id': location_id}

            collection.insert(user)
            counter += 1
            if counter % 1000 == 0:
                print("Inserted {} users".format(counter))

