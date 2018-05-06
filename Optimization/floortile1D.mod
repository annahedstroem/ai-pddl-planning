# Floortile problem
# 1 robot, 1D

### PARAMETERS ###

param n; # nb rows
param T; # time max
param pattern{i in 1..n};
param initialStock0;
param initialStock1;

### VARIABLES ###

var tstar integer >=1; # time needed for complete board
var cell{i in 1..n, t in 1..T} binary; # 0 = not painted, 1 = painted

# State of the robot
var y{t in 1..T} integer >= 0, <= n;
var color{t in 1..T} binary; # 0 = black, 1 = white
var stock0 {t in 1..T} integer >= 0; # stock of black color
var stock1 {t in 1..T} integer >= 0; # stock of white color

# Actions of the robot, 1 = doing this action
var paint{t in 1..T-1} binary;
var move{t in 1..T-1} binary;
var switch{t in 1..T-1} binary;

### OBJECTIVE ###

minimize objective: tstar;

### CONSTRAINTS ###

subject to BoardComplete:
	exists{t in 1..T} (sum{i in 1..n} cell[i,t] = n and t = tstar);
	
subject to OneAction {t in 1..T-1}:
	paint[t] + move[t] + switch[t] <= 1;

subject to NotStandOnPaint {t in 1..T}:
	y[t] >= 1 ==> exists{i in 1..n} (cell[i,t] = 0 and y[t] = i);

# Initial conditions
subject to InitialY:
	y[1] = 0;
subject to InitialColor:
	color[1] = 0;
subject to InitialBoard {i in 1..n}:
	cell[i,1] = 0;
subject to InitialStock0:
	stock0[1] = initialStock0;
subject to InitialStock1:
	stock1[1] = initialStock1;

# Cells update
subject to PaintingY0 {t in 1..T-1}:
 	paint[t] = 1 and y[t] = 0 ==> cell[1,t+1] = 1 + cell[1,t];
subject to PaintingY1 {t in 1..T-1}:
	paint[t] = 1 and y[t] = 1 ==> cell[2,t+1] = 1 + cell[2,t];
subject to PaintingYn {t in 1..T-1}:
	paint[t] = 1 and y[t] = n ==> cell[n-1,t+1] = 1 + cell[n-1,t];
subject to PaintingYinside {t in 1..T-1}:
	paint[t] = 1 and y[t] >= 2 and y[t] <= n-1 ==>
	exists{i in 2..n-1} (cell[i-1,t+1] + cell[i+1,t+1] = 1 + cell[i-1,t] + cell[i+1,t] and i = y[t]);
subject to PaintingOthersRemainTheSame {i in 1..n, t in 1..T-1}:
	paint[t] = 1 and y[t] <> i-1 and y[t] <> i+1 ==> cell[i,t+1] = cell[i,t];
subject to NotPainting {i in 1..n, t in 1..T-1}:
	paint[t] = 0 ==> cell[i,t+1] = cell[i,t];

# Position update
subject to Moving {t in 1..T-1}:
	move[t] = 1 ==> abs(y[t+1] - y[t]) = 1;
subject to NotMovingY {t in 1..T-1}:
	move[t] = 0 ==> y[t+1] = y[t];

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
	paint[t] = 1 and y[t] <= n-1 ==> exists{i in 0..n-1} (color[t] = pattern[i+1] and i = y[t]);
subject to RespectPatternDown {t in 1..T-1}:
	paint[t] = 1 and y[t] = n ==> color[t] = pattern[n-1];
