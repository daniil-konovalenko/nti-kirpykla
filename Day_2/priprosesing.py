import pickle

def func(graph):
    big_table = list()
    for id, inform in graph.items():
        line = [0]*len(inform)
        for index, j in enumerate(inform):
            line[index] = [j, 1]
        big.table.append(line)
    return big_table

