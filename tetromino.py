# Library imports
import pygame

# Tetris block class
from core_component import window, gameboard

# Tetromino class
class Tetromino:

    # Constructor
    def __init__(self):
        self.col = 0                 # Column location of Tetromino
        self.row = 0                 # Row location of Tetrmino
        self.coloffset = 0           # The column offset of the self.shape list
        self.type = "O"              # Official names are I, J, L, O, S, T, Z
        self.rot = 1                 # Current rotation (1, 2, 3, 4) (90, 180, 270, 360)
        self.color = 0               # Color (1 - aqua, 2 - blue, 3 - orange 4 - yellow, 5 - green, 6 - purple, 7 - red)
        self.shape = [[0, 1, 1, 0],
                      [0, 1, 1, 0],  # Representation of current block in memory
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.placed = False         # Is current block placed

    # Gathers the indexes of all four sub blocks needed to make up one Tetromino
    def getindex(self):
        index = []
        indexcol = []
        indexrow = []
        indexcoloffset = []
        for i in range(0, 4):
            for j in range(0, 4):
                if self.shape[i][j] == 1:
                    index.append(i)
                    index.append(j)
                    indexcol.append(j)
                    indexrow.append(i)
        for j in range(1, 8, 2):
                indexcoloffset.append(index[j] - min(indexcol))
                index[j] = index[j] - min(indexcol)
        for j in range(0, 7, 2):
                index[j] = index[j] - min(indexrow)
        self.coloffset = max(indexcoloffset)    # Determines the offset of the self.shape list
        return index

    # Draw subblocks
    def drawsubblocks(self, r, g, b, o):
        index = self.getindex()
        if not self.placed:
            pygame.draw.rect(window, (r, g, b), ((index[1]+self.col) * 40, (index[0]+self.row) * 40, 40, 40), o)
            pygame.draw.rect(window, (r, g, b), ((index[3]+self.col) * 40, (index[2]+self.row) * 40, 40, 40), o)
            pygame.draw.rect(window, (r, g, b), ((index[5]+self.col) * 40, (index[4]+self.row) * 40, 40, 40), o)
            pygame.draw.rect(window, (r, g, b), ((index[7]+self.col) * 40, (index[6]+self.row) * 40, 40, 40), o)

    # Draws the current block in play
    def drawcurrent(self, gameboard):
        if not self.placed:
            if self.color == 1:
                self.drawsubblocks(122, 216, 239, 0)
                self.drawsubblocks(0, 0, 0, 1)
            elif self.color == 2:
                self.drawsubblocks(47, 100, 214, 0)
                self.drawsubblocks(0, 0, 0, 1)
            elif self.color == 3:
                self.drawsubblocks(255, 182, 0, 0)
                self.drawsubblocks(0, 0, 0, 1)
            elif self.color == 4:
                self.drawsubblocks(255, 255, 153, 0)
                self.drawsubblocks(0, 0, 0, 1)
            elif self.color == 5:
                self.drawsubblocks(0, 255, 127, 0)
                self.drawsubblocks(0, 0, 0, 1)
            elif self.color == 6:
                self.drawsubblocks(84, 0, 255, 0)
                self.drawsubblocks(0, 0, 0, 1)
            elif self.color == 7:
                self.drawsubblocks(255, 58, 58, 0)
                self.drawsubblocks(0, 0, 0, 1)

    # Sets the gameboard 2d list to 1 where the current block has landed
    def drawplaced(self, gamebard):
        if self.placed:
            index = self.getindex()
            gameboard[(index[0] + self.row)][(index[1] + self.col)] = self.color
            gameboard[(index[2] + self.row)][(index[3] + self.col)] = self.color
            gameboard[(index[4] + self.row)][(index[5] + self.col)] = self.color
            gameboard[(index[6] + self.row)][(index[7] + self.col)] = self.color

    # Checks if there is a block below the current controlled Tetromino
    def checkcollisionbelow(self, gameboard):
        index = self.getindex()
        if (gameboard[index[0]+self.row+1][index[1]+self.col] >= 1):
                    self.placed = True
                    return True
        elif (gameboard[index[2] + self.row + 1][index[3] + self.col] >= 1):
                self.placed = True
                return True
        elif (gameboard[index[4] + self.row + 1][index[5] + self.col] >= 1):
                self.placed = True
                return True
        elif (gameboard[index[6] + self.row + 1][index[7] + self.col] >= 1):
                self.placed = True
                return True
        else:
            return False

    # Checks if Tetromino is able to move right
    def checkcollisionright(self, gameboard):
        index = self.getindex()
        if (gameboard[index[0]+self.row][index[1]+self.col+1] >= 1):
                return False
        elif (gameboard[index[2] + self.row][index[3] + self.col+1] >= 1):
                return False
        elif (gameboard[index[4] + self.row][index[5] + self.col+1] >= 1):
                return False
        elif (gameboard[index[6] + self.row][index[7] + self.col+1] >= 1):
                return False
        else:
            return True

    # Checks if Tetromino is able to move left
    def checkcollisionleft(self, gameboard):
        index = self.getindex()
        if (gameboard[index[0]+self.row][index[1]+self.col-1] >= 1):
                return False
        elif (gameboard[index[2] + self.row][index[3] + self.col-1] >= 1):
                return False
        elif (gameboard[index[4] + self.row][index[5] + self.col-1] >= 1):
                return False
        elif (gameboard[index[6] + self.row][index[7] + self.col-1] >= 1):
                return False
        else:
            return True

    # Move left
    def moveleft(self, gameboard):
        index = self.getindex()
        if not self.placed:
            if (index[1] + self.col + self.coloffset >= 0) and (index[3] + self.col + self.coloffset >= 0) and(index[5] + self.col + self.coloffset >= 0) and (index[7] + self.col + self.coloffset >= 0):
                if self.checkcollisionleft(gameboard):
                    if self.col > 0:
                        self.col -= 1

    # Move right
    def moveright(self, gameboard):
        index = self.getindex()
        if not self.placed:
            if (index[1] + self.col + self.coloffset <= 9):
                if self.checkcollisionright(gameboard):
                    if self.col < 9:
                        self.col += 1
            elif self.type == "L" and self.rot == 4:
                if self.col <= 6:
                    self.col += 1

    # Default shapes of all seven Tetromino
    def setshape(self, type):
        if type == "I":
            self.type = type
            self.color = 1
            self.shape = [[0, 1, 0, 0],
                          [0, 1, 0, 0],
                          [0, 1, 0, 0],
                          [0, 1, 0, 0]]
        elif type == "J":
            self.type = type
            self.color = 2
            self.shape = [[0, 1, 1, 0],
                          [0, 1, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 0]]
        elif type == "L":
            self.type = type
            self.color = 3
            self.shape = [[0, 1, 0, 0],
                          [0, 1, 0, 0],
                          [0, 1, 1, 0],
                          [0, 0, 0, 0]]
        elif type == "O":
            self.type = type
            self.color = 4
            self.shape = [[0, 1, 1, 0],
                          [0, 1, 1, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]
        elif type == "S":
            self.type = type
            self.color = 5
            self.shape = [[0, 1, 1, 0],
                          [1, 1, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]
        elif type == "T":
            self.type = type
            self.color = 6
            self.shape = [[1, 1, 1, 0],
                          [0, 1, 0, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]
        elif type == "Z":
            self.type = type
            self.color = 7
            self.shape = [[1, 1, 0, 0],
                          [0, 1, 1, 0],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]

    # Increases / decreases the current rotation value
    def setrotate(self):
        if self.rot == 4:
            self.rot = 1
        else:
            self.rot += 1

    # Handles all rotations and rotation edge cases (Ex. Where Tetrominos are unable to rotate)
    def rotate(self, gameboard):
        index = self.getindex()
        if not self.checkcollisionbelow(gameboard):
            # Edge cases (Ex. "I" piece against wall)
                if self.type == "J" and gameboard[index[3]+self.row][index[4]+self.col+1] == 1 and self.rot == 1:
                    self.col -= 1
                    self.setrotate()
                elif self.type == "J" and gameboard[index[3]+self.row][index[4]+self.col] == 1 and self.rot == 3:
                    print("do nothing")
                elif self.type == "Z" and gameboard[index[0]+self.row][index[1]+self.col+1] == 1 and (self.rot == 4 or self.rot == 2):
                    self.col -= 1
                    self.setrotate()
                elif self.type == "T" and gameboard[index[0]+self.row][index[1]+self.col+1] == 1 and (self.rot == 2):
                    print ("do nothing T")
                elif self.type == "T" and gameboard[index[0]+self.row][index[1]+self.col+2] == 1 and (self.rot == 4):
                    self.col -= 1
                    self.setrotate()
                elif self.type == "S" and gameboard[index[0]+self.row][index[1]+self.col+2] == 1 and (self.rot == 2 or self.rot == 4):
                    self.col -= 1
                    self.setrotate()
                elif self.type == "L" and gameboard[index[0]+self.row][index[1]+self.col+2] == 1 and (self.rot == 3):
                    print ("do nothing L")
                elif self.type == "L" and gameboard[index[0]+self.row][index[1]+self.col+2] == 1 and (self.rot == 1):
                    self.col -= 1
                    self.setrotate()
                elif self.type == "I" and gameboard[index[0]+self.row][index[1]+self.col+2] == 1 and (self.rot == 1 or self.rot == 3):
                    print ("do nothing I")
                elif self.type == "I" and gameboard[index[0]+self.row][index[1]+self.col+3] == 1 and (self.rot == 1 or self.rot == 3):
                    self.col -= 1
                    self.setrotate()
                elif self.type == "I" and index[0]+self.row <= 20 and (self.rot == 2 or self.rot == 4):
                    if gameboard[index[0]+self.row+3][index[1]+self.col] == 1:
                        print ("do nothing I2")
                    else:
                        self.setrotate()
                else:
                    self.setrotate()

                # Common rotations
                # "I" piece rotations
                if self.rot == 1 and self.type == "I":
                    self.shape = [[0, 1, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 1, 0, 0]]
                elif self.rot == 2 and self.type == "I":
                    self.shape = [[0, 0, 0, 0],
                                  [0, 0, 0, 0],
                                  [1, 1, 1, 1],
                                  [0, 0, 0, 0]]
                elif self.rot == 3 and self.type == "I":
                    self.shape = [[0, 0, 1, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 1, 0]]
                elif self.rot == 4 and self.type == "I":
                    self.shape = [[0, 0, 0, 0],
                                  [1, 1, 1, 1],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]

                # "J" piece rotations
                if self.rot == 1 and self.type == "J":
                    self.shape = [[0, 1, 1, 0],
                                  [0, 1, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 2 and self.type == "J":
                    self.shape = [[1, 1, 1, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 3 and self.type == "J":
                    self.shape = [[0, 1, 0, 0],
                                  [0, 1, 0, 0],
                                  [1, 1, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 4 and self.type == "J":
                    self.shape = [[1, 0, 0, 0],
                                  [1, 1, 1, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]

                # "L" piece rotations
                if self.rot == 1 and self.type == "L":
                    self.shape = [[0, 1, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 1, 1, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 2 and self.type == "L":
                    self.shape = [[1, 1, 1, 0],
                                  [1, 0, 0, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 3 and self.type == "L":
                    self.shape = [[1, 1, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 4 and self.type == "L":
                    self.shape = [[0, 0, 1, 0],
                                  [1, 1, 1, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]

                # "O" piece rotations
                if self.rot >= 1 and self.type == "O":
                    self.shape = [[0, 1, 1, 0],
                                  [0, 1, 1, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]

                # "S" piece rotations
                if self.rot == 1 and self.type == "S":
                    self.shape = [[0, 1, 1, 0],
                                  [1, 1, 0, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 2 and self.type == "S":
                    self.shape = [[0, 1, 0, 0],
                                  [0, 1, 1, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 3 and self.type == "S":
                    self.shape = [[0, 1, 1, 0],
                                  [1, 1, 0, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 4 and self.type == "S":
                    self.shape = [[1, 0, 0, 0],
                                  [1, 1, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 0, 0]]

                # "T" piece rotations
                if self.rot == 1 and self.type == "T":
                    self.shape = [[1, 1, 1, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 2 and self.type == "T":
                    self.shape = [[0, 1, 0, 0],
                                  [1, 1, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 3 and self.type == "T":
                    self.shape = [[0, 1, 0, 0],
                                  [1, 1, 1, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 4 and self.type == "T":
                    self.shape = [[1, 0, 0, 0],
                                  [1, 1, 0, 0],
                                  [1, 0, 0, 0],
                                  [0, 0, 0, 0]]

                # "Z" piece rotations
                if self.rot == 1 and self.type == "Z":
                    self.shape = [[1, 1, 0, 0],
                                  [0, 1, 1, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 2 and self.type == "Z":
                    self.shape = [[0, 1, 0, 0],
                                  [1, 1, 0, 0],
                                  [1, 0, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 3 and self.type == "Z":
                    self.shape = [[1, 1, 0, 0],
                                  [0, 1, 1, 0],
                                  [0, 0, 0, 0],
                                  [0, 0, 0, 0]]
                elif self.rot == 4 and self.type == "Z":
                    self.shape = [[0, 1, 0, 0],
                                  [1, 1, 0, 0],
                                  [1, 0, 0, 0],
                                  [0, 0, 0, 0]]
