# Threshold for recipe
param Qo;

# Gem qualities
set Q, dimen 2;


# Items: index, size, profit
set G, dimen 2;

# Workaround
param ref{(i,q) in 1..card(G) cross 1..card(Q)}, symbolic, in G;

param a{G};

# Indices
set I := setof{(i,q) in G} i;
set J := {I,I};

# Decision variables
var x{I}, binary;
var y{J}, binary;

# Objective function
maximize obj:
  sum{(i,q) in G} x[i];

# Constraints
s.t. quality {j in I}:
  sum{(i,q) in G} a[ref[j]]*y[i,j] >= Qo*x[j];
s.t. at_most_one {i in I}:
	sum{(j,q) in G} y[i,j] <= 1;

solve;

printf "Using gems:\n";
printf {(i,q) in G: x[i]== 1} "%i", i;
printf "\n";

data;

# Threshold for recipe
param Qo := 40;

# Items: index, size, profit
set G :=
  1 19
  2 18
  3 17
  4 5;
  
  
set Q :=
	1 1
	2 2
	3 3
	4 4
	5 5
	6 6
	7 7
	8 8
	9 9
	10 10
	11 11
	12 12
	13 13
	14 15
	15 15
	16 16
	17 17
	18 18
	19 19;

end;