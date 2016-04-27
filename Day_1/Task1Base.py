import pickle
import random
import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

from Day_1.relations import is_relevant, is_probably_same_age
from Day_1.database import db, get_age, get_friends

def visualisation(data: np.ndarray, a, b):
    x_line = [random.randint(0, 100) for x in range(10)]
    y_line = [a * x_line[i] + b for i in range(10)]
    plt.plot(y_line, x_line)
    plt.scatter(data[:, 0], data[:, 1])
    plt.show()


def common_friends(userId_1: int, userId_2: list) -> float:
    neighborhood_1 = set(map(lambda x: x[0], get_friends(userId_1)))
    neighborhood_2 = set(map(lambda x: x[0], get_friends(userId_2)))
    c_friends = list(neighborhood_1 & neighborhood_2)
    return len(c_friends)


def jaccard_coefficient(userId_1: int, userId_2: int) -> float:
    neighborhood_1 = set(map(lambda x: x[0], get_friends(userId_1)))
    neighborhood_2 = set(map(lambda x: x[0], get_friends(userId_2)))
    c_friends = neighborhood_1 & neighborhood_2
    all_friends = neighborhood_1 | neighborhood_2
    return len(c_friends) / len(all_friends)


def jaccard_from_kailiak(userId_1: int, userId_2: int, graph: dict) -> float:
    # user1 is user for which we make a prediction
    neighborhood_1 = set(map(lambda x: x[0], graph[userId_1]))
    neighborhood_2 = set(map(lambda x: x[0], graph[userId_2]))
    c_friends = neighborhood_1 & neighborhood_2
    return len(c_friends) / len(neighborhood_1)


def prediction_function():
    results = np.empty((0, 2))
    y = np.empty((0, 1))
    without_age = list()
    missed = list()
    for user in db.user_friends.find():
        userId = user['id']
        neighborhood = user['friends']
        try:
            age = get_age(userId)
            if age != None:
                y = np.vstack((y, age))
        except:
            without_age.append(userId)
            print(userId)
            continue
        print('Age for user {} have to be predicted'.format(userId))
        try:
            neighborhood = np.array(list(filter(is_relevant, neighborhood)))
            print("{}' neighborhood exists".format(userId))
            jaccard_score = np.array([jaccard_coefficient(userId, user[0]) for user in neighborhood])
            print(jaccard_score)
            probaility_score = np.array(list(map(is_probably_same_age, neighborhood)))
            ages = np.array(list(map(lambda user: get_age(user[0]), neighborhood)))
            print(ages)
            result = np.sum(jaccard_score * probaility_score * ages) / np.sum(jaccard_score)
            result = np.hstack((userId, result))
            results = np.vstack((results, result))
        except KeyError:
            missed.append(userId)
            continue
    return y, results, without_age


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
    (demog, fd) = graphParser.parseFolderBySchema("Task1/Task1/trainDemography", 0, "", "userId", cols, True)



    cols = list()
    cols.append("from")
    cols.append("to")
    cols.append("links")
    cols.append('mask')
    (graph, fd) = graphParser.parseFolderBySchema("Task1/Task1/graph", 0, "", "from", cols, True)
    with open("graph.pkl", "wb") as fout:
        pickle.dump(graph, fout)

    y, results, without_age = prediction_function(demog, graph)
    X = results[:, 1]
    model = LinearRegression(normalize=True, n_jobs=-1)
    model.fit(X, y)
    y_hat = model.predict(without_age)
    with open("y_hat.pkl", "wb") as f:
        pickle.dump(y_hat, f)


