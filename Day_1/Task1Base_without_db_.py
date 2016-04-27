import pickle
import random
import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

from Day_1.relations import is_relevant, is_probably_same_age


def visualisation(data: np.ndarray, a, b):
    x_line = [random.randint(0, 100) for x in range(10)]
    y_line = [a * x_line[i] + b for i in range(10)]
    plt.plot(y_line, x_line)
    plt.scatter(data[:, 0], data[:, 1])
    plt.show()



def jaccard_coefficient(userId_1: int, userId_2: int) -> float:
    neighborhood_1 = set(map(lambda x: x[0], get_friends(userId_1)))
    neighborhood_2 = set(map(lambda x: x[0], get_friends(userId_2)))
    c_friends = neighborhood_1 & neighborhood_2
    all_friends = neighborhood_1 | neighborhood_2
    return len(c_friends) / len(all_friends)


def prediction_function():
    results = np.empty((0, 2))
    y = np.empty((0, 1))
    without_age = list()
    for userId, neighborhood in db.user_friends.find():
        try:
            age = get_age(userId)
            if age != None:
                y = np.vstack((y, age))
        except:
            without_age.append(userId)
            continue
        try:
            print('Age for user {} have to be predicted'.format(userId))
            neighborhood = list()
            if len(neighborhood) == 1:
                neighborhood.append(is_relevant(neighborhood))
            else:
                for user in neighborhood:
                    a = is_relevant(user)
                    neighborhood.append(a)
            neighborhood = np.array(neighborhood)
        except KeyError:
            continue
        print("{}' neighborhood exists".format(userId))
        probaility_score = list()
        jaccard_score = list()
        ages = list()

        for i, user in enumerate(neighborhood):
            try:
                jaccard_score.append(jaccard_coefficient(userId, user[0]))
            except KeyError:
                jaccard_score.append(0.5)
            prob_score = is_probably_same_age(user)
            probaility_score.append(prob_score)
            try:
                ages.append(get_age(user[1]))
            except KeyError:
                jaccard_score.pop()
                probaility_score.pop()
                continue
        ages = np.array(ages)
        print(ages.shape)
        jaccard_score = np.array(jaccard_score)
        print(jaccard_score.shape)
        probaility_score = np.array(probaility_score)
        result = np.sum(jaccard_score * probaility_score * ages) / np.sum(jaccard_score)
        result = np.hstack((userId, result))
        results = np.vstack((results, result))
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

''''
from GraphParser import graphParser
cols = list()
cols.append("from")
cols.append("to")
cols.append("links")
cols.append('mask')
(graph, fd) = graphParser.parseFolderBySchema("Task1/Task1/graph", 0, "", "from", cols, True)
with open("graph.pkl", "wb") as fout:
    pickle.dump(graph, fout)

cols = list()
cols.append("userId")
cols.append("birth_date")
(demog, fd) = graphParser.parseFolderBySchema("Task1/Task1/trainDemography", 0, "", "userId", cols, True)
with open("demog.pkl", "wb") as fout:
    pickle.dump(demog, fout)
graph = pickle.load(open('graph.pkl', 'rb'))
'''
y, results, without_age = prediction_function()
X = results[:, 1]
model = LinearRegression(normalize=True, n_jobs=-1)
model.fit(X, y)
y_hat = model.predict(without_age)
with open("y_hat.pkl", "wb") as f:
    pickle.dump(y_hat, f)


