from node import node

class mazeObj():
    def __init__(self, mazeSizeX, mazeSizeY):
        self.mazeSizeX = mazeSizeX
        self.mazeSizeY = mazeSizeY
        self.outOfBounds = int(-1)
        self.path = int(0)
        self.wall = int(1)
        self.start = int(2)
        self.end = int(3)
        self.rows = []
        pass

    def createMaze(self):
        for y in range(self.mazeSizeY):
            currentRowNodes = []
            for x in range(self.mazeSizeX):
                if x == 0 and y == 0:
                    n = node(x, y, self.start, self.mazeSizeX, self.mazeSizeY)
                elif x== self.mazeSizeX-1 and y == self.mazeSizeY-1:
                    n = node(x, y, self.end, self.mazeSizeX, self.mazeSizeY)
                else:
                    n = node(x, y, self.path, self.mazeSizeX, self.mazeSizeY)
                currentRowNodes.append(n)
            self.rows.append(currentRowNodes)
    
    def addFromFile(self, mazeArray):
        self.rows = mazeArray
        pass