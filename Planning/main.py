"""
DD2380 ai17 HT17-2 : (Artificial Intelligence) Floortile planning project
File: main.py (Main file)
Authors: Antonie Legat, Anna Hedström, Sandra Picó, David Vega
12th October 2017
"""
from copy import copy, deepcopy
import datetime as time
import numpy as np
import parse as p
import Interface as gui

robot1 = []
robot2 = []
robots =[]
state = []
target = []
columns = 0
rows = 0


#Path as a global variable
path = []

# Sequence
sequenceStates = []

# Robots
sequenceRobots =[]

# Keeping track during DP
sequenceMovements = []

## trying all the possible combinations between N robots
def getSequence(robots,index,currState,seqMov,seqRobots,target):
    if(index == len(robots)):
        global sequenceStates,sequenceRobots,sequenceMovements
        sequenceMovements.append(seqMov)
        sequenceStates.append(currState)
        sequenceRobots.append(seqRobots)
        return
    possibles,movement = getPossiblesFOC_ClearCells(robots[index],currState,target)
    for i in range(len(possibles)):
        auxMov = deepcopy(seqMov)
        auxMov.append("Robot"+str(index+1) +": " +str(movement[i]))
        auxRobots= deepcopy(seqRobots)
        auxRobots.append(possibles[i][0])
        getSequence(robots, index+1, possibles[i][1],auxMov,auxRobots,target)
    return

## this functions checks all the possible actions that we can take for a given robot and an state
## target it's our goal, we want to paint with the colors that we should
def moveRobot(robot, dx, dy):
    return [[robot[0][0] + dx, robot[0][1] + dy], robot[1], robot[2], robot[3]]

def removePaint(robot, d1, d2):
    return [robot[0], robot[1], robot[2] - d1, robot[3] - d2]

def changePaint(robot, change):
    return [robot[0], change, robot[2], robot[3]]


""" Generate the next possibles states taking into account the preconditions and also the Forced Ordering Constraints.
    In this case, this function is used when the pattern has some clear cells in the target.
    @robot - robot information defined as: [ [x,y], color, color1Remaining, color2Remaining]
    @state - matrix that defines the current state configuration
    @target - matrix that defines the target configuration
    """
def getPossiblesFOC_ClearCells(robot, state, target):

    s = []
    states = []

    #If the robot wants to move in an existing position and the position of this particular state is clear..
    if ((robot[0][1] + 1) < len(state) and state[robot[0][1] + 1][robot[0][0]] == 0):
        row = robot[0][1]
        column = robot[0][0]
        painted = True
        #Priorizing
        #Forced ordering constraints.
        if (row != 0):
            for i in range(0,row):
                for j in range(0, columns):
                    #If there is non-painted cell
                    if ((state[i][j] != 2) and (state[i][j] != 1)):
                        #If is really need to be painted...
                        if((target[i][j] == 2) or (target[i][j] == 1)):
                            painted = False
        if (painted == True):
            s.append("down")
            aux = deepcopy(state)
            aux[robot[0][1]][robot[0][0]] = 0
            aux[robot[0][1] + 1][robot[0][0]] = 3
            states.append([moveRobot(robot, 0, 1), aux])

    #If the robot wants to move in an existing position and the position of this particular state is clear..
    if ((robot[0][1] - 1) >= 0 and state[robot[0][1] - 1][robot[0][0]] == 0):
        s.append("up")
        aux = deepcopy(state)
        aux[robot[0][1]][robot[0][0]] = 0
        aux[robot[0][1] - 1][robot[0][0]] = 3
        states.append([moveRobot(robot, 0, -1), aux])

    #If the robot wants to move in an existing position and the position of this particular state is clear..
    if ((robot[0][0] + 1) < len(state[0]) and state[robot[0][1]][robot[0][0] + 1] == 0):
        s.append("right")
        aux = deepcopy(state)
        aux[robot[0][1]][robot[0][0]] = 0
        aux[robot[0][1]][robot[0][0] + 1] = 3
        states.append([moveRobot(robot, 1, 0), aux])

     #If the robot wants to move in an existing position and the position of this particular state is clear..
    if ((robot[0][0] - 1) >= 0 and state[robot[0][1]][robot[0][0] - 1] == 0):
        s.append("left")
        aux = deepcopy(state)
        aux[robot[0][1]][robot[0][0]] = 0
        aux[robot[0][1]][robot[0][0] - 1] = 3
        states.append([moveRobot(robot, -1, 0), aux])
    
    ## if its possible to move up / we have paint / we need to paint it like that / and the "up"- row is already painted..
    if (("up") in s and robot[1 + robot[1]] > 0 and target[robot[0][1] - 1][robot[0][0]] == robot[1]):
        #Where you want to paint
        row_robot = robot[0][1]-1
        column_robot = robot[0][0]
        painted = True
        if (row_robot != 0):
            for i in range(0,row_robot):
                for j in range(0,columns):
                    if ((state[i][j] != 2) and (state[i][j] != 1)):
                        #And its really needed to paint there..
                         if((target[i][j] == 2) or (target[i][j] == 1)):
                            painted = False
        if (painted == True):
            s.append("paint_up")
            aux = deepcopy(state)
            aux[robot[0][1] - 1][robot[0][0]] = robot[1]
            d1 = d2 = 0
            if (robot[1] == 1):
                d1 = 1
            else:
                d2 = 1
            states.append([removePaint(robot, d1, d2), aux])
    ## todo append SAT for painting
    if(robot[ robot[1] +  1 ] >0):
        if(robot[1] == 1):
            auxR = changePaint(robot,2)
            s.append("change_paint_black")
        else:
            auxR = changePaint(robot,1)
            s.append("change_paint_white")
        states.append([auxR, state])
    s.append("still")
    states.append( [robot, state])
    return states, s


""" Generate the next possibles states taking into account the preconditions and also the Forced Ordering Constraints.
    In this case, the algorithm is much more effected because a lot of braches are prunned. The action paint_down is not considered.
    @robot - robot information defined as: [ [x,y], color, color1Remaining, color2Remaining]
    @state - matrix that defines the current state configuration
    @target - matrix that defines the target configuration
    """
def getPossiblesFOC(robot, state, target):
    s = []
    states = []

    #If its possible to go down...
    if ((robot[0][1] + 1) < len(state) and state[robot[0][1] + 1][robot[0][0]] == 0):
        row = robot[0][1]
        column = robot[0][0]
        painted = True
        #Check if you are not in the top row and if you have tiles to paint up you.
        if (row != 0):
            for i in range(0,row):
                for j in range(0, columns):
                    if ((state[i][j] != 2) and (state[i][j] != 1)):
                        painted = False
    
        #You can only go down if you don't have any non-painted tile up to you. (Forced Ordering Constraints)
        if (painted == True):
            s.append("down")
            aux = deepcopy(state)
            aux[robot[0][1]][robot[0][0]] = 0
            aux[robot[0][1] + 1][robot[0][0]] = 3
            states.append([moveRobot(robot, 0, 1), aux])

    if ((robot[0][1] - 1) >= 0 and state[robot[0][1] - 1][robot[0][0]] == 0):
        s.append("up")
        aux = deepcopy(state)
        aux[robot[0][1]][robot[0][0]] = 0
        aux[robot[0][1] - 1][robot[0][0]] = 3
        states.append([moveRobot(robot, 0, -1), aux])
    
    if ((robot[0][0] + 1) < len(state[0]) and state[robot[0][1]][robot[0][0] + 1] == 0):
        s.append("right")
        aux = deepcopy(state)
        aux[robot[0][1]][robot[0][0]] = 0
        aux[robot[0][1]][robot[0][0] + 1] = 3
        states.append([moveRobot(robot, 1, 0), aux])
    
    if ((robot[0][0] - 1) >= 0 and state[robot[0][1]][robot[0][0] - 1] == 0):
        s.append("left")
        aux = deepcopy(state)
        aux[robot[0][1]][robot[0][0]] = 0
        aux[robot[0][1]][robot[0][0] - 1] = 3
        states.append([moveRobot(robot, -1, 0), aux])
    
    ## if up is clear / we have paint / we need to paint it like that / and the "up"- row is already painted..
    if (("up") in s and robot[1 + robot[1]] > 0 and target[robot[0][1] - 1][robot[0][0]] == robot[1]):
        #Where you want to paint
        row_robot = robot[0][1]-1
        column_robot = robot[0][0]
        painted = True
        #If you want to paint, check if there is any other tile non-painted up to you.
        if (row_robot != 0):
            for i in range(0,row_robot):
                for j in range(0,columns):
                    if ((state[i][j] != 2) and (state[i][j] != 1)):
                        painted = False
        if (painted == True):
            s.append("paint_up")
            aux = deepcopy(state)
            aux[robot[0][1] - 1][robot[0][0]] = robot[1]
            d1 = d2 = 0
            if (robot[1] == 1):
                d1 = 1
            else:
                d2 = 1
            states.append([removePaint(robot, d1, d2), aux])

    #Change color if available.
    if(robot[ robot[1] +  1 ] >0):
        if(robot[1] == 1):
            auxR = changePaint(robot,2)
            s.append("change_paint_black")
        else:
            auxR = changePaint(robot,1)
            s.append("change_paint_white")
        states.append([auxR, state])
    s.append("still")
    states.append( [robot, state])
    return states, s



""" Generate the next possibles states taking into account the preconditions.
    Generate all the possibles nextStates without Forced Ordering Constraints
    @robot - robot information defined as: [ [x,y], color, color1Remaining, color2Remaining]
    @state - matrix that defines the current state configuration
    @target - matrix that defines the target configuration
    """
def getPossibles(robot, state, target):

    s = []
    states = []
    
    
    """
    ## For actions: down, up, right, left, can be considered as a possible action if:
    ##   The adjacent cell exists (where you want to move) and if it's clear ( no robot, no painted )
    ##        exists -> it's in the bounds of the board
    """
    if ((robot[0][1] + 1) < len(state) and state[robot[0][1] + 1][robot[0][0]] == 0):
        s.append("down")
        aux = deepcopy(state)
        aux[robot[0][1]][robot[0][0]] = 0
        aux[robot[0][1] + 1][robot[0][0]] = 3
        states.append([moveRobot(robot, 0, 1), aux])

    if ((robot[0][1] - 1) >= 0 and state[robot[0][1] - 1][robot[0][0]] == 0):
        s.append("up")
        aux = deepcopy(state)
        aux[robot[0][1]][robot[0][0]] = 0
        aux[robot[0][1] - 1][robot[0][0]] = 3
        states.append([moveRobot(robot, 0, -1), aux])

    if ((robot[0][0] + 1) < len(state[0]) and state[robot[0][1]][robot[0][0] + 1] == 0):
        s.append("right")
        aux = deepcopy(state)
        aux[robot[0][1]][robot[0][0]] = 0
        aux[robot[0][1]][robot[0][0] + 1] = 3
        states.append([moveRobot(robot, 1, 0), aux])

    if ((robot[0][0] - 1) >= 0 and state[robot[0][1]][robot[0][0] - 1] == 0):
        s.append("left")
        aux = deepcopy(state)
        aux[robot[0][1]][robot[0][0]] = 0
        aux[robot[0][1]][robot[0][0] - 1] = 3
        states.append([moveRobot(robot, -1, 0), aux])


    ## To execute paint_up, the preconditions that must happen are:
    ## if up is clear( we can execute up action) / we have enough amount of paint / we need to paint it like that (as target defines)
    if (("up") in s and robot[1 + robot[1]] > 0 and target[robot[0][1] - 1][robot[0][0]] == robot[1]):
        s.append("paint_up")
        aux = deepcopy(state)
        aux[robot[0][1] - 1][robot[0][0]] = robot[1]
        d1 = d2 = 0
        if (robot[1] == 1):
            d1 = 1
        else:
            d2 = 1
        states.append([removePaint(robot, d1, d2), aux])

    if (("down") in s and robot[1 + robot[1]] > 0 and target[robot[0][1] + 1][robot[0][0]] == robot[1]):
        s.append("paint_down")
        aux = deepcopy(state)
        aux[robot[0][1] + 1][robot[0][0]] = robot[1]
        d1 = d2 = 0
        if (robot[1] == 1):
            d1 = 1
        else:
            d2 = 1
        states.append([removePaint(robot, d1, d2), aux])

    ## If the robot wants to paint , we need to check that is possible ( enough amount of paint )
    if(robot[ robot[1] +  1 ] >0):
        if(robot[1] == 1):
            auxR = changePaint(robot,2)
            s.append("change_paint_black")
        else:
            auxR = changePaint(robot,1)
            s.append("change_paint_white")
        states.append([auxR, state])
    
    s.append("still")
    states.append( [robot, state])
    return states, s

""" Forward Search algorithm to solve the problem
    This is the first version that we did to solve the problem. It only works with 2 robots.
    @how_many_robots - integer that define how many robots we have in the state.
    @robots - list of robots defined as [ [x,y], color, color1Remaining, color2Remaining]
    @iniState - matrix that defines the initial configuration
    @target - matrix that defines the target configuration
    """
def solve_2robots(how_many_robots,robots, iniState, target):
    # using list as queue and dictionary as hashmap
    q = []
    visited = {}
    # initializing the queue for the BFS
    # the state it's represented as current state of robots
    # current state of the board
    # and the list of movements
    q.append([robots, iniState, []])
    # Using np arrays because of comparation function between matrices
    targetCheck = np.array(target)
    # flag to check if we were able to achieve the target
    done = False;
    current = None
    robotPossibles = []
    robotMovement = []
    index  = []
    for i in range(0,how_many_robots):
        element = []
        num = 0
        robotPossibles.append(element)
        index.append(num)
        robotMovement.append(element)
    
    while q:
        current = q[0]
        q.pop(0)
        currentCheck = np.array(current[1])
        # converting the state to string for hashing
        keyState = str(current[1])
        KeyRobots = str(current[0])
        # checking if we have been in this state before
        value1 = visited.get(keyState)
        value2 = visited.get(KeyRobots)
        if value1!= None:
            continue
        # marking and hashing state
        visited[keyState] = True
        visited[KeyRobots] = True

        # Checking if our current board it's our target
        currentCheck[currentCheck == 3] = 0
        if (currentCheck == targetCheck).all():
            print(currentCheck)
            print(current[2])
            global path
            path = current[2]
            done = True
            break;

        # Get possibles for robot1 then try those as current States for robot2 and so on
        # Only working with 2 robots.
        robot1Possibles, movement1 = getPossiblesFOC_2(current[0][0], current[1], target)
        index1 = 0
        for possible1 in robot1Possibles:
            robot2Possibles, movement2 = getPossiblesFOC_2(current[0][1], possible1[1], target)
            index2 = 0
            for possible2 in robot2Possibles:
                sequence = deepcopy(current[2])
                sequence.append("Robot1: " + movement1[index1])
                sequence.append("Robot2: " + movement2[index2])
                index2 += 1
                q.append([[possible1[0], possible2[0]], possible2[1], sequence])
            index1 += 1
    return done


""" Forward Search algorithm to solve the problem
    @how_many_robots - integer that define how many robots we have in the state.
    @robots - list of robots defined as [ [x,y], color, color1Remaining, color2Remaining]
    @iniState - matrix that defines the initial configuration
    @target - matrix that defines the target configuration
    """
def solve_NRobots(how_many_robots, robots, iniState, target):

    # using list as queue and dictionary as hashmap
    q = []
    visited = {}
    # initializing the queue for the BFS
    # the state it's represented as current state of robots
    # current state of the board
    # and the list of movements
    q.append([robots, iniState, []])
    # Using np arrays because of comparation function between matrices
    targetCheck = np.array(target)
    # flag to check if we were able to achieve the target
    done = False;
    current = None
    robotPossibles = []
    robotMovement = []
    index  = []
    for i in range(0,how_many_robots):
        element = []
        num = 0
        robotPossibles.append(element)
        index.append(num)
        robotMovement.append(element)
    while q:
        current = q[0]
        q.pop(0)
        currentCheck = np.array(current[1])
        ### converting the state to string for hashing
        keyState = str(current[1])
        KeyRobots = str(current[0])
        ### checking if we have been in this state before
        value1 = visited.get(keyState)
        value2 = visited.get(KeyRobots)
        if value1!= None:
            continue
        # marking and hashing state
        visited[keyState] = True
        visited[KeyRobots] = True

        # Checking if our current board it's our target
        currentCheck[currentCheck == 3] = 0
        if (currentCheck == targetCheck).all():
            print(currentCheck)
            print(current[2])
            global path
            path = current[2]
            done = True
            break;

        global sequenceRobots,sequenceStates,sequenceMovements
        # Sequence
        sequenceStates = []
        # Robots
        sequenceRobots =[]
        # Keeping track during DP
        sequenceMovements = []

        # Get possibles for all the robots.
        # This algorithm works with N robots.
        getSequence(current[0],0,current[1],[],[],target)
        for i in range(len(sequenceStates)):
            aux = deepcopy(current[2])
            aux.extend(sequenceMovements[i])
            q.append( [sequenceRobots[i], sequenceStates[i], aux]    )
    return done


""" Main function of the program:
    - Take the information of the pddl.
    - Solve the planning problem.
    - Send the path into the graphics.
    - Print the cpu time needed to find the optimal path.
    """
if __name__ == '__main__':
    
    #Actual time
    a = time.datetime.now()
    #Information from the PDDL file using parse.py. Robots information, the initial state and the target state.
    robots,state,target = p.main()
    how_many_robots = len(robots)
    for i in range(0,how_many_robots):
        robots[i][1] +=1
        robots[i][0][0] -=1
    rows = len(state)
    columns = len(state[0])
    solution = False
    #Solve and find the proper path
    solution = solve_NRobots(how_many_robots,robots, state, target)
    #Time needed
    print("Time: ")
    print(time.datetime.now() - a)
    if (solution == True):
        #We found a path. Needed to draw it.
        print("Solved")
        #Draw and simulate the path.
        gui.Draw(robots,state,path)
    else:
        #No path found.
        print("To solve")


