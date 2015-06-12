# WARNING!!!!!
#
# BLACK MAGIC MAKES THIS WORK. WE DID NOT WRITE THIS CODE.
# THIS CODE WAS TAKEN FROM GITHUB.
# 
# Accessible at https://github.com/claudioharu/tronB/
#


from itertools import product
from math import sqrt

class AStar:
    def __init__(self, graph):
        self.graph = graph
        
    def heuristic(self, node, start, end):
        raise NotImplementedError
        
    def search(self, start, end):
        openset = set()
        closedset = set()
        current = start
        openset.add(current)
        while openset:
            current = min(openset, key=lambda o:o.g + o.h)
            if current == end:
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                    try:
                        if current == current.parent.parent:
                            break
                    except:
                        pass
                path.append(current)
                return path[::-1]
            openset.remove(current)
            closedset.add(current)
            for node in self.graph[current]:
                if node in closedset:
                    continue
                if node in openset:
                    cost = current.move_cost(node)
                    if cost == 14:
                        continue
                    new_g = current.g + cost
                    if node.g > new_g:
                        node.g = new_g
                        node.parent = current
                else:
                    cost = current.move_cost(node)
                    if cost == 14:
                        continue
                    node.g = current.g + cost
                    node.h = self.heuristic(node, start, end)
                    node.parent = current
                    openset.add(node)
        return None
 
class AStarNode(object):
    def __init__(self):
        self.g = 0
        self.h = 0
        self.parent = None
        
    def move_cost(self, other):
        raise NotImplementedError

class AStarGrid(AStar):
    def heuristic(self, node, start, end):
        return abs(end.x - node.x) + abs(end.y - node.y)
 
class AStarGridNode(AStarNode):
    def __init__(self, x, y):
        self.x, self.y = x, y
        super(AStarGridNode, self).__init__()
 
    def move_cost(self, other):
        diagonal = abs(self.x - other.x) == 1 and abs(self.y - other.y) == 1
        return 14 if diagonal else 10
 
    def __repr__(self):
        return '(%d %d)' % (self.x, self.y)

def make_graph(mapinfo):
    nodes = [[AStarGridNode(x, y) for y in range(mapinfo['height'])] for x in range(mapinfo['width'])]
    graph = {}
    for x, y in product(range(mapinfo['width']), range(mapinfo['height'])):
        node = nodes[x][y]
        graph[node] = []
        for i, j in product([-1, 0, 1], [-1, 0, 1]):
            if not (0 <= x + i < mapinfo['width']): continue
            if not (0 <= y + j < mapinfo['height']): continue
            if [x+i,y+j] in mapinfo['obstacle']: continue
            graph[nodes[x][y]].append(nodes[x+i][y+j])
    return graph, nodes
