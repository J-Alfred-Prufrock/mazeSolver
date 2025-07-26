from node import node
from mazeObj import mazeObj

path = int(0)
wall = int(1)
start = int(2)
end = int(3)

propertyMap = {
    ".": path,
    "#": wall,
    "S": start,
    "E": end
}


class fileReader():
    def __init__(self):
        pass

    #precondition a maze exists in correct format in file
    #postcondition a maze object is created and passed back out 
    def loadMaze(self, fileName):

        mazeGridChars = []

        
        f = open(fileName+".txt")

        mazeWidth = int(f.readline().strip())
        mazeHeight = int(f.readline().strip())

        tempTestArray = []
        xCounter = 0
        yCounter = 0

        print(mazeWidth,mazeHeight)
        for rawLines in f:
             lines = rawLines.strip()
             for i in range(len(lines)):
                 n = node(xCounter,yCounter,lines[i],mazeWidth,mazeHeight)
                 tempTestArray.append(n)
                 print(n.xPosition,n.yPosition,n.property)
                 xCounter = xCounter+1
             yCounter = yCounter+1
             xCounter = 0
             print("\n")
        
        f.close()


