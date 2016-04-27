from ..Day_2.in_memory import get_friends


def mask_open(mask):
    mask = int(mask)
    opened = bin(mask)[2:]
    opened = '0' + opened[-1::-1]
    return opened


def get_relationships(mask: int) -> set:
    result = set()
    relationships = {1: 'Love',
                     2: 'Spouse',
                     3: 'Parent',
                     4: 'Child',
                     5: 'Brother/Sister',
                     6: 'Uncle/Aunt',
                     7: 'Relative',
                     8: 'Close friend',
                     9: 'Colleague',
                     10: 'Schoolmate',
                     11: 'Nephew',
                     12: 'Grandparent',
                     13: 'Grandchild',
                     14: 'College/University fellow',
                     15: 'Army fellow',
                     16: 'Parent in law',
                     17: 'Child in law',
                     18: 'Godparent',
                     19: 'Godchild',
                     20: 'Playing together',
                     21: ''}

    mask = mask_open(mask)
    for index, bit in enumerate(mask):
        if bit == '1':
            result.add(relationships[index])

    return result


def is_representative(mask: int):
    set_mask = get_relationships(mask)
    non_represent = {'Army fellow', 'Playing together'}
    very_represent = {'Love', 'Spouse', 'Parent', 'Child'}
    if not set_mask:
        return 1
    if non_represent & set_mask:
        return 0.1
    if very_represent & set_mask:
        return 7
    return 1


def jaccard_from_kailiak(userId_1: int, userId_2: int, graph: dict) -> float:
    # user1 is user for which we make a prediction
    neighborhood_1 = set(map(lambda x: x[0], graph[userId_1]))
    neighborhood_2 = set(map(lambda x: x[0], graph[userId_2]))
    c_friends = neighborhood_1 & neighborhood_2
    return len(c_friends) / len(neighborhood_1)


def jaccard_coefficient(userId_1: int, userId_2: int) -> float:
    neighborhood_1 = set(map(lambda x: x[0], get_friends(userId_1)))
    neighborhood_2 = set(map(lambda x: x[0], get_friends(userId_2)))
    c_friends = neighborhood_1 & neighborhood_2
    all_friends = neighborhood_1 | neighborhood_2
    return len(c_friends) / len(all_friends)


def list_nearest(user_id: int, friends: list) -> list:
    # return list with shape (count_of_friends, 2), where for every friend in descreasing order one line contains coefficient and location of friend
    answers = list()
    for friend_id, friend_mask in friends:
        result_friend = (1 + jaccard_coefficient(user_id, friend_id)) * is_representative(friend_mask)
        answers.append((result_friend, get_location(friend_id)))
    answers.sort()
    answers.reverse()
    return answers


def k_nearest(user_id, friends, k):
    list_1 = list_nearest(user_id, friends)
    list_k = list_1[:max(k, len(list_1))]
    dict = {}
    for x, y in list_k:
        dict.setdefault(y, 0)
        dict[y] += 1
    ma = -1
    ma_ind = -1
    for ind, value in dict.items():
        if ma < value:
            ma = value
            ma_ind = ind
    return ma_ind


def nearest(user_id, friends):
    return k_nearest(user_id, friends, 1)
