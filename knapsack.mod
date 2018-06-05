# Threshold for recipe
param Q;

# Items: index, size, profit
set G, dimen 2;

# Indices
set I := setof{(i,q) in G} i;

# Assignment
var x{I}, binary;

minimize obj :
  sum{(i,q) in G} x[i];

s.t. size :
  sum{(i,q) in G} q*x[i] >= Q;

solve;

printf "Using gems:\n";
printf {(i,q) in I: x[i]== 1} "%i", i;
printf "\n";

data;

# Threshold for recipe
param Q := 40;

# Items: index, size, profit
set G :=
  1 19
  2 18
  3 17
  4 5;
  

end;