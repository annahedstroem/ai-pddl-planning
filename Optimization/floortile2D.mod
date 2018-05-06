# Floortile problem
# 1 robot, 2D

### PARAMETERS ###

param n; # nb rows
param m; # nb cols
param T; # time max
param pattern{i in 1..n, j in 1..m};
param initialStock0;
param initialStock1;

### VARIABLES ###

var tstar integer >=1; # time needed for complete board
var cell{i in 1..n, j in 1..m, t in 1..T} binary; # 0 = not painted, 1 = painted

# State of the robot
var y{t in 1..T} integer >= 0, <= n;
var x{t in 1..T} integer >= 1, <= m;
var color{t in 1..T} binary; # 0 = black, 1 = white
var stock0 {t in 1..T} integer >= 0; # stock of black color
var stock1 {t in 1..T} integer >= 0; # stock of white color

# Actions of the robot, 1 = doing this action
var paint{t in 1..T-1} binary;
var move{t in 1..T-1} binary;
var switch{t in 1..T-1} binary;

### OBJECTIVE ###

minimize cost: tstar;

### CONSTRAINTS ###

subject to BoardComplete:
	exists{t in 1..T} (sum{i in 1..n, j in 1..m} cell[i,j,t] = n*m and t = tstar);
	
subject to OneAction {t in 1..T-1}:
	paint[t] + move[t] + switch[t] <= 1;

subject to NotStandOnPaint {t in 1..T}:
	y[t] >= 1 ==> exists{i in 1..n, j in 1..m} (cell[i,j,t] = 0 and y[t] = i and x[t] = j);

# Initial conditions
subject to InitialY:
	y[1] = 0;
subject to InitialX:
	x[1] = 1;
subject to InitialColor:
	color[1] = 0;
subject to InitialBoard {i in 1..n, j in 1..m}:
	cell[i,j,1] = 0;
subject to InitialStock0:
	stock0[1] = initialStock0;
subject to InitialStock1:
	stock1[1] = initialStock1;

# Cells update
subject to Painting01 {t in 1..T-1}:
 	paint[t] = 1 and y[t] = 0 and x[t] = 1 ==> cell[1,1,t+1] = 1 + cell[1,1,t];
subject to Painting02 {t in 1..T-1}:
 	paint[t] = 1 and y[t] = 0 and x[t] = 2 ==> cell[1,2,t+1] = 1 + cell[1,2,t];
subject to Painting11 {t in 1..T-1}:
 	paint[t] = 1 and y[t] = 1 and x[t] = 1 ==> cell[2,1,t+1] = 1 + cell[2,1,t];
subject to Painting12 {t in 1..T-1}:
 	paint[t] = 1 and y[t] = 1 and x[t] = 2 ==> cell[2,2,t+1] = 1 + cell[2,2,t];
subject to Painting21 {t in 1..T-1}:
 	paint[t] = 1 and y[t] = 2 and x[t] = 1 ==> cell[1,1,t+1] = 1 + cell[1,1,t];
subject to Painting22 {t in 1..T-1}:
 	paint[t] = 1 and y[t] = 2 and x[t] = 2 ==> cell[1,2,t+1] = 1 + cell[1,2,t];
subject to PaintingOthersRemainTheSame {i in 1..n, j in 1..m, t in 1..T-1}:
	paint[t] = 1 and ((y[t] <> i-1 and y[t] <> i+1) or x[t] <> j) ==> cell[i,j,t+1] = cell[i,j,t];
subject to NotPainting {i in 1..n, j in 1..m, t in 1..T-1}:
	paint[t] = 0 ==> cell[i,j,t+1] = cell[i,j,t];

# Position update
subject to Moving {t in 1..T-1}:
	move[t] = 1 ==> abs(y[t+1] - y[t]) + abs(x[t+1] - x[t]) = 1;
subject to NotMoving {t in 1..T-1}:
	move[t] = 0 ==> y[t+1] = y[t] and x[t+1] = x[t];

# Color update
subject to Switching {t in 1..T-1}:
	switch[t] = 1 ==> abs(color[t+1] - color[t]) = 1;
subject to NotSwitching {t in 1..T-1}:
	switch[t] = 0 ==> color[t+1] = color[t];

# Stock update
subject to DecrementStock0 {t in 1..T-1}:
	paint[t] = 1 and color[t] = 0 ==> stock0[t+1] = stock0[t] - 1 and stock1[t+1] = stock1[t];
subject to DecrementStock1 {t in 1..T-1}:
	paint[t] = 1 and color[t] = 1 ==> stock1[t+1] = stock1[t] - 1 and stock0[t+1] = stock0[t];
subject to StockRemainsSame {t in 1..T-1}:
	paint[t] = 0 ==> stock0[t+1] = stock0[t] and stock1[t+1] = stock1[t];

# Respect the pattern
subject to RespectPatternUp {t in 1..T-1}:
	paint[t] = 1 and y[t] <= n-1 ==>
	exists{i in 0..n-1, j in 1..m} (color[t] = pattern[i+1,j] and i = y[t] and j = x[t]);
subject to RespectPatternDown {t in 1..T-1}:
	paint[t] = 1 and y[t] = n ==> exists{j in 1..m} (color[t] = pattern[n-1,j] and j = x[t]);