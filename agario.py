##################################################################
# Authors: Lindsey Engel and Steven Hill
# Group 17 for software engineering capstone
# Latest version: 3.3.0
##################################################################
# The imports used in the software
# All imports are 1.0.0v other than webbrowser and os which is 2.2.0v
# webbrowser and os is used in the how to play button

import math
import os
import pygame
import random
import sys
import time
import webbrowser
from pygame.locals import *

pygame.init()
###################################################################
# These are the global at are used for the game code version 1.0.0

# screen // set size to a default size that is not full windowed
screen_width = 1280
screen_height = 780
SCREEN = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Game window title
pygame.display.set_caption("AGAR.IO")

# FPSCounter assets
frame_per_second = 30
GAMECLOCK = pygame.time.Clock()

# food // size 2000 is a size we found fitting for map size
food_balls = 2000

# max bots // size 20 is a size we found fitting for map size
bot_max = 20

# max bad squares // size 100 is a size we found fitting for map size
bad_sqrt_max = 100

# map size // we found this to be a good map size that does not lag bad for the size it is.
map_size = 3000

# player attributes
player_size = 10
player_color = (255, 0, 0)

# bot attributes
bot_min_size = 10
bot_max_size = 100

# screen background
screen_color = (0, 0, 0)
text_color = (255, 255, 255)
bad_sqrt_color = (5, 235, 16)
FONT = pygame.font.Font("freesansbold.ttf", 32)
TITLEFONT = pygame.font.Font("freesansbold.ttf", 40)
SMALLFONT = pygame.font.Font("freesansbold.ttf", 20)

# size
WIDTH = screen_width
HEIGHT = screen_height

# list
balls = []
bots = []
bad_sqrts = []

game_over = False


#############################################################
# FPS assets 3.2.0
start_time = 0
frame_rate = 30
ticks = 0
##############################################################

##############################################################
# This was a added fix to make sure the game does not crash
# from mouse movement
# 1.1.1v

# mouse position globals
mouse_x = WIDTH / 2
mouse_y = HEIGHT / 2


###############################################################

###############################################################
# This is the class used to draw and handle functions in the game
# 1.0.0v

class Create:
    # This is the stored values used for object that use this class.
    def __init__(self, x, y, color, size, name):
        self.name = name
        self.size = size
        self.color = color
        self.status = random.randint(1, 8)
        self.xPos = x
        self.yPos = y

    # This is the bot movement function. Makes the movement random.
    # This is what self.status is for.
    def bot_movement(self):
        so_random = random.randint(1, round(self.size))
        if so_random == 1:
            self.status = random.randint(1, 8)
        if self.status == 1:
            self.yPos += 300 / self.size
        elif self.status == 2:
            self.xPos += 300 / self.size
        elif self.status == 3:
            self.xPos += 150 / self.size
            self.yPos += 150 / self.size
        elif self.status == 4:
            self.xPos += 150 / self.size
            self.yPos -= 150 / self.size
        elif self.status == 5:
            self.xPos -= 150 / self.size
            self.yPos += 150 / self.size
        elif self.status == 6:
            self.xPos -= 150 / self.size
            self.yPos -= 150 / self.size
        elif self.status == 7:
            self.yPos -= 300 / self.size
        elif self.status == 8:
            self.yPos -= 300 / self.size

    # This function handles when any collision happens and determines if
    # eating should happen.
    def collision(self, player):
        global balls, bots, bad_sqrts, game_over
        # This is for player checking to eat foodballs
        for ball in balls:
            if math.sqrt(((player.xPos - (WIDTH / 2) + ball.xPos) ** 2 + (player.yPos - (
                    HEIGHT / 2) + ball.yPos) ** 2)) <= ball.size + player.size and ball.size <= player.size:
                balls.remove(ball)
                # This sets the growth size after player eats a ball
                player.size += 0.25
                # This will respawn balls
                new_ball = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                                  (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5, "Ball")
                balls.append(new_ball)

        ################################################################################################################
        # This is part of the collision for an add feature in the version 3.1.0v
        # bad square decreases size when eaten for the player
        for bad_sqrt in bad_sqrts:
            if math.sqrt(((player.xPos - (WIDTH / 2) + bad_sqrt.xPos) ** 2 + (player.yPos - (
                    HEIGHT / 2) + bad_sqrt.yPos) ** 2)) <= bad_sqrt.size + player.size and bad_sqrt.size <= player.size:
                bad_sqrts.remove(bad_sqrt)

                # This sets the takes size after bot eats a ball
                player.size -= 1

                # This will respawn bad sqrts and size change in 3.1.1v
                new_sqrt = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                                  bad_sqrt_color, 20, "sqrt")
                bad_sqrts.append(new_sqrt)
        ################################################################################################################

        # This is for player checking to eat bots
        for bot in bots:
            if math.sqrt(((player.xPos - (WIDTH / 2) + bot.xPos) ** 2 + (player.yPos - (
                    HEIGHT / 2) + bot.yPos) ** 2)) <= bot.size + player.size and bot.size * 1.05 <= player.size:
                bot_size = math.pi * (bot.size ** 2)
                player_size = math.pi * (player.size ** 2)
                new_size = math.sqrt((bot_size + player_size) / math.pi)
                player.size += new_size - player.size
                bots.remove(bot)
                # This will respawn bots
                new_bot = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                                 (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                 random.randint(bot_min_size, bot_max_size), "bot")
                bots.append(new_bot)

            # This is for bot checking to eat the player
            elif math.sqrt(((player.xPos - (WIDTH / 2) + bot.xPos) ** 2 + (player.yPos - (
                    HEIGHT / 2) + bot.yPos) ** 2)) <= bot.size + player.size and bot.size >= player.size * 1.05:
                bot_size = math.pi * (bot.size ** 2)
                player_size = math.pi * (player.size ** 2)
                new_size = math.sqrt((bot_size + player_size) / math.pi)
                bot.size += new_size - player.size
                game_over = True
            else:
                # This is for bot checking to eat bots
                for eatBot in bots:
                    if math.sqrt((eatBot.xPos - bot.xPos) ** 2 + (
                            eatBot.yPos - bot.yPos) ** 2) <= bot.size and bot.size >= eatBot.size * 1.05:
                        bots.remove(eatBot)
                        bot_size = math.pi * (bot.size ** 2)
                        eat_bot_size = math.pi * (eatBot.size ** 2)
                        new_size = math.sqrt((bot_size + eat_bot_size) / math.pi)
                        bot.size += new_size - bot.size

                        # This will respawn bots
                        new_bot = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                                         (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                         random.randint(bot_min_size, bot_max_size), "bot")
                        bots.append(new_bot)
                # This is for bot checking to eat foodballs
                for ball in balls:
                    if math.sqrt(((bot.xPos - ball.xPos) ** 2 + (
                            bot.yPos - ball.yPos) ** 2)) <= ball.size + bot.size and ball.size <= bot.size:
                        balls.remove(ball)

                        # This sets the growth size after bot eats a ball
                        bot.size += 0.25

                        # This will respawn balls
                        new_ball = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                                          (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5,
                                          "Ball")
                        balls.append(new_ball)
                ########################################################################################################
                # This is part of the collision for an add feature in the 3.1.0v
                # bad square decreases size when eaten for the player
                for bad_sqrt in bad_sqrts:
                    if math.sqrt(((bot.xPos - bad_sqrt.xPos) ** 2 + (
                            bot.yPos - bad_sqrt.yPos) ** 2)) <= bad_sqrt.size + bot.size and bad_sqrt.size <= bot.size:
                        bad_sqrts.remove(bad_sqrt)

                        # This sets the takes size after bot eats a ball
                        bot.size -= 1

                        # This will respawn bad sqrts and size change in 3.1.1v
                        new_sqrt = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                                          bad_sqrt_color, 20, "sqrt")
                        bad_sqrts.append(new_sqrt)
            ############################################################################################################

    # This draws the object of the balls, bots, and player.
    def draw(self, surface, x, y):
        # This args was added to help with drawing squares
        if self.name != "sqrt":
            # draws the circles for all that are circles
            pygame.draw.circle(surface, self.color, (x, y), int(self.size))
            if self.name == "bot" or self.name == "player":
                message = FONT.render(str(round(self.size)), False, text_color)

                # This centers the bot and player size in the middle of them.
                SCREEN.blit(message, (x - 17.5, y - 12.5))
        else:
            # This draws the squares 3.1.0v
            pygame.draw.rect(surface, self.color, (x, y, int(self.size), int(self.size)))


#################################################################################################
#################################################################################################
# This is the menu method; part of 2.0.0v
# The "if game_over" is part of 2.1.0v
# The instruction_button is part of 2.2.0v
# Added code to text and stand_ins is [art pf 2.3.0v

def menu(game_over=False):
    global start_game
    if game_over:
        start_button_text = FONT.render("Play Again", True, (29, 104, 242))
        quit_button_text = FONT.render("Quit", True, (247, 87, 87))
        instruction_button_text = FONT.render("Game Instruction", True, (126, 242, 63))
        title = TITLEFONT.render("Game over you lost", True, text_color)

    else:
        start_button_text = FONT.render("Start", True, (29, 104, 242))
        quit_button_text = FONT.render("Quit", True, (247, 87, 87))
        instruction_button_text = FONT.render("How To Play", True, (126, 242, 63))
        title = TITLEFONT.render("Welcome to Agar.io!", True, text_color)

    # Define button dimensions including the desired border width
    button_width = 500
    button_height = 150
    border_width = 100

    # Define top border dimensions
    top_border_height = 80

    # Gives default structure to the buttons
    start_button_rect = pygame.Rect(500, 300, button_width, button_height)
    quit_button_rect = pygame.Rect(500, 420, button_width, button_height)
    instruction_button_rect = pygame.Rect(500, 540, button_width, button_height)

    # This is used to give some background details to the menu
    stand_ins = []
    for c in range(30):
        new_stand_in = Create(random.randint(-100, 1000), random.randint(-100, 1000),
                              (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                              random.randint(10, 50), "stand_in")
        stand_ins.append(new_stand_in)

    # Start of the menu loop
    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    start_game = True
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                elif instruction_button_rect.collidepoint(mouse_pos):
                    webbrowser.open_new_tab('file:///' + os.getcwd() + '/' + 'Manual.html')
        # This is used for the menu getting resized.
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        # This is to fill the screen color
        SCREEN.fill(screen_color)

        # To draw in the background details on the screen
        for stand_in in stand_ins:
            stand_in.draw(SCREEN, stand_in.xPos, stand_in.yPos)

        # Define top border rectangle
        top_border_rect = pygame.Rect(0, 0, WIDTH, top_border_height)

        # Draw the top border rectangle (buttons)
        pygame.draw.rect(SCREEN, (25, 25, 25), top_border_rect)
        pygame.draw.rect(SCREEN, (25, 25, 28), start_button_rect, border_width)
        pygame.draw.rect(SCREEN, (25, 25, 28), quit_button_rect, border_width)
        pygame.draw.rect(SCREEN, (25, 25, 28), instruction_button_rect, border_width)

        # Set up the buttons to be centered whenever screen is resized
        title_rect = title.get_rect(center=(WIDTH / 2, (HEIGHT / 2) - 200))
        start_button_rect = start_button_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        quit_button_rect = quit_button_text.get_rect(center=(WIDTH / 2, (HEIGHT / 2) + 200))
        instruction_button_rect = instruction_button_text.get_rect(center=(WIDTH / 2, (HEIGHT / 2) + 100))

        # Draws buttons and title to screen
        SCREEN.blit(start_button_text, start_button_rect)
        SCREEN.blit(quit_button_text, quit_button_rect)
        SCREEN.blit(instruction_button_text, instruction_button_rect)
        SCREEN.blit(title, title_rect)

        # to let the player know what version they are on.
        version_message = SMALLFONT.render("3.3.0v", True, text_color)
        SCREEN.blit(version_message, (0, HEIGHT - 30))

        # Updates display
        pygame.display.update()

    return start_game

start_game = menu(game_over=False)

######################################################################################
######################################################################################
# This is the start of the game. The game loop is inside the "if start_game"
# The start_game is part of the menu version so that mean it 2.0.0v
# everything else is 1.0,0v
if start_game:

    # creates the foodBalls on the screen.
    # random.randint(0,255) is give you the values for RGB.
    for i in range(food_balls):
        new_ball = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                          (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5, "ball")
        balls.append(new_ball)
    # create the bots on the screen
    for i in range(bot_max):
        new_bot = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                         (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                         random.randint(bot_min_size, bot_max_size), "bot")
        bots.append(new_bot)
    # creates the bad_sqrt on screen
    for i in range(bad_sqrt_max):  # and size change in 3.1.1v
        new_sqrt = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                          bad_sqrt_color, 20, "sqrt")
        bad_sqrts.append(new_sqrt)

    # to create the player.
    player = Create(0, 0, player_color, player_size, "player")

    # game loop starts here
    while True:
        for event in pygame.event.get():
            # to exit the game by the windows close button.
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    #####################################################################
    # This is add in 2.4.0v and 2.4.1v
    # This adds more menu features
            # Takes you back to the main menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                start_game = menu(game_over=False)
            # Takes you to the game over menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                game_over = True
    ######################################################################
            # This is check Mouse x and y so that we can track the mouse for player movement
            if event.type == MOUSEMOTION and game_over == False:
                mouse_x, mouse_y = event.pos
            else:  # This prevents errors
                mouse_x = WIDTH / 2
                mouse_y = HEIGHT / 2
        ######################################################################################
        # Part of the code here had a fix. player.pos change from 5.
        # and bots on the map. 1.2.0v

        # Keeps check of collisions
        if not game_over:
            player.collision(player)

            # map bound checks
            if player.xPos >= map_size + (WIDTH / 2):
                player.xPos = map_size + (WIDTH / 2) - 10
            elif player.xPos <= -map_size + (WIDTH / 2):
                player.xPos = -map_size + (WIDTH / 2) + 10
            else:
                player.xPos += round(-((mouse_x - (WIDTH / 2)) / player.size / 2))

            if player.yPos >= map_size + (HEIGHT / 2):
                player.yPos = map_size + (HEIGHT / 2) - 10
            elif player.yPos <= -map_size + (HEIGHT / 2):
                player.yPos = -map_size + (HEIGHT / 2) + 10
            else:
                player.yPos += round(-((mouse_y - (HEIGHT / 2)) / player.size / 2))

        # for drawing the foodballs
        for ball in balls:
            ball.draw(SCREEN, ball.xPos + player.xPos, ball.yPos + player.yPos)
        # for drawing the bad_sqrts
        for bad_sqrt in bad_sqrts:
            bad_sqrt.draw(SCREEN, bad_sqrt.xPos + player.xPos, bad_sqrt.yPos + player.yPos)
        # for drawing the bots and setting bounds
        for bot in bots:
            bot.draw(SCREEN, bot.xPos + player.xPos, bot.yPos + player.yPos)
            bot.bot_movement()
            if bot.xPos >= map_size:
                bot.xPos = map_size - 10
            elif bot.xPos <= -map_size:
                bot.xPos = -map_size + 10
            if bot.yPos >= map_size:
                bot.yPos = map_size - 10
            elif bot.yPos <= -map_size:
                bot.yPos = -map_size + 10
        ##################################################################################
        # 1.1.0v was changed after 2.1.0v. That changed the layout of the game over text
        # as well as what the player see on the game over screen.
        # For drawing player and handling game over message
        if game_over:
            start_game = menu(game_over=True)
            if start_game:
                balls = []  # reset objects that were in previous game
                bots = []
                bad_sqrts = []

                # creates the foodBalls on the screen again.
                # random.randint(0,255) is give you the values for RGB.
                for i in range(food_balls):
                    new_ball = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                                      (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 5,
                                      "ball")
                    balls.append(new_ball)
                # create the bots on the screen again.
                for i in range(bot_max):
                    new_bot = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                                     (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                     random.randint(bot_min_size, bot_max_size), "bot")
                    bots.append(new_bot)
                # creates the bad_sqrt on screen again.
                for i in range(bad_sqrt_max):  # and size change in 3.1.1v
                    new_sqrt = Create(random.randint(-map_size, map_size), random.randint(-map_size, map_size),
                                      bad_sqrt_color, 20, "sqrt")
                    bad_sqrts.append(new_sqrt)

                # to create the player again.
                player = Create(0, 0, player_color, player_size, "player")

                game_over = False
                # game loop continues over again with FPS being right
                start_time = time.time()

        else:
            player.draw(SCREEN, WIDTH / 2, HEIGHT / 2)
            # keeping track of this will create the illusion that our player is moving when ready everything else is.
            player.xPos += round(-((mouse_x - (WIDTH / 2)) / player.size / 2))
            player.yPos += round(-((mouse_y - (HEIGHT / 2)) / player.size / 2))

    ############################################################################################
        # FPS
        ticks += 1
        if frame_rate > 20:
            message = FONT.render("Frame Speed: " + str(frame_rate), False, (55, 255, 55))
            SCREEN.blit(message, (10, 10))
        elif 20 >= frame_rate > 10:
            message = FONT.render("Frame Speed: " + str(frame_rate), False, (255, 255, 55))
            SCREEN.blit(message, (10, 10))
        elif 10 >= frame_rate > 0:
            message = FONT.render("Frame Speed: " + str(frame_rate), False, (255, 55, 55))
            SCREEN.blit(message, (10, 10))
        if (time.time() - start_time) > 0.5:
            frame_rate = round(ticks / (time.time() - start_time))
            ticks = 0
            start_time = time.time()
    ############################################################################################

        # For the information to the player
        advice = SMALLFONT.render("Press m on keyboard to go back to main menu "
                                  "or press k on keyboard to reset the game", False, text_color)
        SCREEN.blit(advice, (0, HEIGHT - 30))
        # Just like the menu, this is used to keep everything running during resizing the screen.
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        # Updates display
        pygame.display.update()
        # set frames for game
        GAMECLOCK.tick(frame_per_second)
        # Set screen background
        SCREEN.fill(screen_color)

#######################################################################################################
#######################################################################################################
