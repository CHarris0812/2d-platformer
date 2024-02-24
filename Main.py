import pygame

import Player

PATH_TO_LEVELS = "levels\\"
MAX_FPS = 60
SCALE_FACTOR = 16
LEVEL_BACKGROUND_COLOR = (252, 251, 220)
UNUSED_AREA_COLOR = (0, 0, 0)
OBSTACLE_COLOR = (80, 80, 80)
PLAYER_COLOR = (0, 0, 255)

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
def displayLevel(level):
    #Calculate where to place the level
    level_left = screen_info.current_w // 2 - (level_width * SCALE_FACTOR) // 2
    level_top = screen_info.current_h // 2 - (level_height * SCALE_FACTOR) // 2
    
    #Create surface
    surface = pygame.Surface((screen_info.current_w, screen_info.current_h))

    #Start by filling in whole screen
    surface.fill(UNUSED_AREA_COLOR)

    #Draw board
    for i in range(level_height):
        for j in range(level_width):
            if board[i][j] == ".": pixelColor = LEVEL_BACKGROUND_COLOR
            elif board[i][j] == "#": pixelColor = OBSTACLE_COLOR
            else: pixelColor = (255, 0, 0)

            for k in range(SCALE_FACTOR):
                for l in range(SCALE_FACTOR):
                    surface.set_at((level_left + j * SCALE_FACTOR + k, level_top + i * SCALE_FACTOR + l), pixelColor)

    return surface



if __name__ == "__main__":
    board = generateLevel("test_level.txt")

    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
    clock = pygame.time.Clock()
    running = True

    #Create level surface
    level = displayLevel(board)

    #Create player
    player = Player.Player(MAX_FPS, 600, 600)
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

        #Render screen
        pygame.display.flip()
        #Limit fps
        clock.tick(MAX_FPS)

        


    


# TODO LIST
#
# CRITICAL
# Load level from file
# Display level
# Add player
# Add player movement
# Add gravity
# Add jumping
#
# HIGH
# Add end of level
# Add obstacles
# Create an actual level
#
# MEDIUM
# Add enemies
# Add multiple levels
# Add level selector
#
# LOW
# Add start screen
# Add graphics
# Add sound
#
# ADDITIONAL FEATURES
# Level creator
# Import/export level
# 2 player mode