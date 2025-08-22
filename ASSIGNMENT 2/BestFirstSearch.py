class State:
    def __init__(self, row, col, grid):
        self.grid = grid
        self.row = row
        self.col = col
        self.size = len(grid)

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
                children.append(State(newRow, newCol, self.grid))
        return children

    def stepCost(self):
        return 1

    # manhattan distance
    def heuristic(self):
        dx = abs((self.size - 1) - self.row)
        dy = abs((self.size - 1) - self.col)
        return dx + dy


def reconstructPath(parentMap, node):
    path = [node]
    parent = parentMap[node]
    while parent:
        path.append(parent)
        parent = parentMap[parent]

    path = path[::-1]
    print("Reconstructed Path (row, col):")
    for step in path:
        print(f"({step.row}, {step.col})")
    print("GOAL")

    return [(step.row, step.col) for step in path]


def BestFirstSearch(start):
    if start.grid[start.row][start.col] == 1:
        print("-1 (no path exists)")
        return []

    openList = [start]
    closedList = []   
    parentMap = {start: None}

    while openList:
        node = min(openList, key=lambda x: x.heuristic())
        openList.remove(node)

        if node.goalTest():
            return reconstructPath(parentMap, node)

        closedList.append(node)
        for move in node.moveGen():
            if move not in closedList and move not in openList:
                parentMap[move] = node
                openList.append(move)

    return []


grid = [[0, 0, 0],
        [1, 1, 0],
        [1, 1, 0]]

start = State(0, 0, grid)
path = BestFirstSearch(start)
