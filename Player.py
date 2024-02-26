import pygame
import math

class Player():
    SPEED = 150
    GRAVITY = 0.05
    JUMP_RATE = 3
    level_left, level_top = 0, 0
    scale_factor = 0
    #xPos and yPos are position of top left corner
    xPos, yPos, dx, dy, FPS = 0, 0, 0, 0, 0

    def __init__(self, framerate, startX, startY, lvlLeft, lvlTop, scaleFactor):
        self.FPS = framerate
        self.xPos = startX
        self.yPos = startY
        self.level_left = lvlLeft
        self.level_top = lvlTop
        self.scale_factor = scaleFactor

    #Check for key presses and move
    def updateLocation(self, keys, board):
        #Define dx and dy
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]: self.dx = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]: self.dx = 1
        else: self.dx = 0

        #If up arrow and not already in air
        if keys[pygame.K_UP] and not self.canMoveDown(board): 
            self.dy = -1 * self.JUMP_RATE
            self.yPos -= 1

        #Stop going up if would hit an object
        self.yPos += (self.dy * self.SPEED / self.FPS)
        if not self.canMoveUp(board):
            self.yPos -= (self.dy * self.SPEED / self.FPS)
            self.dy = 0
        else:
            self.yPos -= (self.dy * self.SPEED / self.FPS)

        #Stop going left if would hit an object
        self.xPos += (self.dx * self.SPEED / self.FPS)
        if not self.canMoveLeft(board):
            self.xPos -= (self.dx * self.SPEED / self.FPS)
            self.dx = max(0, self.dx)
        else:
            self.xPos -= (self.dx * self.SPEED / self.FPS)

        #Stop going right if would hit an object
        self.xPos += (self.dx * self.SPEED / self.FPS)
        if not self.canMoveRight(board):
            self.xPos -= (self.dx * self.SPEED / self.FPS)
            self.dx = min(0, self.dx)
        else:
            self.xPos -= (self.dx * self.SPEED / self.FPS)

        #Update dy using gravity    
        if self.canMoveDown(board): self.dy += self.GRAVITY
        else: self.dy = 0

        #Move
        self.xPos += (self.dx * self.SPEED / self.FPS)
        self.yPos += (self.dy * self.SPEED / self.FPS)

    #Return top left pixel
    def getTopLeftPosition(self):
        return (self.xPos, self.yPos)
    
    #Check if player can move down
    def canMoveDown(self, board):
        #Calculate bottom and right sides of player
        playerBottom = self.yPos + self.scale_factor
        playerRight = self.xPos + self.scale_factor

        #Convert player coordinates to grid
        playerBottomGrid = math.floor((playerBottom - self.level_top) / self.scale_factor)
        playerLeftGrid = math.floor((self.xPos - self.level_left) / self.scale_factor)
        playerRightGrid = math.ceil((playerRight - self.level_left) / self.scale_factor)

        #Determine if these are touching the board
        for i in range(playerLeftGrid, playerRightGrid + 1):
            if board[playerBottomGrid + 1][i] == "#":
                self.yPos = (playerBottomGrid - 1) * self.scale_factor + self.level_top
                return False
            
        return True
    
    #Check if player can move up
    def canMoveUp(self, board):
        #Calculate right side of player
        playerRight = self.xPos + self.scale_factor

        #Convert player coordinates to grid
        playerTopGrid = math.floor((self.yPos - self.level_top) / self.scale_factor)
        playerLeftGrid = math.floor((self.xPos - self.level_left) / self.scale_factor)
        playerRightGrid = math.ceil((playerRight - self.level_left) / self.scale_factor)

        #Determine if these are touching the board
        for i in range(playerLeftGrid, playerRightGrid + 1):
            if board[playerTopGrid][i] == "#":
                self.yPos = (playerTopGrid + 1) * self.scale_factor + self.level_top
                return False
            
        return True
    
    #Check if player can move left
    def canMoveLeft(self, board):
        #Calculate bottom of player
        playerBottom = self.yPos + self.scale_factor

        #Convert player coordinates to grid
        playerTopGrid = math.floor((self.yPos - self.level_top) / self.scale_factor)
        playerLeftGrid = math.floor((self.xPos - self.level_left) / self.scale_factor)
        playerBottomGrid = math.floor((playerBottom - self.level_top) / self.scale_factor)

        #Determine if these are touching the board
        for i in range(playerTopGrid, playerBottomGrid + 1):
            if board[i][playerLeftGrid] == "#":
                self.xPos = (playerLeftGrid + 1) * self.scale_factor + self.level_left
                return False
            
        return True
    
    #Check if player can move right
    def canMoveRight(self, board):
        #Calculate bottom of player
        playerBottom = self.yPos + self.scale_factor
        playerRight = self.xPos + self.scale_factor

        #Convert player coordinates to grid
        playerTopGrid = math.floor((self.yPos - self.level_top) / self.scale_factor)
        playerBottomGrid = math.floor((playerBottom - self.level_top) / self.scale_factor)
        playerRightGrid = math.ceil((playerRight - self.level_left) / self.scale_factor)

        #Determine if these are touching the board
        for i in range(playerTopGrid, playerBottomGrid + 1):
            if board[i][playerRightGrid] == "#":
                self.xPos = (playerRightGrid - 2) * self.scale_factor + self.level_left
                return False
            
        return True