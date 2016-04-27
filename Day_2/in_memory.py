import pickle
import os.path


pickled_graph = pickle.load(open(os.path.join('..', 'res', 'graph.pkl'), 'rb'))
pickled_demography = pickle.load(open(os.path.join('..', 'res', 'locs_.pkl'), 'rb'))

def get_friends(user_id):
    return pickled_graph.get(user_id, [])

def get_location(user_id):
    return pickled_demography.get(user_id, 0)
