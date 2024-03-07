import pygame
import math

class Player():
    SPEED = 150
    GRAVITY = 3
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
        movingLeft = keys[pygame.K_LEFT] or keys[pygame.K_a]
        movingRight = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        movingUp = keys[pygame.K_UP] or keys[pygame.K_w]

        #Define dx and dy
        if movingLeft and not movingRight: self.dx = -1
        elif movingRight and not movingLeft: self.dx = 1
        else: self.dx = 0

        #If up arrow and not already in air
        if movingUp and not self.canMoveDown(board): 
            self.dy = -1 * self.JUMP_RATE
            self.yPos -= 1

        #Stop going up if would hit an object
        topOpen, playerTopGrid = self.canMoveUp(board)
        if not topOpen:
            self.dy = 0
            self.yPos = (playerTopGrid + 1) * self.scale_factor + self.level_top

        #Stop going left if would hit an object
        leftOpen, playerLeftGrid = self.canMoveLeft(board)
        if not leftOpen:
            self.dx = max(0, self.dx)
            self.xPos = (playerLeftGrid + 1) * self.scale_factor + self.level_left

        #Stop going right if would hit an object
        rightOpen, playerRightGrid = self.canMoveRight(board)
        if not rightOpen:
            self.dx = min(0, self.dx)
            self.xPos = (playerRightGrid - 2) * self.scale_factor + self.level_left

        #Update dy using gravity    
        if self.canMoveDown(board): self.dy += self.GRAVITY / self.FPS
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
        playerTopGrid = math.floor((self.yPos+ (self.dy * self.SPEED / self.FPS) - self.level_top) / self.scale_factor)
        playerLeftGrid = math.floor((self.xPos - self.level_left) / self.scale_factor)
        playerRightGrid = math.ceil((playerRight - self.level_left) / self.scale_factor)

        #Determine if these are touching the board
        for i in range(playerLeftGrid, playerRightGrid + 1):
            if board[playerTopGrid][i] == "#":
                return False, playerTopGrid
            
        return True, playerTopGrid
    
    #Check if player can move left
    def canMoveLeft(self, board):
        #Calculate bottom of player
        playerBottom = self.yPos + self.scale_factor

        #Convert player coordinates to grid
        playerTopGrid = math.floor((self.yPos - self.level_top) / self.scale_factor)
        playerLeftGrid = math.floor((self.xPos + (self.dx * self.SPEED / self.FPS) - self.level_left) / self.scale_factor)
        playerBottomGrid = math.floor((playerBottom - self.level_top) / self.scale_factor)

        #Determine if these are touching the board
        for i in range(playerTopGrid, playerBottomGrid + 1):
            if board[i][playerLeftGrid] == "#":
                return False, playerLeftGrid
            
        return True, playerLeftGrid
    
    #Check if player can move right
    def canMoveRight(self, board):
        #Calculate bottom of player
        playerBottom = self.yPos + self.scale_factor
        playerRight = self.xPos + self.scale_factor + (self.dx * self.SPEED / self.FPS)

        #Convert player coordinates to grid
        playerTopGrid = math.floor((self.yPos - self.level_top) / self.scale_factor)
        playerBottomGrid = math.floor((playerBottom - self.level_top) / self.scale_factor)
        playerRightGrid = math.ceil((playerRight - self.level_left) / self.scale_factor)

        #Determine if these are touching the board
        for i in range(playerTopGrid, playerBottomGrid + 1):
            if board[i][playerRightGrid] == "#":
                return False, playerRightGrid
            
        return True, playerRightGrid
    
    #Check if player has reached the end of the level
    def atLevelEnd(self, board):
        return self.isTouchingObject(board, "E")
    
    def touchingLava(self, board):
        return self.isTouchingObject(board, "X")
    
    def isTouchingObject(self, board, object):
        #Calculate bottom of player
        playerBottom = self.yPos + self.scale_factor
        playerRight = self.xPos + self.scale_factor

        #Convert player coordinates to grid
        playerTopGrid = math.floor((self.yPos - self.level_top) / self.scale_factor)
        playerBottomGrid = math.floor((playerBottom - self.level_top) / self.scale_factor)
        playerLeftGrid = math.floor((self.xPos - self.level_left) / self.scale_factor)
        playerRightGrid = math.ceil((playerRight - self.level_left) / self.scale_factor)

        #Determine if these are touching the goal
        for i in range(playerTopGrid, playerBottomGrid + 1):
            for j in range(playerLeftGrid, playerRightGrid + 1):
                if board[i][j] == object:
                    return True
        
        return False
