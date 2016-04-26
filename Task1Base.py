import os
import random
import sys
from functools import partial

import matplotlib.pyplot as plt
import numpy as np
from relations import is_relevant, is_probably_same_age
from sklearn.linear_model import LinearRegression


def visualisation(data: np.ndarray, a, b):
    x_line = [random.randint(0, 100) for x in range(10)]
    y_line = [a * x_line[i] + b for i in range(10)]
    plt.plot(y_line, x_line)
    plt.scatter(data[:, 0], data[:, 1])
    plt.show()


def common_friends(userId_1: int, user_2: list, graph: dict) -> float:
    neighborhood_1 = set(graph[userId_1])
    neighborhood_2 = set(graph[user_2[0]])
    c_friends = list(neighborhood_1 & neighborhood_2)
    return len(c_friends)


def jaccard_coefficient(userId_1: int, user_2: list, graph: dict) -> float:
    neighborhood_1 = set(graph[userId_1])
    neighborhood_2 = set(graph[user_2[0]])
    c_friends = neighborhood_1 & neighborhood_2
    all_friends = neighborhood_1 | neighborhood_2
    return len(c_friends) / len(all_friends)


def jaccard_from_kailiak(userId_1: int, user_2: list, graph: dict) -> float:
    # user1 is user for which we make a prediction
    neighborhood_1 = set(graph[userId_1])
    neighborhood_2 = set(graph[user_2[0]])
    c_friends = neighborhood_1 & neighborhood_2
    return len(c_friends) / len(neighborhood_1)





def prediction_function(demog, graph):
    results = np.empty((0, 2))
    for userId, neighborhood in graph.items():
        try:
            if demog[userId] != None:
                continue
        except:
            print('Age for user {} have to be predicted'.format(userId))
        neighborhood = np.array(list(filter(is_relevant, neighborhood)))
        jaccard_score = np.array([jaccard_coefficient(userId, user, graph) for user in neighborhood])
        probaility_score = np.array(list(map(is_probably_same_age, neighborhood)))
        ages = np.array(list(map(lambda user: demog[user[0]], neighborhood)))
        result = np.sum(jaccard_score.dot(probaility_score.T) * ages)
        result = np.hstack((userId, result))
        results = np.vstack((results, result))
    return results


def bl(graph, demog, fd=False):
    res = list()
    count = int(0)

    for pId, conns in graph.items():
        count += 1
        if count % 1000 == 0:
            print(count)
        dateSum = 0
        totalLen = 0
        maxBDp = 0
        minBDp = sys.maxint
        print(pId)
        try:
            if demog[pId] is not None:
                continue
        except:
            print("good")
        if type(conns) == int:
            conns = [conns]
        for links in conns:
            totalLen += 1
            try:
                bd = int(demog[links])
            except:
                bd = sys.maxint

            if bd == sys.maxint:
                continue
            if bd > maxBDp:
                maxBDp = bd
            if bd < minBDp:
                minBDp = bd
            dateSum += int(bd)

        if (totalLen == 0):
            continue
        if (totalLen >= 4):
            avg = (dateSum - maxBDp - minBDp) / (totalLen - 2)
        else:
            avg = (dateSum) / (totalLen)
        res.append([pId, avg])
        if (fd):
            fd.write(str(pId) + '\t' + str(avg) + '\n')
    return res


if __name__ == '__main__':
    from GraphParser import graphParser

    cols = list()
    cols.append("userId")
    cols.append("birth_date")
    (demog, fd) = graphParser.parseFolderBySchema(os.path.join("Task1", "Task1",
                                                               "trainDemography"), 0, "",
                                                  "userId", cols, True)

    cols = list()
    cols.append("from")
    cols.append("to")
    cols.append("links")
    cols.append("mask")
    (graph, fd) = graphParser.parseFolderBySchema(os.path.join("Task1", "Task1", "graph"),
                                                  0, "", "from", cols,
                                                  True)
    print("data loaded")
    fdres = open("results.txt", 'w')
    bl(graph, demog, fdres)
