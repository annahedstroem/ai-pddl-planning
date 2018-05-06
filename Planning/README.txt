Authors: Sandra Picó, David Vega, Anna Hedström and Antonie Legat
Title: Floortile - Project Artificial Intelligence (DD2380)
12th October 2017

DESCRIPTION

ICPS Planning competition : “A set of robots use different colors to paint patterns in floor tiles. The robots can move around the floor tiles in four directions (up, down, left and right). Robots paint with one color at a time, but can change their spray guns to any available color. However, robots can only paint the tile that is in front (up) and behind (down) them, and once a tile has been painted no robot can stand on it. 
For the IPC set, robots need to paint a grid with black and white, where the cell color is alternated always. This particular configuration makes the domain hard because robots should only paint tiles in front of them, since painting tiles behind make the search to reach a dead-end.” 


GETTING STARTED

Prerequisites : To be able to run this project, you need to install the following library:

1. Install pddlpy library

	pip install pddlpy

RUNNING THE PROJECT

In order to run the project you just have to run the main file:

	python main.py

Once you run it, you will be able to watch the result for an specific pattern.


CHANGE THE PDDL FILE

If you want to test different cases, you need to change the pddl file read in the parse.py file.

	1. Open the parse.py with an editor

	

	2. In the line 25, you will find the following line of code:
		
		domprob = pddlpy.DomainProblem('Domain.pddl', Size_Problems[5])

	3. To change the pddl environment, you only need to change the second argument of the function. You have the following options (declared in the 		parse.py file):

		Size_Problems =['size_case_1.pddl','size_case_2.pddl','size_case_3.pddl','size_case_4.pddl', 'size_case_5.pddl','size_case_6.pddl', 'size_case_7.pddl', 'size_case_8.pddl', 'size_case_9.pddl','size_case_10.pddl']
Pattern_Problems = ['pattern_case_1.pddl', 'pattern_case_2.pddl']
Robots_Problems = ['robots_case_1.pddl', 'robots_case_2.pddl', 'robots_case_3.pddl']



	4. Example: If you want to change the environment ‘size_case_5.pddl’ (Size_Problems[5]) , for the environment ‘robots_case_1.pddl’. You only need to change the line of code stated before for:


	domprob = pddlpy.DomainProblem('Domain.pddl', Robots_Problems[0])


UNDERSTANDING THE PDDL ENVIRONMENTS

Each of the environment represents a specific case in our project:

Size_Problems: All the PDDL files contained in this array increments the size of the grid proportionally. That’s why if you executed the third case, you will have to wait more time (until you get the solution) compared with the second and the first ones.

Pattern_Problems: The first pattern pddl file paints a pattern where all the tiles are painted. The second one, have some tiles that have to remain non-painted.

Robots_Problems: Incrementing the number of robots in each file. First file: 2 robots, second file: 3 robots, third file: 4 robots (if you execute this file, you will need to wait 20-30 minutes to achieve the result).



