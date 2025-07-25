from node import node

class fileReader():
    def __init__(self, fileName):
        self.fileName = fileName
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


