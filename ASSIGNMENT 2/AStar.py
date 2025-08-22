class State:
    def __init__(self, row, col, grid, cost):
        self.grid = grid
        self.row = row
        self.col = col
        self.size = len(grid)
        self.gCost = cost  

    def goalTest(self):
        return self.row == self.size - 1 and self.col == self.size - 1

    def moveGen(self):
        children = []
        dr = [-1, 1, 0, 0, -1, 1, -1, 1]
        dc = [0, 0, -1, 1, 1, -1, -1, 1]
        for k in range(8):
            newRow = self.row + dr[k]
            newCol = self.col + dc[k]
            if 0 <= newRow < self.size and 0 <= newCol < self.size and self.grid[newRow][newCol] == 0:
                children.append(State(newRow, newCol, self.grid, self.gCost + 1))
        return children

    def stepCost(self):
        return 1

    # Manhattan distance
    def heuristic(self):
        dx = abs((self.size - 1) - self.row)
        dy = abs((self.size - 1) - self.col)
        return dx + dy


def reconstructPath(parentMap, node, gCostMap, fCostMap):
    path = [node]
    parent = parentMap[node]
    while parent:
        path.append(parent)
        parent = parentMap[parent]

    path = path[::-1]  
    print("Reconstructed Path with g, h, f values:")

    for step in path:
        print(f"({step.row}, {step.col}) -> g = {gCostMap[step]}, h = {step.heuristic()}, f = {fCostMap[step]}")
    print("GOAL")

    return path


def propagateImprovement(node, gCostMap, fCostMap, parentMap, closedList):
    for move in node.moveGen():
        step = move.stepCost()
        newg = step + gCostMap[node]
        if newg < gCostMap.get(move, float('inf')):
            parentMap[move] = node
            gCostMap[move] = newg
            fCostMap[move] = gCostMap[move] + move.heuristic()
            if move in closedList:
                propagateImprovement(move, gCostMap, fCostMap, parentMap, closedList)


def AStar(start):
    if start.grid[start.row][start.col] == 1:
        print("-1 (no path exists)")
        return []

    openList = [start]
    closedList = []
    parentMap = {start: None}
    gCostMap = {start: 0}
    fCostMap = {start: gCostMap[start] + start.heuristic()}

    while openList:
        node = min(openList, key=lambda x: fCostMap.get(x, float('inf')))
        openList.remove(node)

        if node.goalTest():
            return reconstructPath(parentMap, node, gCostMap, fCostMap)
        else:
            closedList.append(node)
            for move in node.moveGen():
                step = move.stepCost()
                newg = step + gCostMap[node]
                if newg < gCostMap.get(move, float('inf')):
                    parentMap[move] = node
                    gCostMap[move] = newg
                    fCostMap[move] = gCostMap[move] + move.heuristic()
                    if move in closedList:
                        propagateImprovement(move, gCostMap, fCostMap, parentMap, closedList)
                    elif move not in openList:
                        openList.append(move)
    return []


grid = [
    [0, 0, 0],
    [1, 1, 0],
    [1, 1, 0]
]

start = State(0, 0, grid, 0)
path = AStar(start)
