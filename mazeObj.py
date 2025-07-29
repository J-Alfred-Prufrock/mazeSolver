from node import node
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import os 

class mazeObj():
    def __init__(self, mazeSizeX, mazeSizeY):
        self.mazeSizeX = mazeSizeX
        self.mazeSizeY = mazeSizeY
        self.outOfBounds = int(-1)
        self.path = int(0)
        self.wall = int(1)
        self.start = int(2)
        self.end = int(3)
        self.cursor = int(4)
        self.rows = []
        self.symbolMap = {
            self.path: ".",
            self.wall: "#",
            self.start: "S",
            self.end: "E"
        }

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

    def saveMazeToFile(self):
        fileName = self.createPopUp()


        if fileName:
            filePath = f"{fileName}.txt"
            
            if os.path.exists(filePath):
                result = messagebox.askyesno("File Exists", f"File '{filePath}' already exists. Overwrite?")

                if not result:
                    print("Save cancelled - file already exists")
                    return

            try:
                with open(f"{fileName}.txt", "w") as f:
                    f.write(f"{self.mazeSizeX}\n")
                    f.write(f"{self.mazeSizeY}\n")

                    for y in range(self.mazeSizeY):
                        rowChars = ""
                        for x in range(self.mazeSizeX):
                            n = self.rows[y][x]
                            rowChars +=self.symbolMap.get(n.property, '?')#adding symbol to the string we write
                        f.write(f"{rowChars}\n")

                    print(f"Maze saved successfully to {fileName}.txt")
            except Exception as e:
                print(f"Error saving file: {e}")
        else:
            print("Save cancelled by user")

    def printMazeTerminalCoords(self):
        print("\nMaze Layout\n")
        for y in range(self.mazeSizeY):
            for x in range(self.mazeSizeX):

                currentNode = self.rows[y][x]
                print(f"[{currentNode.xPosition},{currentNode.yPosition}]",end=" ")
            print()
        print("Where S = start, . = path, # = wall, E = end")  

    def printMazeLayout(self):
        print("\nMaze Layout")
        for y in range(self.mazeSizeY):
            for x in range(self.mazeSizeX):
                n = self.rows[y][x]
                print(f"[{self.symbolMap[n.property]}]", end=" ")
            print()  
        print("Where S = start, . = path, # = wall, E = end")  

    def showMazePopupCoords(self):
        mazePopup = tk.Tk()
        mazePopup.title("Maze Layout")
        
        mazePopup.attributes("-topmost", True) # put on top

        text = tk.Text(mazePopup, font=("Courier", 12)) # creates a textbox evenly spaced, font size 12
        text.pack() # puts the text into the popup

        #loops through to add each row collum
        for y in range(self.mazeSizeY):
            for x in range(self.mazeSizeX):
                n = self.rows[y][x]
                text.insert(tk.END, f"[{n.xPosition},{n.yPosition}] ") #inserts text as position
            text.insert(tk.END, "\n")

        text.insert(tk.END, "Where;\nS = start\n. = path\n# = wall\nE = end")
        mazePopup.mainloop()

    def showMazePopupProperties(self):
        mazePopup = tk.Tk()
        mazePopup.title("Maze Layout")
        
        mazePopup.attributes("-topmost", True) # put on top

        text = tk.Text(mazePopup, font=("Courier", 12)) # creates a textbox evenly spaced, font size 12 and modular size
        text.pack() # puts the text into the popup

        #loops through to add each row collum
        for y in range(self.mazeSizeY):
            for x in range(self.mazeSizeX):
                n = self.rows[y][x]
                text.insert(tk.END, f"[{self.symbolMap[n.property]}] ") #inserts text at position
            text.insert(tk.END, "\n")# gives the space

        text.insert(tk.END, "Where;\nS = start\n. = path\n# = wall\nE = end")
        mazePopup.mainloop()
    
    def openMazeEditor(self): 
        """
        Opens a Tkinter window for editing the maze.
        Allows changing path/wall properties of cells by clicking.
    
        """
        cellSize = 30 #each cell is 30x30 pixels

        #calc canvas dimensions based upon maze size and cell size
        canvasWidth = self.mazeSizeX * cellSize
        canvasHeight = self.mazeSizeY *cellSize

        #Defining colour for each of the properties
        colourMap = {
            self.path: "white",
            self.wall: "black",
            self.start: "green",
            self.end: "red",
            self.cursor: "blue"
        }

        #creating the window
        editorWindow = tk.Tk()
        editorWindow.title("Maze Editor - click to change! wall becomes path, path becomes wall!")
        editorWindow.attributes("-topmost", True)
        
        #create the canvas
        canvas = tk.Canvas(editorWindow, width=canvasWidth, height=canvasHeight, background="lightgray")
        canvas.pack(padx=10, pady=10)# gives canvas space in window

        #now we draw the maze
        def drawMaze():
            canvas.delete("all") # makes sure the canvas is empty

            for y in range(self.mazeSizeY):
                for x in range(self.mazeSizeX):
                    currentNode = self.rows[y][x]

                    #calc pixel coords for current cell
                    #(x0,y0) is top left (x1,y1) is bottom right
                    x0 = x * cellSize
                    y0 = y * cellSize
                    x1 = x0 + cellSize
                    y1 = y0 + cellSize

                    #get the colour based on node property
                    fillColour = colourMap.get(currentNode.property, "grey")#if the property is not in map it goes grey as defualt

                    canvas.create_rectangle(x0,y0,x1,y1, fill=fillColour, outline="black")
        
        #calls drawmaze to draw the maze
        drawMaze()

        def handleCanvasClick(event):
            print(f"Canvas clicked at pixel coordinates: ({event.x}, {event.y})")

            #converts to pixel coords
            clickedX = event.x // cellSize
            clickedY = event.y // cellSize

            if 0<= clickedX < self.mazeSizeX and 0<= clickedY < self.mazeSizeY:
                clickedNode = self.rows[clickedY][clickedX]

                if clickedNode.property == self.wall:
                    clickedNode.property = self.path
                elif clickedNode.property == self.path:
                    clickedNode.property = self.wall
                elif clickedNode.property == self.start:
                    print(f"Cannot change Start node at ({clickedX},{clickedY}).")
                elif clickedNode.property == self.end:
                    print(f"Cannot change End node at ({clickedX},{clickedY}).")
                
                drawMaze()
            else:
                print(f"Clicked outside maze bounds at pixel ({event.x},{event.y}).")

        saveButton = tk.Button(editorWindow, text="Save Maze to new text file", command=self.saveMazeToFile)
        saveButton.pack(pady=10) # Add some vertical padding

        canvas.bind("<Button-1>",handleCanvasClick)

        #start the event loop
        editorWindow.mainloop()

    def createPopUp(self):
        userMazeFileName = None
        popup = tk.Toplevel()
        popup.title("Enter new maze file name")
        popup.geometry("300x150")

        popup.attributes("-topmost", True)  # Always on top
        popup.grab_set()    # Makes popup modal (blocks interaction with other windows)
        popup.focus_set()   # Gives the popup keyboard focus
        popup.lift()        # Brings window to front

        textEntry = tk.Entry(popup, width=30)
        textEntry.pack(pady=20)

        #call this when button
        def getText():
            nonlocal userMazeFileName 
            userMazeFileName = textEntry.get()
            print(f"User entered: {userMazeFileName}")
            popup.destroy()

        okButton = tk.Button(popup, text="OK",command=getText)
        okButton.pack(pady=10)

        popup.wait_window()
        return userMazeFileName

