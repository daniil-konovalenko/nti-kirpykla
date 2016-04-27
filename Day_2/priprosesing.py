import pickle
graph = pickle.load(open("graph_.pkl", "rb"))
demog = pickle.load(open("demog.pkl", "rb"))

def func(graph):
    big_table = list()
    se = set()
    for id, inform in graph.items():
        line = [0]*len(inform)
        for index, j in enumerate(inform):
            se.add(demog[j])
            line[index] = [demog[j], 1]
        big_table.append(line)
    return big_table,len(se)

