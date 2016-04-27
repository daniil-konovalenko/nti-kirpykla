import os.path
from Day_1.database import user_data, get_csv_filenames, demography_to_db

demography_base_folder = os.path.join("..", "Task2", "Task2", "trainDemography")
csv_filenames = get_csv_filenames(demography_base_folder)

print("Extracting data from files: \n {}".format("\n".join(csv_filenames)))

for csv_file in csv_filenames:
    print("Opening demography file {}".format(csv_file))
    demography_to_db(user_data, csv_file)
