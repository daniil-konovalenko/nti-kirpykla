from GraphParser import graphParser
from ..Day_1.database import get_location
import random

def mk_test(k: int) -> list, list:
    file_no = open("ids_to_predist.txt", "r")
    cols = list()
    cols.append("from")
    cols.append("to")
    cols.append("links")
    (graph, fd) = graphParser.parseFolderBySchema("Task2\\Task2\\graph", 3000, "", "from", cols, True)
    se = list()
    for i, y in graph.items():
        se.append(i)
    list_index = [x for x in range(3000)]
    random.shuffle(list_index)
    list_index = list_index[:k]
    list_answers = [0]* k
    for i in range(k):
        list_answers[i] = get_location(list_index[i])
    return list_index, list_answers