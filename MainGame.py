import pygame
import random
import pickle  # pickle is used for high score saving
import os
from Snake import Button

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'  # this centers the window to the center of the user's screen

# Color definitions
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
lightRed = (249, 52, 52)
green = (0, 155, 0)
lightGreen = (74, 196, 74)

# Game property constants
blockSize = 20
displayWidth = 800
displayHeight = 600
centerDisplayWidth = displayWidth / 2
centerDisplayHeight = displayHeight / 2
boundX = displayWidth - (blockSize * 2)
boundY = displayHeight - (blockSize * 2)
scoreOffsetX = 140
scoreOffsetY = 27
scoreBoundWidth = displayWidth - 180
scoreBoundHeight = 100 - blockSize

FPS = 13

# Game variables
degrees = 270
randAppleX, randAppleY = (0,) * 2
goldenApple = random.randint(1, 10) == 10
leadX = centerDisplayWidth
leadY = centerDisplayHeight
leadXChange = blockSize
leadYChange = 0
appleCounter = 0
highScore = 0
buttonWidth = 150
buttonHeight = 50
snakeList = []

# Importing font
bodyFont = pygame.font.SysFont("comicsansms", 50)
buttonFont = pygame.font.SysFont("comicsansms", 25)

# Importing images
snakeHeadImage = pygame.image.load("images/SnakeHead.png")
snakeBodyImage = pygame.image.load("images/SnakeBody.png")
appleImage = pygame.image.load("images/Apple.png")
goldenAppleImage = pygame.image.load("images/GoldenApple.png")
icon = pygame.image.load("images/Icon.png")

# Configuring display
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Snake")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

startButton = Button.button(green, lightGreen, gameDisplay, "START", centerDisplayWidth - (buttonWidth / 2),
                            centerDisplayHeight - 30, buttonWidth, buttonHeight, white, -30, centerDisplayWidth,
                            centerDisplayHeight, buttonFont)

quitButton = Button.button(red, lightRed, gameDisplay, "QUIT", centerDisplayWidth - (buttonWidth / 2),
                           centerDisplayHeight + 50, buttonWidth, buttonHeight, white, 50, centerDisplayWidth,
                           centerDisplayHeight, buttonFont)

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
        put_message_custom("Welcome to Snake!", green, -80)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitProgram()

        startButton.showButton()
        quitButton.showButton()

        if startButton.isHovered(getCursorPos()) and isLeftMouseClicked():
            reset()
            return
        elif quitButton.isHovered(getCursorPos()) and isLeftMouseClicked():
            quitProgram()

        pygame.display.update()


def showScores(score, new):
    """
    This function displays the scores on the display.
    :param score:
    :param new:
    :return:
    """
    screen_text = pygame.font.SysFont("comicsansms", 15).render("Score: " + str(score), True, black)
    gameDisplay.blit(screen_text, (displayWidth - scoreOffsetX, scoreOffsetY + 20))

    high_score = pygame.font.SysFont("comicsansms", 15).render("High Score: " + str(highScore), True, black)

    if new:
        high_score = pygame.font.SysFont("comicsansms", 15).render("New High Score!", True, red)

    gameDisplay.blit(high_score, (displayWidth - scoreOffsetX, scoreOffsetY))


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

    randAppleX = round(random.randint(blockSize * 2, boundX - (blockSize * 4)) / blockSize) * blockSize
    randAppleY = round(random.randint(blockSize * 2, boundY - (blockSize * 4)) / blockSize) * blockSize

    while [randAppleX, randAppleY] in snakeList or randAppleX == lastAppleX or randAppleY == lastAppleY or \
            (randAppleX >= scoreBoundWidth and randAppleY <= scoreBoundHeight):
        # if the apple generates under the snake or within the high score box, regenerate it
        randAppleX = round(random.randint(blockSize * 2, boundX - scoreBoundWidth - (blockSize * 4)) / blockSize) * \
                     blockSize
        randAppleY = round(random.randint(blockSize * 2, boundY - scoreBoundHeight - (blockSize * 4)) / blockSize) * \
                     blockSize


def generateGoldenApple():
    """
    This function returns if a golden apple should be generated or not.
    :return:
    """
    return random.randint(1, 15) == 1


def snake(snakeCoors):
    """
    This function handles blitting the snake and rotating the head of the snake.
    :param snakeCoors:
    :return:
    """
    rotatedHead = pygame.transform.rotate(snakeHeadImage, degrees)

    gameDisplay.blit(rotatedHead, (snakeCoors[-1][0], snakeCoors[-1][1]))

    for coor in snakeCoors[:-1]:
        gameDisplay.blit(snakeBodyImage, [coor[0], coor[1]])


def put_message_center(message, color):
    """
    This function displays a message in the center of the screen.
    :param message:
    :param color:
    :return:
    """
    screen_text = bodyFont.render(message, True, color)
    gameDisplay.blit(screen_text, [centerDisplayWidth - (screen_text.get_rect().width / 2), centerDisplayHeight -
                                   (screen_text.get_rect().height / 2)])


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
    gameDisplay.blit(screen_text, [centerDisplayWidth - (screen_text.get_rect().width / 2),
                                   (centerDisplayHeight - (screen_text.get_rect().height / 2) + offsetY)])


def quitProgram():
    """
    This function quits the program.
    :return:
    """
    pygame.quit()
    exit()


def fillBackground(isStartScreen):
    """
    This function fills the game display background.
    :return:
    """
    gameDisplay.fill(black)
    gameDisplay.fill(white, [blockSize, blockSize, boundX, boundY])

    if not isStartScreen:
        gameDisplay.fill(black, [scoreBoundWidth, blockSize, displayWidth - 150, scoreBoundHeight])
        gameDisplay.fill(white, [(scoreBoundWidth + blockSize, blockSize), (blockSize * 7, 100 - (blockSize * 2))])


def reset():
    """
    This function resets all the variables to their default value (i.e. starting a new game)
    :return:
    """
    global appleCounter
    global degrees
    global highScore
    global leadX
    global leadY
    global leadXChange
    global leadYChange
    global randAppleX
    global randAppleY
    global snakeList
    global goldenApple

    degrees = 270
    leadX = centerDisplayWidth
    leadY = centerDisplayHeight
    leadXChange = blockSize
    leadYChange = 0
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
    global leadX
    global leadY
    global leadXChange
    global leadYChange
    global snakeList
    global goldenApple
    global FPS
    leadXChange = blockSize
    leadYChange = 0
    gameOver = False
    goldenApple = generateGoldenApple()

    randomApple()

    while True:
        events = pygame.event.get()
        fillBackground(False)

        while gameOver:  # the user lost
            if highScore < appleCounter:
                # set new high score if applicable
                with open('score.dat', 'rb') as fromFile:
                    highScore = pickle.load(fromFile)
                with open('score.dat', 'wb') as fromFile:
                    pickle.dump(appleCounter, fromFile)
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
                    leadXChange = -blockSize
                    leadYChange = 0
                    degrees = 90
                elif (len(snakeList) < 2 or degrees != 90) and (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                    leadXChange = blockSize
                    leadYChange = 0
                    degrees = 270
                elif (len(snakeList) < 2 or degrees != 180) and (event.key == pygame.K_UP or event.key == pygame.K_w):
                    leadYChange = -blockSize
                    leadXChange = 0
                    degrees = 0
                elif (len(snakeList) < 2 or degrees != 0) and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    leadYChange = blockSize
                    leadXChange = 0
                    degrees = 180
                elif event.key == pygame.K_p:
                    pause()

        leadX += leadXChange
        leadY += leadYChange

        if leadX == randAppleX and leadY == randAppleY:  # if the snake has eaten the apple
            if goldenApple:
                appleCounter += 3
            else:
                appleCounter += 1
            randomApple()

        snakeHead = [leadX, leadY]  # updates the snake's head location

        # checks if a golden apple should be generated
        if goldenApple:
            gameDisplay.blit(goldenAppleImage, (randAppleX, randAppleY))
        else:
            gameDisplay.blit(appleImage, (randAppleX, randAppleY))

        # condition checking if the snake has run into itself or gone out of bounds
        if snakeHead in snakeList[:-1] or \
                (leadX > boundX or leadX < blockSize or leadY > boundY or leadY < blockSize) \
                or (leadX >= scoreBoundWidth and leadY <= scoreBoundHeight):
            gameOver = True

        snakeList.append(snakeHead)  # add the snakeHead
        snake(snakeList)  # generate the snake

        if len(snakeList) > appleCounter:  # delete the first element of the snakeList.
            del snakeList[0]

        with open('score.dat', 'rb') as fromFile:  # load high score
            highScore = pickle.load(fromFile)

        showScores(appleCounter, highScore < appleCounter)
        pygame.display.update()
        clock.tick(FPS + (appleCounter / 50))  # set FPS, scales with how many apples the user has


def getCursorPos():
    return pygame.mouse.get_pos()


def isLeftMouseClicked():
    return pygame.mouse.get_pressed()[0]


while True:
    startScreen()
    gameLoop()
