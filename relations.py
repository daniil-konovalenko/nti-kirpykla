
def mask_open(mask):
    opened = bin(mask)[2:]
    opened = '0' + opened[-1::-1]
    return opened

def get_non_relatives(graph, user) -> list:
    friends = graph[user]
    non_relatives = [friend for friend in friends if not is_relative(user)]
    return non_relatives


def is_relative(user: list) -> bool:
    mask = user[1]
    relationship = get_relationships(mask)
    relatives =  {'Parent',
                  'Child',
                  'Brother/Sister',
                  'Uncle/Aunt',
                  'Relative',
                  'Nephew',
                  'Grandparent',
                  'Grandchild',
                  'Parent in law',
                  'Child in law',
                  'Godparent',
                  'Godchild'
                    }
    if relationship & relatives:
        return True
    else:
        return False

def is_probably_same_age(user: list, k=3):
    mask = user[1]
    relationships = get_relationships(mask)
    same_agers = {'Army fellow',
                  'College/University fellow',
                  'Schoolmate',
                  }
    if relationships & same_agers:
        return True * k
    return False

def get_relationships(mask: int) -> str:
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
                     15: 'Army fellow ',
                     16: 'Parent in law',
                     17: 'Child in law',
                     18: 'Godparent',
                     19: 'Godchild',
                     20: 'Playing together'}

    mask = mask_open(mask)
    for index, bit in enumerate(mask):
        if bit == '1':
            result.add(relationships[index])

    return  result

def is_relevant(user):
    mask = user[1]
    if not mask:
        return True
    if is_probably_same_age(user) and not is_relative(user):
        return True
    else:
        return False
