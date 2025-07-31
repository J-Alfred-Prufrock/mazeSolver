import time
import tkinter as tk
from tkinter import scrolledtext

class mazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.visited = None
        self.path = []
        self.startX = 0
        self.startY = 0 
        self.dfsSteps = []
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
        #print(f"node neighbours right-{checkingNode.right}, left - {checkingNode.left}, up- {checkingNode.up}, down - {checkingNode.down} and postion{x},{y}")
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
   
    #the main recursive dfs algorithm
    def dfsRecursive(self, visualize=False):
        startTime = time.time()
        self.visited = [[False for _ in range(self.maze.mazeSizeX)] for _ in range(self.maze.mazeSizeY)]
        self.path = []
        self.dfsSteps = []
        
        result = self.dfsRecursiveCall(self.startX,self.startY, visualize)   


     
        endTime = time.time()
        totalTime = endTime - startTime
        elapsedTime = totalTime * 1000
        print(f"Recursive dfs took {elapsedTime:.6f} miliseconds")

        if visualize == True:
            self.visualizeDFS()
            

        return totalTime

    #the recursive call to dfs
    def dfsRecursiveCall(self,currentLocationX,currentLocationY, collectSteps=False):
        print(f"Exploring position ({currentLocationX}, {currentLocationY})")
        self.visited[currentLocationY][currentLocationX] = True
        print(f"Marked ({currentLocationX}, {currentLocationY}) as visited")

        if collectSteps == True:
            neighbours = self.getValidNeighbours(currentLocationX, currentLocationY)
            self.dfsSteps.append(((currentLocationX, currentLocationY), "exploring", neighbours))



        if self.goalCheck(currentLocationX,currentLocationY) == True:
            print("Goal found!")
            if collectSteps == True:
                self.dfsSteps.append(((currentLocationX, currentLocationY), "goal_found", None))
            return True

        neighbours = self.getValidNeighbours(currentLocationX,currentLocationY)
        print(f"Found {len(neighbours)} neighbors: {neighbours}")
        for neighbourX, neighbourY in neighbours:
            if self.visited[neighbourY][neighbourX] == False:

                if self.dfsRecursiveCall(neighbourX,neighbourY,collectSteps) == True:
                    return True
        print(f"Backtracking from ({currentLocationX}, {currentLocationY})")
        if collectSteps == True:
            self.dfsSteps.append(((currentLocationX, currentLocationY), "backtracking", None))
        return False


    def visualizeDFS(self):
        """
        Opens a Tkinter window to visualize the DFS algorithm results.
        """
        cellSize = 30
        borderThickness = 15
        
        # Calculate canvas dimensions
        canvasWidth = self.maze.mazeSizeX * cellSize + (2 * borderThickness)
        canvasHeight = self.maze.mazeSizeY * cellSize + (2 * borderThickness)
        
        # Color map for visualization
        colourMap = {
            0: "white",      # path
            1: "black",      # wall
            2: "green",      # start
            3: "red",        # end
            "visited": "lightblue",
            "current": "yellow",
            "backtrack": "orange",
            "final_path": "lime"
        }
        
        # Create the visualization window
        dfsWindow = tk.Tk()
        dfsWindow.title("DFS Algorithm Visualization")
        dfsWindow.attributes("-topmost", True)
        
        # Create canvas
        canvas = tk.Canvas(dfsWindow, width=canvasWidth, height=canvasHeight, background="lightgray")
        canvas.pack(padx=10, pady=10)
        
        # Status label
        statusLabel = tk.Label(dfsWindow, text="Ready to visualize DFS", font=("Arial", 12))
        statusLabel.pack(pady=5)
        
        # Control variables
        currentStep = 0
        isPlaying = False
        animationSpeed = 500
        visited = set()
        
        def drawMaze(specialNodes=None):
            """Draw the maze with special highlighting"""
            canvas.delete("all")
            canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill="", outline="black", width=borderThickness)
            
            for y in range(self.maze.mazeSizeY):
                for x in range(self.maze.mazeSizeX):
                    currentNode = self.maze.rows[y][x]
                    
                    # Calculate pixel coordinates
                    x0 = x * cellSize + borderThickness
                    y0 = y * cellSize + borderThickness
                    x1 = x0 + cellSize
                    y1 = y0 + cellSize
                    
                    # Determine color
                    fillColour = "grey"  # default
                    
                    if specialNodes and (x, y) in specialNodes:
                        fillColour = colourMap.get(specialNodes[(x, y)], "grey")
                    else:
                        fillColour = colourMap.get(currentNode.property, "grey")
                    
                    canvas.create_rectangle(x0, y0, x1, y1, fill=fillColour, outline="black")
        
        def updateVisualization():
            """Update the visualization based on current step"""
            nonlocal currentStep
            if currentStep >= len(self.dfsSteps):
                statusLabel.config(text="DFS Complete!")
                return
            
            position, action, extra = self.dfsSteps[currentStep]
            x, y = position
            
            # Create special nodes dict for coloring
            specialNodes = {}
            
            # Color all previously visited nodes
            for pos in visited:
                if pos != position:
                    specialNodes[pos] = "visited"
            
            # Color current position based on action
            if action == "exploring":
                visited.add(position)
                specialNodes[position] = "current"
                statusLabel.config(text=f"Exploring position ({x}, {y})")
            elif action == "backtracking":
                specialNodes[position] = "backtrack"
                statusLabel.config(text=f"Backtracking from ({x}, {y})")
            elif action == "goal_found":
                specialNodes[position] = "final_path"
                statusLabel.config(text=f"Goal found at ({x}, {y})!")
            
            drawMaze(specialNodes)
            stepLabel.config(text=f"Step: {currentStep + 1} / {len(self.dfsSteps)}")
        
        def playAnimation():
            """Play the DFS animation automatically"""
            nonlocal isPlaying, currentStep
            
            if not isPlaying or currentStep >= len(self.dfsSteps):
                isPlaying = False
                playButton.config(text="Play")
                return
            
            updateVisualization()
            currentStep += 1
            
            # Schedule next step
            dfsWindow.after(animationSpeed, playAnimation)
        
        def togglePlay():
            """Toggle play/pause"""
            nonlocal isPlaying
            isPlaying = not isPlaying
            
            if isPlaying:
                playButton.config(text="Pause")
                playAnimation()
            else:
                playButton.config(text="Play")
        
        def nextStep():
            """Go to next step manually"""
            nonlocal currentStep
            if currentStep < len(self.dfsSteps):
                updateVisualization()
                currentStep += 1
        
        def prevStep():
            """Go to previous step manually"""
            nonlocal currentStep, visited
            if currentStep > 0:
                currentStep -= 1
                # Rebuild visited set up to current step
                visited = set()
                for i in range(currentStep):
                    pos, action, _ = self.dfsSteps[i]
                    if action == "exploring":
                        visited.add(pos)
                updateVisualization()
                stepLabel.config(text=f"Step: {currentStep + 1} / {len(self.dfsSteps)}")
        
        def reset():
            """Reset to beginning"""
            nonlocal currentStep, isPlaying, visited
            currentStep = 0
            isPlaying = False
            visited = set()
            playButton.config(text="Play")
            drawMaze()
            statusLabel.config(text="Ready to visualize DFS")
            stepLabel.config(text=f"Step: 0 / {len(self.dfsSteps)}")
        
        def changeSpeed():
            """Change animation speed"""
            nonlocal animationSpeed
            if animationSpeed == 500:
                animationSpeed = 200
                speedButton.config(text="Speed: Fast")
            elif animationSpeed == 200:
                animationSpeed = 100
                speedButton.config(text="Speed: Very Fast")
            else:
                animationSpeed = 500
                speedButton.config(text="Speed: Normal")
        
        # Control buttons
        buttonFrame = tk.Frame(dfsWindow)
        buttonFrame.pack(pady=10)
        
        playButton = tk.Button(buttonFrame, text="Play", command=togglePlay, bg="lightgreen")
        playButton.pack(side=tk.LEFT, padx=5)
        
        prevButton = tk.Button(buttonFrame, text="← Prev", command=prevStep, bg="lightblue")
        prevButton.pack(side=tk.LEFT, padx=5)
        
        nextButton = tk.Button(buttonFrame, text="Next →", command=nextStep, bg="lightblue")
        nextButton.pack(side=tk.LEFT, padx=5)
        
        resetButton = tk.Button(buttonFrame, text="Reset", command=reset, bg="lightcoral")
        resetButton.pack(side=tk.LEFT, padx=5)
        
        speedButton = tk.Button(buttonFrame, text="Speed: Normal", command=changeSpeed, bg="lightyellow")
        speedButton.pack(side=tk.LEFT, padx=5)
        
        # Step counter
        stepLabel = tk.Label(dfsWindow, text=f"Step: 0 / {len(self.dfsSteps)}", font=("Arial", 10))
        stepLabel.pack()
        
        # Legend
        legendFrame = tk.Frame(dfsWindow)
        legendFrame.pack(pady=5)
        
        tk.Label(legendFrame, text="Legend:", font=("Arial", 10, "bold")).pack()
        legendText = "Yellow: Current | Light Blue: Visited | Orange: Backtracking | Green: Start | Red: End"
        tk.Label(legendFrame, text=legendText, font=("Arial", 8)).pack()
        
        # Initial draw
        drawMaze()
        
        # Start the event loop
        dfsWindow.mainloop()




    #not implemneted yet
    def bfs(self):
        startTime = time.time()
        self.visited = [[False for _ in range(self.maze.mazeSizeX)] for _ in range(self.maze.mazeSizeY)]
        self.path = []



        endTime = time.time()
        totalTime = endTime - startTime
        print(f"dfs took {totalTime:.4f} seconds")
        return totalTime