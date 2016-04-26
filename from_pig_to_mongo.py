import pymongo
import os
from ast import literal_eval


batch_size = 1000

graph_base_folder = os.path.join("Task1", "Task1", "graph")
graph_folder_path = os.path.join("Task1", "Task1", "graph")
graph_prefix = "part-v006-o000-r-"


client = pymongo.MongoClient("localhost", 27017)
db = client.odnoklassniki
user_collection = db.user_friends

start = 0
end = 16

for i in range(start, end):

    graph_filename = graph_prefix + str(i).rjust(5, "0")


    graph_path = os.path.join(graph_base_folder, graph_filename)

    print("Opening graph_file {}".format(graph_path))


    graph_file = open(graph_path, 'r')
    users = []

    for line in graph_file:
        user_id, friends_string = line.strip().split('\t')
        user_id = int(user_id)
        friends_set = literal_eval(friends_string)
        friend_list = sorted(list(friends_set))
        user = {"id": user_id, "friends": friend_list}
        user_collection.insert(user)
