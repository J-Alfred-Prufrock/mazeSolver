class fileReader():
    def __init__(self, fileName):
        self.fileName = fileName
        f = open(fileName+".txt")
        mazeWidthStr = f.readline().strip()
        mazeHeightStr = f.readline().strip()

        mazeWidth = int(mazeWidthStr)
        mazeHeight = int(mazeHeightStr)
        
        print("Maze Width =",mazeWidth,"Maze Height =",mazeHeight)
        
        f.close()


