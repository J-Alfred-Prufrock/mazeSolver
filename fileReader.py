class fileReader():
    def __init__(self, fileName):
        self.fileName = fileName
        f = open(fileName+".txt")
        mazeWidth = int(f.readline().strip())
        mazeHeight = int(f.readline().strip())

        print(mazeWidth,mazeHeight)
        for lines in f:
             print(lines[1])
        
        f.close()


