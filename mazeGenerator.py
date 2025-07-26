from node import node
import tkinter as tk
from tkinter import scrolledtext
from fileReader import fileReader


outOfBounds = int(-1)
path = int(0)
wall = int(1)
start = int(2)
end = int(3)

rows= []
collums = []

symbolMap = {
    path: ".",
    wall: "#",
    start: "S",
    end: "E"
}

def main():
    print("Hello welcome to maze solver printer thing idk")
    choice = int(input("Would you like to create your own maze or select a pre made maze?\n1: Create own Maze\n2: Select premade maze\n"))
    if choice == 1:
        printMaze()
    if choice == 2:
        loadMadeFromFile("premadeMaze1")

def printMaze():
    done = False
    while(done == False):
        try:
            mazeSizeX = int(input("what would you like the width of the maze to be?\n"))
            done = True
        except:
            print("please enter an integer")
            done = False

    done = False
    while done == False:
        try:
            mazeSizeY = int(input("what would you like the height of the maze to be?\n"))
            done = True
        except:
            print("please enter an integer")
            done = False

    print(f"Making {mazeSizeX}x{mazeSizeY} maze")

    for y in range(mazeSizeY):
        row = []
        for x in range(mazeSizeX):
            if x == 0 and y == 0:
                n = node(x, y, start, mazeSizeX, mazeSizeY)
            elif x== mazeSizeX-1 and y == mazeSizeY-1:
                n = node(x, y, end, mazeSizeX, mazeSizeY)
            else:
                n = node(x, y, path, mazeSizeX, mazeSizeY)
            row.append(n)
        rows.append(row)
        
    choice = int(input("How would you like the maze to be displayed?\n1: Printed in terminal as walls, paths, start and exit\n2: Printed in terminal as [x,y] coordinates\n3: In a pop-up box as walls, paths, start and exit\n4: In a pop-up box as [x,y] coordinates\n5: Open maze editor\n6: Read from file (currently hardcoded to premadeMaze1)\n"))
    if choice == 1:
        printMazeLayout()
    elif choice == 2:
        printMazeCoords()
    elif choice == 3:
        showMazePopupProperties()
    elif choice == 4:
        showMazePopupCoords()
    elif choice== 5:
        openMazeEditor()
    elif choice == 6:
        pass

def loadMadeFromFile(fileName):
    fileName = "premadeMaze1" # stub
    m = fileReader(fileName)

def showMazePopupCoords():
    mazePopup = tk.Tk()
    mazePopup.title("Maze Layout")
    
    mazePopup.attributes("-topmost", True) # put on top

    text = tk.Text(mazePopup, font=("Courier", 12)) # creates a textbox evenly spaced, font size 12
    text.pack() # puts the text into the popup

    #loops through to add each row collum
    for y in range(mazeSizeY):
        for x in range(mazeSizeX):
            n = rows[y][x]
            text.insert(tk.END, f"[{n.xPosition},{n.yPosition}] ") #inserts text as position
        text.insert(tk.END, "\n")

    text.insert(tk.END, "Where;\nS = start\n. = path\n# = wall\nE = end")
    mazePopup.mainloop()

def openMazeEditor():
    def renderMaze():
        text.config(state="normal")  # Temporarily make it editable so we can update
        text.delete("1.0", tk.END)
        for y in range(mazeSizeY):
            for x in range(mazeSizeX):
                n = rows[y][x]
                text.insert(tk.END, f"[{symbolMap[n.property]}] ")
            text.insert(tk.END, "\n")
        text.insert(tk.END, "Where;\nS = start\n. = path\n# = wall\nE = end")
        text.config(state="disabled")  # Lock the text area to prevent user edits


    def getCoordinates():
        try:
            coords = coord_entry.get().split(",")
            x, y = int(coords[0]), int(coords[1])
            if 0 <= x < mazeSizeX and 0 <= y < mazeSizeY:
                return x, y
            else:
                text.insert(tk.END, f"\nInvalid coordinates: ({x},{y}) out of bounds.\n")
                return None
        except Exception as e:
            text.insert(tk.END, f"\nError reading coordinates: {e}\n")
            return None

    def setWall():
        coords = getCoordinates()
        if coords:
            x, y = coords
            if rows[y][x].property not in (start, end):  # don't overwrite start/end
                rows[y][x].property = wall
                renderMaze()

    def setPath():
        coords = getCoordinates()
        if coords:
            x, y = coords
            if rows[y][x].property not in (start, end):
                rows[y][x].property = path
                renderMaze()

    # Create popup
    mazePopup = tk.Tk()
    mazePopup.title("Maze Layout")
    mazePopup.attributes("-topmost", True)

    # Entry + buttons
    coord_label = tk.Label(mazePopup, text="Enter coord in form x,y")
    coord_label.pack()
    coord_entry = tk.Entry(mazePopup)
    coord_entry.pack()

    # Buttons side by side
    button_frame = tk.Frame(mazePopup)
    button_frame.pack()

    wall_btn = tk.Button(button_frame, text="Make Wall", command=setWall)
    wall_btn.grid(row=0, column=0, padx=5)

    path_btn = tk.Button(button_frame, text="Make Path", command=setPath)
    path_btn.grid(row=0, column=1, padx=5)


    # Text area
    text = tk.Text(mazePopup, font=("Courier", 12))
    text.pack()

    renderMaze()
    mazePopup.mainloop()


def showMazePopupProperties():
    mazePopup = tk.Tk()
    mazePopup.title("Maze Layout")
    
    mazePopup.attributes("-topmost", True) # put on top

    text = tk.Text(mazePopup, font=("Courier", 12)) # creates a textbox evenly spaced, font size 12 and modular size
    text.pack() # puts the text into the popup

    #loops through to add each row collum
    for y in range(mazeSizeY):
        for x in range(mazeSizeX):
            n = rows[y][x]
            text.insert(tk.END, f"[{symbolMap[n.property]}] ") #inserts text at position
        text.insert(tk.END, "\n")# gives the space

    text.insert(tk.END, "Where;\nS = start\n. = path\n# = wall\nE = end")
    mazePopup.mainloop()

def printMazeLayout():
    print("\nMaze Layout")
    for y in range(mazeSizeY):
        for x in range(mazeSizeX):
            n = rows[y][x]
            print(f"[{symbolMap[n.property]}]", end=" ")
        print()  
    print("Where S = start, . = path, # = wall, E = end")  

def printMazeCoords():
    print("\nMaze Layout")
    for y in range(mazeSizeY):
        for x in range(mazeSizeX):
            n = rows[y][x]
            print(f"[{n.xPosition},{n.yPosition}]", end=" ")
        print()  
    print("Where S = start, . = path, # = wall, E = end")  





main()



