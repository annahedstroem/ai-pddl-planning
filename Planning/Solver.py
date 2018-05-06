"""
    DD2380 ai17 HT17-2 : (Artificial Intelligence) Floortile planning project
    File: Solver.py (File not used. First idea of the project implementation.)
    Authors: Antonie Legat, Anna Hedström, Sandra Picó, David Vega
    12th October 2017
"""

import sys
from  pddlpy import DomainProblem

def possible_Movements(action, H, W, domprob):
    W += 1
    movex = 0
    movey = 0
    if (action == "up"):
        movey = 1
    elif (action == "down"):
        movey = -1
    elif (action == "left"):
        movex = -1
    else:
        movex = 1
    movements = {}
    indexes = list(reversed(list(range(H))))
    print(indexes)
    for i in indexes:
        for j in range(1, W):
            if (i + movey >= 0 and i + movey < H):
                if (j + movex >= 0 and j + movex < W):
                    currentTile = "tile_" + str(i) + "-" + str(j)
                    targetTile = "tile_" + str(i + movey) + "-" + str(j + movex)
                    movements[currentTile] = []
                    print(currentTile, targetTile)
                    for o in domprob.ground_operator(action):
                        if (action, targetTile, currentTile) in o.precondition_pos:
                            movements[currentTile].append(o.precondition_pos)
    return movements


def possible_Paint(H, W, domprob):
    W += 1
    movex = 0
    movey = 1
    painting_up = {}
    painting_down = {}
    action = "paint-up"
    indexes = list(reversed(list(range(H))))
    print(indexes)
    for i in indexes:
        for j in range(1, W):
            if (i + movey >= 0 and i + movey < H):
                if (j + movex >= 0 and j + movex < W):
                    currentTile = "tile_" + str(i) + "-" + str(j)
                    targetTile = "tile_" + str(i + movey) + "-" + str(j + movex)
                    painting_up[currentTile] = []
                    print(currentTile, targetTile)
                    for o in domprob.ground_operator(action):
                        if ('up', targetTile, currentTile) in o.precondition_pos:
                            painting_up[currentTile].append(o.precondition_pos)
    action = "paint-down"
    movey = -1
    print("######")
    for i in indexes:
        for j in range(1, W):
            if (i + movey >= 0 and i + movey < H):
                if (j + movex >= 0 and j + movex < W):
                    currentTile = "tile_" + str(i) + "-" + str(j)
                    targetTile = "tile_" + str(i + movey) + "-" + str(j + movex)
                    painting_down[currentTile] = []
                    print(currentTile, targetTile)
                    for o in domprob.ground_operator(action):
                        if ('down', targetTile, currentTile) in o.precondition_pos:
                            painting_down[currentTile].append(o.precondition_pos)
    return [painting_up, painting_down]

robot = [0, 1, "black", 10, 10]
def main(argv):

    domainfile = "domain-04.pddl"  ##% demonumber
    problemfile = "problem-04.pddl"  ##% demonumber
    domprob = DomainProblem(domainfile, problemfile)
    H = 5
    W = 3
    res = possible_Movements("up", H, W, domprob)
    print(res)
    print("-------")
    res = possible_Paint(H, W, domprob)
    print(res[0])
    print(res[1])

if __name__ == '__main__':
    main(sys.argv)
