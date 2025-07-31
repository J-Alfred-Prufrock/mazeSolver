import time

class mazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.visited = None
        self.path = []
        self.startX = 0
        self.startY = 0 
        self.endX = self.maze.mazeSizeX - 1
        self.endY = self.maze.mazeSizeY - 1 #index at 0 so -1 to get max
        
    #passes out true if the x and y passed in is the end, false if not
    def goalCheck(self,currentLocationX, currentLocationY):
        if (currentLocationX == self.endX) and (currentLocationY == self.endY):
            print(f"end reached")
            return True
        return False
        
    #passes true if the passed in x and y are inbounds, passes false if out of bounds
    def isPositionValid(self,currentLocationX, currentLocationY):
        if(0<=currentLocationX<self.maze.mazeSizeX) and (0<=currentLocationY<self.maze.mazeSizeY):
            return True
        else:
            return False

    #passes out true if the passed in x and y coords indicate a path, false if wall outof bounds        
    def isWalkable(self,x,y):
        validPosition = self.isPositionValid(x,y)
        if(validPosition == False):
            return False
            
        checkingNode = self.maze.rows[y][x]
        if(checkingNode.property == 0) or (checkingNode.property == 2) or (checkingNode.property == 3):
            # 0 = path, 2= start, 3 = end
            return True
        else:
            return False

    #returns an array of tuples with valid neighbours of the given x and y coords
    def getValidNeighbours(self,x,y):
        checkingNode = self.maze.rows[y][x]
        neighbours = []

        if(checkingNode.right!=-1):
            neighbourX = checkingNode.right
            if self.isWalkable(neighbourX,y) == True:
                neighbours.append((neighbourX,y))

        if(checkingNode.left!=-1):
            neighbourX = checkingNode.left
            if self.isWalkable(neighbourX,y) == True:
                neighbours.append((neighbourX,y))  

        if(checkingNode.up!=-1):
            neighbourY = checkingNode.up
            if self.isWalkable(x,neighbourY) == True:
                neighbours.append((x,neighbourY))

        if(checkingNode.down!=-1):
            neighbourY = checkingNode.down
            if self.isWalkable(x,neighbourY) == True:
                neighbours.append((x,neighbourY))

        return neighbours
   

    def dfs(self):
        startTime = time.time()
        self.visited = [[False for _ in range(self.maze.mazeSizeX)] for _ in range(self.maze.mazeSizeY)]
        self.path = []
        

        result = self.dfsRecursive(self.startX,self.startY)   

     
        endTime = time.time()
        totalTime = endTime - startTime
        print(f"dfs took {totalTime:.4f} seconds")
        return totalTime

    def dfsRecursive(self,currentLocationX,currentLocationY):
        print(f"Exploring position ({currentLocationX}, {currentLocationY})")
        self.visited[currentLocationY][currentLocationX] = True
        print(f"Marked ({currentLocationX}, {currentLocationY}) as visited")
        

        if self.goalCheck(currentLocationX,currentLocationY) == True:
            print("Goal found!")
            return True

        neighbours = self.getValidNeighbours(currentLocationX,currentLocationY)
        print(f"Found {len(neighbours)} neighbors: {neighbours}")
        for neighbourX, neighbourY in neighbours:
            if self.visited[neighbourY][neighbourX] == False:
                if self.dfsRecursive(neighbourX,neighbourY) == True:
                    return True
        print(f"Backtracking from ({currentLocationX}, {currentLocationY})")
        return False


    def bfs(self):
        startTime = time.time()
        self.visited = [[False for _ in range(self.maze.mazeSizeX)] for _ in range(self.maze.mazeSizeY)]
        self.path = []



        endTime = time.time()
        totalTime = endTime - startTime
        print(f"dfs took {totalTime:.4f} seconds")
        return totalTime