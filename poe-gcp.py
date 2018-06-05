from pymprog import *
import sys

# Create model
begin('gcp')

# Suppress output
solver(float, msg_lev=glpk.GLP_MSG_OFF)
solver(int, msg_lev=glpk.GLP_MSG_OFF)

# Vendor recipe threshold
Q_0 = 40

# Read qualities as command-line arguments
Q = [int(arg) for arg in sys.argv[1:]]

# Number of gems
N = len(Q)

# Index set
G = range(N)


# Decision variables
x = var('x', G, kind=bool)
y = var('y', iprod(G,G), kind=bool)

# Constraints
for i in G:
    sum(y[i,j] for j in G) <= 1

for j in G:
    sum(Q[j]*y[i,j] for i in G) >= Q_0 * x[j]

# Objective function
maximize(sum(x[i] for i in G), 'objval')

solve()

num_gcp = int(sum(x[i].primal for i in G))
waste = []

print("\nNumber of GCP's: ", num_gcp)


for j in G:
    if int(x[j].primal) == 0:
        continue
    print("")
    temp = 0
    for i in G:
        if y[i,j].primal > 0:
            print(Q[i], end='')
            print(", ", end='')
            temp += Q[i]
    print("Waste: ", max(temp-Q_0,0))
    if temp > Q_0:
        waste.append(temp-Q_0)


print("\nTotal waste: ", sum(waste))

end()
