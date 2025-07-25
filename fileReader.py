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
        for lines in f:
             for i in lines:
                 n = node(xCounter,yCounter,lines[i],mazeWidth,mazeHeight)
                 tempTestArray.insert(node)
        
        f.close()


