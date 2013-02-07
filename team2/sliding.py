import pprint
n = 3
board = dict(((i,j),j*n+i+1) for i in range(n) for j in range(n))
board[(n-1,n-1)] = ' '
for j in range(n):
	for i in range(n):
		print board[(i,j)],
	print