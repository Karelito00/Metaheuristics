from sortedcontainers import SortedList
import math

MAX_VALUE = int(1e9)
TRANS_X = [0, 0, 1, 1, 1, -1, -1, -1]
TRANS_y = [1, -1, 0, 1, -1, 0, 1, -1]

class Node:
    # g is the distance from the source to the Node
    # h is the value of the heuristic(Euclidean in this case) from 
    #   the Node to the target
    # f = g + h
    # parent_y and parent_x is for build the path :)
    def __init__(self, y, x):
        self.f = MAX_VALUE
        self.g = 0
        self.y = y
        self.x = x
        self.parent_y = -1

    def __lt__(self, other):
        return self.f > other.f

# we use the Euclidean distance because we can move in eight directions
def euclidean(ay, ax, by, bx):
    return math.sqrt((ay - by)**2 + (ax - bx)**2)

def get_path(matrix, y, x):
    path = [(y, x)]
    while(matrix[y][x].parent_y != -1):
        y, x = matrix[y][x].parent_y, matrix[y][x].parent_x
        path.append((y, x))
    
    return path

def A_star(n, m, matrix, sx, sy, tx, ty):
    open_list = SortedList()

    assert(sy >= 0 and sy < n and sx >= 0 and sx < m)
    assert(ty >= 0 and ty < n and tx >= 0 and tx < m)

    arr = [[Node(i, j) for j in range(m)] for i in range(n)]
    mark_closed = [[False for j in range(m)] for i in range(n)]

    arr[sy][sx].f = 0
    open_list.add(arr[sy][sx])

    while(len(open_list) > 0):
        q = open_list.pop()
        mark_closed[q.y][q.x] = True

        for i in range(8):
            # move transition
            cy, cx = q.y + TRANS_y[i], q.x + TRANS_X[i]
            if(cy < 0 or cy >= n or cx < 0 or cx >= m or matrix[cy][cx] == "b"):
                continue
            
            # Stop de algorithm if the target is found 
            if(cy == ty and cx == tx):
                arr[cy][cx].parent_y, arr[cy][cx].parent_x = q.y, q.x
                # build the path
                return get_path(arr, cy, cx)
            
            # if the successor has better f value than nf then we can't improve the 
            # solution with it, otherwise put it in our sorted list
            if(mark_closed[cy][cx] == False):
                ng = q.g + 1.0
                nh = euclidean(cy, cx, ty, tx)
                nf = ng + nh
                
                if(arr[cy][cx].f > nf):
                    arr[cy][cx].f = nf
                    arr[cy][cx].g = ng
                    arr[cy][cx].parent_y, arr[cy][cx].parent_x = q.y, q.x
                    open_list.add(arr[cy][cx])

    # path not found
    return None

# input n, m - matrix dimensions
# b - blocked cell
# * - free cell
# s - source
# t - target
n, m = [int(x) for x in input().split()]

mat = [['0' for j in range(m)] for i in range(n)]
# input example
"""
4 7
s * b * * * *
* * * * * * *
* * b b * * t
* * * * * * *
"""
sx, sy, tx, ty = -1, -1, -1, -1
for i in range(n):
    j = 0
    for c in input().split():
        assert(j < m)
        mat[i][j] = str(c)
        
        if(mat[i][j] == "s"):
            sy, sx = i, j
        if(mat[i][j] == "t"):
            ty, tx = i, j
        
        j += 1

path = A_star(n, m, mat, sx, sy, tx, ty)
if(path is None):
    print("Path not found")
else:
    print(path[::-1])