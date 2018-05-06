# Floortile problem
# 2 robots, 2D

### PARAMETERS ###

param n; # nb rows
param m; # nb cols
param T; # time max
param R; # nb robots
param pattern{i in 1..n, j in 1..m};
param initialStock0{r in 1..R};
param initialStock1{r in 1..R};

### VARIABLES ###

var tstar integer >=1; # time needed for complete board
var cell{i in 1..n, j in 1..m, t in 1..T} binary; # 0 = not painted, 1 = painted
var painting{i in 1..n, j in 1..m, t in 1..T, r in 1..R} binary; # 1 = r is painting (i,j) at time t

# State of the robot
var y{t in 1..T, r in 1..R} integer >= 0, <= n;
var x{t in 1..T, r in 1..R} integer >= 1, <= m;
var color{t in 1..T, r in 1..R} binary; # 0 = black, 1 = white
var stock0 {t in 1..T, r in 1..R} integer >= 0; # stock of black color
var stock1 {t in 1..T, r in 1..R} integer >= 0; # stock of white color

# Actions of the robot, 1 = doing this action
var paint{t in 1..T-1, r in 1..R} binary;
var move{t in 1..T-1, r in 1..R} binary;
var switch{t in 1..T-1, r in 1..R} binary;

### OBJECTIVE ###

minimize objective: tstar - sum{i in 1..n, j in 1..m, t in 1..T-1, r in 1..R} painting[i,j,t,r];

### CONSTRAINTS ###

subject to BoardComplete:
	exists{t in 1..T} (sum{i in 1..n, j in 1..m} cell[i,j,t] = n*m and t = tstar);
	
subject to OneAction {t in 1..T-1, r in 1..R}:
	paint[t,r] + move[t,r] + switch[t,r] <= 1;

subject to NotStandOnPaint {t in 1..T, r in 1..R}:
	y[t,r] >= 1 ==> exists{i in 1..n, j in 1..m} (cell[i,j,t] = 0 and y[t,r] = i and x[t,r] = j);

subject to OneRobotPerCellX {t in 1..T}:
	x[t,1] = x[t,2] ==> y[t,1] <> y[t,2];
subject to OneRobotPerCellY {t in 1..T}:
	y[t,1] = y[t,2] ==> x[t,1] <> x[t,2];

# Initial conditions
subject to InitialY:
	y[1,1] = 0 and y[1,2] = 0;
subject to InitialX:
	x[1,1] = 1 and x[1,2] = 2;
subject to InitialColor{r in 1..R}:
	color[1,r] = 0;
subject to InitialBoard {i in 1..n, j in 1..m}:
	cell[i,j,1] = 0;
subject to InitialStock0{r in 1..R}:
	stock0[1,r] = initialStock0[r];
subject to InitialStock1{r in 1..R}:
	stock1[1,r] = initialStock1[r];

# Paintings
subject to Painting01 {t in 1..T-1, r in 1..R}:
 	paint[t,r] = 1 and y[t,r] = 0 and x[t,r] = 1 ==> painting[1,1,t,r] = 1;
subject to Painting02 {t in 1..T-1, r in 1..R}:
	paint[t,r] = 1 and y[t,r] = 0 and x[t,r] = 2 ==> painting[1,2,t,r] = 1;
subject to Painting11 {t in 1..T-1, r in 1..R}:
	paint[t,r] = 1 and y[t,r] = 1 and x[t,r] = 1 ==> painting[2,1,t,r] = 1;
subject to Painting12 {t in 1..T-1, r in 1..R}:
	paint[t,r] = 1 and y[t,r] = 1 and x[t,r] = 2 ==> painting[2,2,t,r] = 1;
subject to Painting21 {t in 1..T-1, r in 1..R}:
	paint[t,r] = 1 and y[t,r] = 2 and x[t,r] = 1 ==> painting[1,1,t,r] = 1;
subject to Painting22 {t in 1..T-1, r in 1..R}:
	paint[t,r] = 1 and y[t,r] = 2 and x[t,r] = 2 ==> painting[1,2,t,r] = 1;
subject to PaintOnlyOne {t in 1..T-1, r in 1..R}:
	paint[t,r] = 1 ==> sum{i in 1..n, j in 1..m} painting[i,j,t,r] = 1;
subject to NotPainting {i in 1..n, j in 1..m, t in 1..T-1, r in 1..R}:
	paint[t,r] = 0 ==> painting[i,j,t,r] = 0;
	
# Cells update
subject to UpdateCells {i in 1..n, j in 1..m, t in 1..T-1}:
	cell[i,j,t] = 0 and sum{r in 1..R} painting[i,j,t,r] >= 1 ==> cell[i,j,t+1] = 1;
subject to NotUpdateCells {i in 1..n, j in 1..m, t in 1..T-1}:
	cell[i,j,t] = 0 and sum{r in 1..R} painting[i,j,t,r] = 0 ==> cell[i,j,t+1] = 0;

# Position update
subject to Moving {t in 1..T-1, r in 1..R}:
	move[t,r] = 1 ==> abs(y[t+1,r] - y[t,r]) + abs(x[t+1,r] - x[t,r]) = 1;
subject to NotMoving {t in 1..T-1, r in 1..R}:
	move[t,r] = 0 ==> y[t+1,r] = y[t,r] and x[t+1,r] = x[t,r];

# Color update
subject to Switching {t in 1..T-1, r in 1..R}:
	switch[t,r] = 1 ==> abs(color[t+1,r] - color[t,r]) = 1;
subject to NotSwitching {t in 1..T-1, r in 1..R}:
	switch[t,r] = 0 ==> color[t+1,r] = color[t,r];

# Stock update
subject to DecrementStock0 {t in 1..T-1, r in 1..R}:
	paint[t,r] = 1 and color[t,r] = 0 ==> stock0[t+1,r] = stock0[t,r] - 1 and stock1[t+1,r] = stock1[t,r];
subject to DecrementStock1 {t in 1..T-1, r in 1..R}:
	paint[t,r] = 1 and color[t,r] = 1 ==> stock1[t+1,r] = stock1[t,r] - 1 and stock0[t+1,r] = stock0[t,r];
subject to StockRemainsSame {t in 1..T-1, r in 1..R}:
	paint[t,r] = 0 ==> stock0[t+1,r] = stock0[t,r] and stock1[t+1,r] = stock1[t,r];

# Respect the pattern
subject to RespectPattern {t in 1..T-1, r in 1..R}:
	paint[t,r] = 1 and y[t,r] <= n-1 ==>
	exists{i in 0..n-1, j in 1..m} (color[t,r] = pattern[i+1,j] and i = y[t,r] and j = x[t,r]);
