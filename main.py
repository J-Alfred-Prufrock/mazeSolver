from node import node
import tkinter as tk
from tkinter import scrolledtext
from fileReader import fileReader
from mazeObj import mazeObj 
from algorithms import mazeSolver


outOfBounds = int(-1)
path = int(0)
wall = int(1)
start = int(2)
end = int(3)
cursor = int(4)

rows= []

userMaze = None

symbolMap = {
    path: ".",
    wall: "#",
    start: "S",
    end: "E"
}

def main():
    global userMaze
    print("Hello welcome to maze solver printer thing idk")
    choice = int(input("Would you like to create your own maze or select a pre made maze?\n1: Create own Maze\n2: Select premade maze\n"))
    if choice == 1:
        userMaze = createMaze()
    if choice == 2:
        userMaze = loadMadeFromFile()
    
    displayMaze(userMaze)
    
    


#precondition user has premade maze files on their computer in same directory as the code
#postcondition maze is loaded from file and inserted into the array and returned into main
def loadMadeFromFile():
    tempMaze = None
    mazeName = str(input("What is the name of the text file your maze is located in?\n"))
    if mazeName == "a":
        mazeName = "premadeMaze1"
    elif mazeName == "b":
        mazeName = "premadeMaze2"

    fileReaderClass = fileReader()
    tempMaze = fileReaderClass.loadMaze(mazeName)
    #tempMaze.printMazeTerminalCoords()
    #tempMaze.showMazePopupProperties()
    #tempMaze.printMazeLayout()
    #tempMaze.showMazePopupCoords()
    return tempMaze

def createMaze():
    done = False
    tempMaze = None
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
    
    tempMaze = mazeObj(mazeSizeX,mazeSizeY)
    tempMaze.createMaze()
    return tempMaze

def displayMaze(userMaze):
    choice = int(input("How would you like the maze to be displayed?\n1: Printed in commandline as coordiantes\n2: Printed in commandline as properties (walls/floors)\n3: Printed in a popup as coordiantes\n4: Displayed in a pop-up as properties (walls/floors)\n"))
    if choice == 1:
        userMaze.printMazeTerminalCoords()
    elif choice == 2:
        userMaze.printMazeLayout()
    elif choice == 3:
        userMaze.showMazePopupCoords()
    elif choice == 4:
        userMaze.showMazePopupProperties()
    elif choice== 5:
        userMaze.openMazeEditor()
    elif choice == 6:
        pass


main()

testMaze = loadMadeFromFile()
solver = mazeSolver(testMaze)

test = solver.dfs()



