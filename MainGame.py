import pygame
import random
import pickle  # pickle is used for high score saving

pygame.init()

# Color definitions
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

# Game property constants
block_size = 20
display_width = 800
display_height = 600
boundX = display_width - (block_size * 2)
boundY = display_height - (block_size * 2)
scoreOffsetX = 140
scoreOffsetY = 27
scoreBoundWidth = display_width - 180
scoreBoundHeight = 100 - block_size

FPS = 12

# Game variables
degrees = 270
randAppleX, randAppleY = (0,) * 2
goldenApple = random.randint(1, 10) == 10
lead_x = display_width / 2
lead_y = display_height / 2
lead_x_change = block_size
lead_y_change = 0
appleCounter = 0
highScore = 0
snakeList = []

# Importing font
bodyFont = pygame.font.SysFont("comicsansms", 50)

# Importing images
snakeHeadImage = pygame.image.load("images/SnakeHead.png")
snakeBodyImage = pygame.image.load("images/SnakeBody.png")
appleImage = pygame.image.load("images/Apple.png")
goldenAppleImage = pygame.image.load("images/GoldenApple.png")
icon = pygame.image.load("images/Icon.png")

# Configuring display
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# High score loading
try:
    with open('score.dat', 'rb') as file:
        highScore = pickle.load(file)
except:
    highScore = 0
    with open('score.dat', 'wb') as file:
        pickle.dump(highScore, file)


def startScreen():
    """
    This function loads the start screen of the game.
    :return:
    """
    while True:
        fillBackground(True)
        put_message_center("Welcome to Snake!", green)
        put_message_custom("Click to play.", black, fontSize=30, offsetY=50)
        pygame.display.update()
        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitProgram()
            if event.type == pygame.MOUSEBUTTONDOWN:
                reset()
                gameLoop()


def showScores(score, new):
    """
    This function displays the scores on the display.
    :param score:
    :param new:
    :return:
    """
    screen_text = pygame.font.SysFont("comicsansms", 15).render("Score: " + str(score), True, black)
    gameDisplay.blit(screen_text, (display_width - scoreOffsetX, scoreOffsetY + 20))

    high_score = pygame.font.SysFont("comicsansms", 15).render("High Score: " + str(highScore), True, black)

    if new:
        high_score = pygame.font.SysFont("comicsansms", 15).render("New High Score!", True, red)

    gameDisplay.blit(high_score, (display_width - scoreOffsetX, scoreOffsetY))


def pause():
    """
    This function handles the paused event.
    :return:
    """
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitProgram()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        put_message_center("Game Paused", black, )
        put_message_custom("Click to resume..", black, fontSize=30, offsetY=50)
        pygame.display.update()


def randomApple():
    """
    This function handles the random apple generation.
    :return:
    """
    global randAppleX
    global randAppleY
    global goldenApple

    lastAppleX = randAppleX
    lastAppleY = randAppleY

    goldenApple = generateGoldenApple()

    randAppleX = round(random.randint(block_size * 2, boundX - (block_size * 4)) / block_size) * \
                 block_size
    randAppleY = round(random.randint(block_size * 2, boundY - (block_size * 4)) / block_size) * \
                 block_size

    while [randAppleX, randAppleY] in snakeList or randAppleX == lastAppleX or randAppleY == lastAppleY or \
            (randAppleX >= scoreBoundWidth and randAppleY <= scoreBoundHeight):
        # if the apple generates under the snake or within the high score box, regenerate it
        randAppleX = round(random.randint(block_size * 2, boundX - scoreBoundWidth - (block_size * 4)) / block_size) * \
                     block_size
        randAppleY = round(random.randint(block_size * 2, boundY - scoreBoundHeight - (block_size * 4)) / block_size) * \
                     block_size

    print(str(randAppleY) + " " + str(randAppleX))


def generateGoldenApple():
    """
    this function returns if a golden apple should be generated or not.
    :return:
    """
    return random.randint(1, 15) == 1


def snake(snakeList):
    """
    This function handles blitting the snake and rotating the head of the snake.
    :param snakeList:
    :return:
    """
    rotatedHead = pygame.transform.rotate(snakeHeadImage, degrees)

    gameDisplay.blit(rotatedHead, (snakeList[-1][0], snakeList[-1][1]))

    for coor in snakeList[:-1]:
        gameDisplay.blit(snakeBodyImage, [coor[0], coor[1]])


def put_message_center(message, color):
    """
    This function displays a message in the center of the screen.
    :param message:
    :param color:
    :return:
    """
    screen_text = bodyFont.render(message, True, color)
    gameDisplay.blit(screen_text, [(display_width / 2) - (screen_text.get_rect().width / 2),
                                   (display_height / 2) - (screen_text.get_rect().height / 2)])


def put_message_custom(message, color, offsetY, fontSize=50):
    """
    This function puts a message on the screen based off an offset to the center.
    :param message:
    :param color:
    :param offsetY:
    :param fontSize:
    :return:
    """
    screen_text = pygame.font.SysFont("comicsansms", fontSize).render(message, True, color)
    gameDisplay.blit(screen_text, [(display_width / 2) - (screen_text.get_rect().width / 2),
                                   ((display_height / 2) - (screen_text.get_rect().height / 2) + offsetY)])


def quitProgram():
    """
    This function quits the program.
    :return:
    """
    pygame.quit()
    exit()


def fillBackground(startScreen):
    """
    This function fills the game display background.
    :return:
    """
    gameDisplay.fill(black)
    gameDisplay.fill(white, [block_size, block_size, boundX, boundY])

    if not startScreen:
        gameDisplay.fill(black, [scoreBoundWidth, block_size, display_width - 150, scoreBoundHeight])
        gameDisplay.fill(white, [(scoreBoundWidth + block_size, block_size), (block_size * 7, 100 - (block_size * 2))])


def reset():
    """
    This function resets all the variables to their default value (i.e. starting a new game)
    :return:
    """
    global appleCounter
    global degrees
    global highScore
    global lead_x
    global lead_y
    global lead_x_change
    global lead_y_change
    global randAppleX
    global randAppleY
    global snakeList
    global goldenApple

    degrees = 270
    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = block_size
    lead_y_change = 0
    randAppleX, randAppleY, appleCounter = (0,) * 3
    snakeList = []
    goldenApple = generateGoldenApple()


def gameLoop():
    """
    This is the main game loop, called by startScreen() earlier.
    :return:
    """
    global appleCounter
    global degrees
    global highScore
    global lead_x
    global lead_y
    global lead_x_change
    global lead_y_change
    global snakeList
    global goldenApple
    global FPS
    lead_x_change = block_size
    lead_y_change = 0
    gameOver = False
    goldenApple = generateGoldenApple()

    randomApple()

    while True:
        events = pygame.event.get()
        fillBackground(False)

        while gameOver:  # the user lost
            if highScore < appleCounter:
                # set new high score if applicable
                with open('score.dat', 'rb') as file:
                    highScore = pickle.load(file)
                with open('score.dat', 'wb') as file:
                    pickle.dump(appleCounter, file)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quitProgram()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    reset()
                    gameLoop()
            fillBackground(False)
            showScores(appleCounter, highScore < appleCounter)
            put_message_center("Game Over!", red)
            put_message_custom("Click to play again.", black, fontSize=30, offsetY=50)
            pygame.display.update()

        for event in events:
            if event.type == pygame.QUIT:
                quitProgram()
            if event.type == pygame.KEYDOWN:  # key presses
                if (len(snakeList) < 2 or degrees != 270) and (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                    lead_x_change = -block_size
                    lead_y_change = 0
                    degrees = 90
                elif (len(snakeList) < 2 or degrees != 90) and (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                    lead_x_change = block_size
                    lead_y_change = 0
                    degrees = 270
                elif (len(snakeList) < 2 or degrees != 180) and (event.key == pygame.K_UP or event.key == pygame.K_w):
                    lead_y_change = -block_size
                    lead_x_change = 0
                    degrees = 0
                elif (len(snakeList) < 2 or degrees != 0) and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    lead_y_change = block_size
                    lead_x_change = 0
                    degrees = 180
                elif event.key == pygame.K_p:
                    pause()

        lead_x += lead_x_change
        lead_y += lead_y_change

        if lead_x == randAppleX and lead_y == randAppleY:  # if the snake has eaten the apple
            if goldenApple:
                appleCounter += 3
            else:
                appleCounter += 1
            randomApple()

        snakeHead = [lead_x, lead_y]  # updates the snake's head location

        # checks if a golden apple should be generated
        if goldenApple:
            gameDisplay.blit(goldenAppleImage, (randAppleX, randAppleY))
        else:
            gameDisplay.blit(appleImage, (randAppleX, randAppleY))

        # condition checking if the snake has run into itself or gone out of bounds
        if snakeHead in snakeList[:-1] or \
                (lead_x > boundX or lead_x < block_size or lead_y > boundY or lead_y < block_size)\
                or (lead_x >= scoreBoundWidth and lead_y <= scoreBoundHeight):
            gameOver = True

        snakeList.append(snakeHead)  # add the snakeHead
        snake(snakeList)  # generate the snake

        if len(snakeList) > appleCounter:  # delete the first element of the snakeList.
            del snakeList[0]

        with open('score.dat', 'rb') as file:  # load high score
            highScore = pickle.load(file)

        showScores(appleCounter, highScore < appleCounter)
        pygame.display.update()
        clock.tick(FPS + appleCounter / 10)  # set FPS, scales with how many apples the user has


startScreen()
