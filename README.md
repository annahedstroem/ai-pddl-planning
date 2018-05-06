# ai-pddl-planning

**Description of project** (floortile)

ICPS Planning competition : “A set of robots use different colors to paint patterns in floor tiles. The robots can move around the floor tiles in four directions (up, down, left and right). Robots paint with one color at a time, but can change their spray guns to any available color. However, robots can only paint the tile that is in front (up) and behind (down) them, and once a tile has been painted no robot can stand on it. 
For the IPC set, robots need to paint a grid with black and white, where the cell color is alternated always. This particular configuration makes the domain hard because robots should only paint tiles in front of them, since painting tiles behind make the search to reach a dead-end.” 

We solve this problem in two different ways: using a Planning domain (PDDL) and using Optimization.

**Getting started**

1. Planning folder: Here you will find all the files needed and the README file for the Planning domain execution.
In this case, you will be able to view a simulation of how different environments (#robots, grid size, patterns) find an optimal path and simulate this path in a graph environment. 

2. Optimization folder: In order to be able to execute this files you need to install a specific software called AMPL. In the README file that you will find in the folder, we will explain you how to install it properly. 

**Authors** Anna Hedström, Antonie Legat, Sandra Picó, David Vega
