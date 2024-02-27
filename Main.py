import pygame
import time

import Player

PATH_TO_LEVELS = "levels\\"
MAX_FPS = 60
SCALE_FACTOR = 16
LEVEL_BACKGROUND_COLOR = (252, 251, 220)
UNUSED_AREA_COLOR = (0, 0, 0)
OBSTACLE_COLOR = (80, 80, 80)
PLAYER_COLOR = (0, 0, 255)
UNKNOWN_COLOR = (255, 0, 0)
END_COLOR = (50, 255, 50)

level_width, level_height = 0, 0
screen_info = 0

#Load level file and generate board from it
#param level: filename
#return: array of chars representing level
def generateLevel(level):
    global level_width, level_height
    board = []
    f = open(PATH_TO_LEVELS + level)
    for line in f:
        board.append(list(line.replace("\n", "")))
    level_width = len(board[0])
    level_height = len(board)
    return board

#Display level represented as array using pygame
#param level: array of level
#param screen: pygame display
#return: pygame surface
def displayLevel(level_left, level_top):
    #Create surface
    surface = pygame.Surface((screen_info.current_w, screen_info.current_h))

    #Start by filling in whole screen
    surface.fill(UNUSED_AREA_COLOR)

    #Draw board
    for i in range(level_height):
        for j in range(level_width):
            if board[i][j] == ".": pixelColor = LEVEL_BACKGROUND_COLOR
            elif board[i][j] == "#": pixelColor = OBSTACLE_COLOR
            elif board[i][j] == "E": pixelColor = END_COLOR
            else: pixelColor = UNKNOWN_COLOR

            for k in range(SCALE_FACTOR):
                for l in range(SCALE_FACTOR):
                    surface.set_at((level_left + j * SCALE_FACTOR + k, level_top + i * SCALE_FACTOR + l), pixelColor)

    return surface

#Ends game once player has succeeded
def endLevel(screen):
    #Load end of level images
    levelEnd = pygame.image.load(".\\resources\\Level_complete.png").convert()
    mainMenu = pygame.image.load(".\\resources\\Main_menu.png").convert()
    playAgain = pygame.image.load(".\\resources\\Play_again.png").convert()

    #Display screen
    screen_info = pygame.display.Info()
    levelEnd = pygame.transform.scale(levelEnd, (screen_info.current_w, screen_info.current_h))
    screen.blit(levelEnd, (0, 0))
    screen.blit(mainMenu, (screen_info.current_w // 2 - screen_info.current_w // 3, screen_info.current_h // 2 + screen_info.current_h // 6))
    screen.blit(playAgain, (screen_info.current_w // 2 + screen_info.current_w // 3 - playAgain.get_width(), screen_info.current_h // 2 + screen_info.current_h // 6))

    #Render
    pygame.display.flip()
    time.sleep(5)
    exit()


if __name__ == "__main__":
    board = generateLevel("test_level.txt")

    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
    clock = pygame.time.Clock()
    running = True

    #Create level surface
    level_left = screen_info.current_w // 2 - (level_width * SCALE_FACTOR) // 2
    level_top = screen_info.current_h // 2 - (level_height * SCALE_FACTOR) // 2
    level = displayLevel(level_left, level_top)

    #Create player
    player = Player.Player(MAX_FPS, 600, 600, level_left, level_top, SCALE_FACTOR)
    playerSurface = pygame.Surface((SCALE_FACTOR * 2, SCALE_FACTOR * 2))
    playerSurface.fill(PLAYER_COLOR)

    while running:
        #Check if x has been pressed. If so, exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Display level
        screen.blit(level, (0, 0))

        #Update and display player
        keys = pygame.key.get_pressed()
        player.updateLocation(keys, board)
        screen.blit(playerSurface, player.getTopLeftPosition())

        #Check if player has reached end
        if player.atLevelEnd(board):
            endLevel(screen)

        #Render screen
        pygame.display.flip()
        #Limit fps
        clock.tick(MAX_FPS)

        


    


# TODO LIST
#
# HIGH
# Add end of level
# Create an actual level
#
# MEDIUM
# Add enemies
# Add multiple levels
# Add level selector
# Add success screen at end of level
#
# LOW
# Make character not jittery
# Add start screen
# Add graphics
# Add sound
#
# ADDITIONAL FEATURES
# Level creator
# Import/export level
# 2 player mode