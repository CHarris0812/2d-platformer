import pygame

class Player():
    SPEED = 100
    #xPos and yPos are position of top left corner
    xPos, yPos, dx, dy, FPS = 0, 0, 0, 0, 0

    def __init__(self, framerate):
        self.FPS = framerate

    #Check for key presses and move
    def updateLocation(self, keys):
        #Define dx and dy
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]: self.dx = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]: self.dx = 1
        else: self.dx = 0

        #Update dy using gravity
        
        #Move
        self.xPos += (self.dx * self.SPEED / self.FPS)
        self.yPos += (self.dy * self.SPEED / self.FPS)
        print(self.dx)

    #Return top left pixel
    def getTopLeftPosition(self):
        return (self.xPos, self.yPos)
    
    