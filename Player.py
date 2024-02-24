import pygame

class Player():
    SPEED = 100
    GRAVITY = 0.05
    #xPos and yPos are position of top left corner
    xPos, yPos, dx, dy, FPS = 0, 0, 0, 0, 0

    def __init__(self, framerate, startX, startY):
        self.FPS = framerate
        self.xPos = startX
        self.yPos = startY

    #Check for key presses and move
    def updateLocation(self, keys, board):
        #Define dx and dy
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]: self.dx = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]: self.dx = 1
        else: self.dx = 0

        if keys[pygame.K_UP] and self.isOnGround(board): self.dy = -1

        #Update dy using gravity
        if not self.isOnGround(board): self.dy += self.GRAVITY

        #Move
        self.xPos += (self.dx * self.SPEED / self.FPS)
        self.yPos += (self.dy * self.SPEED / self.FPS)

    #Return top left pixel
    def getTopLeftPosition(self):
        return (self.xPos, self.yPos)
    
    #Check if player is on the ground for jumping purposes
    def isOnGround(self, board):
        return True