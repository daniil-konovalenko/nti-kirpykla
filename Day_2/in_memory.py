import pickle
import os.path


pickled_graph = pickle.load(os.path.join('res', 'graph.pkl'))
pickled_demography = pickle.load(os.path.join('res', 'demog.pkl'))

def get_friends(user_id):
    return pickled_graph.get(user_id, [])

def get_location(user_id):
    return pickled_demography.get(user_id)
