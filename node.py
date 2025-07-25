class node:
    def __init__(self, xPosition, yPosition, property, mazeXSize, mazeYSize):
        self.xPosition = xPosition
        self.yPosition = yPosition
        self.property = property #path = 0, wall = 1, start = 2, end = 3
        
        #initalise neighbours, -1 means none
        self.right = (-1)
        self.left = (-1)
        self.up = (-1)
        self.down = (-1)


        if(mazeXSize > xPosition > 0 ):
            self.left = xPosition - 1
        else:
            self.left = (-1)

        if 0 <= xPosition < (mazeXSize-1):
            self.right = xPosition + 1
        else:
            self.right = (-1)



