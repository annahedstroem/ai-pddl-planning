"""
DD2380 ai17 HT17-2 : (Artificial Intelligence) Floortile planning project
File: parse.py (Parsing information between pddl file and main file)
Authors: Antonie Legat, Anna Hedström, Sandra Picó, David Vega
12th October 2017
"""

import pddlpy

#All the pddl files that you can choose
Algorithms_Problems = ['algo_case_1.pddl','algo_case_2.pddl']
Size_Problems = ['size_case_1.pddl', 'size_case_2.pddl','size_case_3.pddl','size_case_4.pddl', 'size_case_5.pddl','size_case_6.pddl', 'size_case_7.pddl', 'size_case_8.pddl', 'size_case_9.pddl','size_case_10.pddl']
Pattern_Problems = ['pattern_case_1.pddl', 'pattern_case_2.pddl']
Robots_Problems = ['robots_case_1.pddl', 'robots_case_2.pddl', 'robots_case_3.pddl']


""" Parsing the information of the pddl file using the pddlpy library.
    Return the information of the pddl file (robots information, initial state and target state)
    """
def main():
    
    #All the robots will have 1000 availability of black color and white color.
    amount = 1000
    #Reading from the Domain and problem file.
    domprob = pddlpy.DomainProblem('Domain.pddl', Size_Problems[5])
    initRob = []
    initState = []
    targetState = []
    max_robot = -300
    #Checking how many robots we have in the pddl file
    for o in domprob.initialstate():
        if ((str(o)).split(',')[0] == "('robot-at'"):
            robot = ((str(o)).split(',')[1])[7]
            Row =(((str(o)).split(',')[2]).split('-')[0]).split('_')[1]
            Column = (((str(o)).split(',')[2]).split('-')[1]).split("'")[0]
            element = [(int(Column)),(int(Row))]
            
            #In order to know how many robots we have
            if (int(robot) > max_robot):
                max_robot = int(robot)

    #Create a list with all the information from the robots.
    for i in range(0,max_robot):
        element = []
        initRob.append(None)

    #Look at the initial positions of the robot.
    #Update the robots list.
    for o in domprob.initialstate():
        if ((str(o)).split(',')[0] == "('robot-at'"):
            robot = ((str(o)).split(',')[1])[7]
            Row =(((str(o)).split(',')[2]).split('-')[0]).split('_')[1]
            Column = (((str(o)).split(',')[2]).split('-')[1]).split("'")[0]
            element = [(int(Column)),(int(Row))]
            element2 = []
            element2.append(element)
            element2.append(0)
            element2.append(amount)
            element2.append(amount)
            initRob[int(robot)-1] = element2

    #Look at which color has the robot.
    for o in domprob.initialstate():
        if ((str(o)).split(',')[0] == "('robot-has'"):
            robot = ((str(o)).split(',')[1])[7]
            color = ((str(o)).split(',')[2])
            if(str(color) == " 'black')"):
                initRob[int(robot)-1][1]= 0
            else:
                initRob[int(robot)-1][1]= 1

    max_column= -3000
    max_rows= -3000
    #How many columns and how many rows we have in this pddl file.
    for o in domprob.worldobjects():
        if ('tile') in o:
            x,column =  (str(o)).split('-')
            if (int(column)>= int(max_column)):
                max_column = column
            z,row = (str(x)).split('_')
            if(int(row)>= int(max_rows)+1):
                max_rows = row

    # Create the initial and the target state.
    for i in range((int(max_rows)) +1):
        list = []
        list2= []
        for j in range(int(max_column)):
            list.append(0)
            list2.append(0)
        initState.append(list)
        targetState.append(list2)

    #Update the initState with the init robot positions.
    for i in range(0,max_robot):
        row_robot, column_robot = initRob[i][0]
        initState[column_robot][row_robot-1] = 3

    #Update the target state using the goals defined in the pddl file.
    for g in domprob.goals():
        goal_row = (((str(g)).split(',')[1]).split('-')[0]).split('_')[1]
        goal_column = (((str(g)).split(',')[1]).split('-')[1]).split("'")[0]
        goal_color = ((str(g)).split(',')[2])
        if (str(goal_color) == " 'black')"):
            num_color = 2
        else:
            num_color = 1

        targetState[int(goal_row)-1][int(goal_column)-1] = int(num_color)

    #return the robot information, the init state information and also the target State information
    return initRob, initState, targetState

