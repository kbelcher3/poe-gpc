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
if len(sys.argv) < 2:
    print("Usage: python poe-gcp.py q1 q2 q3 ...\n\n")
    exit(1)

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
    sum(Q[i]*y[i,j] for i in G) >= Q_0 * x[j]


# Objective function
maximize(sum(x[i] for i in G), 'objval')

solve()

# Maximum number of gcp's
num_gcp = int(sum(x[i].primal for i in G))

# Print the solution from stage 1, along with the waste
waste = []

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
    print("Waste: ", max(temp-Q_0,0), end='')
    if temp > Q_0:
        waste.append(temp-Q_0)


print("\nTotal waste: ", sum(waste))

end()


# Stage 2
begin('gcp-2')

# Suppress output
solver(float, msg_lev=glpk.GLP_MSG_OFF)
solver(int, msg_lev=glpk.GLP_MSG_OFF)


# Number of gems made, determined in stage 1
GG = range(num_gcp)


# Decision variables
z = var('z', iprod(G,GG), kind=bool)
w = var('w', GG, kind=int)

# Constraints
for i in G:
    sum(z[i,j] for j in GG) <= 1

for j in GG:
   sum(Q[i]*z[i,j] for i in G) - Q_0 <= w[j]
   sum(Q[i]*z[i,j] for i in G) >= Q_0
   w[j] >= 0

# Objective function
minimize(sum(w[j] for j in GG), 'objval2')

solve()

# Print the solution from stage 2, along with the waste
for j in GG:
    print("")
    temp = 0
    for i in G:
        if z[i,j].primal > 0:
            print(Q[i], end='')
            print(",", end='')
    print(" Waste: ", int(w[j].primal), end='')

print("\n\nTotal waste: ", int(sum(w[j]. primal for j in GG)), "\n")

end()
