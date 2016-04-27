import os
from Day_1.database import graph_to_db, user_friends, get_csv_filenames


graph_base_folder = os.path.join("..", "Task2", "Task2", "graph")

csv_filenames = get_csv_filenames(graph_base_folder)
print("Extracting data from files: \n {}".format("\n".join(csv_filenames)))

for csv_file in csv_filenames:
    print("Opening file {}".format(csv_file))
    graph_to_db(user_friends, csv_file)

