from GraphParser import graphParser
from Day_2.in_memory import get_location, get_friends
import random
import numpy as np
from Day_2.metrics import k_nearest
import os



def mk_test(k: int, folder_path) -> (list, list):
    cols = list()
    cols.append("from")
    cols.append("to")
    cols.append("links")

    (graph, fd) = graphParser.parseFolderBySchema(folder_path, 3000, "", "from", cols, True)
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


def get_prediction_by_nearest(ids: np.ndarray, k: int) -> np.ndarray:
    result = np.zeros((len(ids), ))
    for i in range(len(ids)):
        print("Processing user #{} from {}".format(i, len(ids)))
        friends = get_friends(ids[i])
        result[i] = k_nearest(ids[i], friends, k)
    return np.array(result)


if __name__ == '__main__':
    folder_path = os.path.join('Task2', 'Task2', 'graph')
    indices, answers = mk_test(1000, )
    answers = np.array(answers)
    predicted = get_prediction_by_nearest(indices, 5)
    result = np.array([1 if answers[i] == predicted[i] else 0 for i in range(len(indices))])
    print(result.sum() / len(result))

