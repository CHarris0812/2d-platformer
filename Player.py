import pygame
import math

class Player():
    SPEED = 100
    GRAVITY = 0.05
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

        if keys[pygame.K_UP] and self.isOnGround(board): 
            self.dy = -1
            self.yPos -= 1

        #Update dy using gravity
        if not self.isOnGround(board): self.dy += self.GRAVITY
        else: self.dy = 0

        #Move
        self.xPos += (self.dx * self.SPEED / self.FPS)
        self.yPos += (self.dy * self.SPEED / self.FPS)

    #Return top left pixel
    def getTopLeftPosition(self):
        return (self.xPos, self.yPos)
    
    #Check if player is on the ground for jumping purposes
    def isOnGround(self, board):
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
                return True

        return False