from pymprog import *

begin('gcp')

x, y = var('x,y')

maximize(15*x + 10*y, 'profit')
x <= 3
y <= 4
x + y <= 5

solve()
