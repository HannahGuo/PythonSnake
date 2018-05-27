import pygame
import random
import pickle

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

block_size = 20
display_width = 800
display_height = 600
boundX = display_width - (block_size * 2)
boundY = display_height - (block_size * 2)
scoreOffsetX = 130
scoreOffsetY = 20
FPS = 15

degrees = 270
randAppleX, randAppleY = (0,) * 2
lead_x = display_width / 2
lead_y = display_height / 2
lead_x_change = block_size
lead_y_change = 0
appleCounter = 0
highScore = 0
snakeList = []

bodyFont = pygame.font.SysFont("comicsansms", 50)
snakeHeadImage = pygame.image.load("SnakeHead.png")
appleImage = pygame.image.load("Apple.png")
icon = pygame.image.load("Icon.png")

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Snake")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

try:
    with open('score.dat', 'rb') as file:
        highScore = pickle.load(file)
except:
    highScore = 0
    with open('score.dat', 'wb') as file:
        pickle.dump(highScore, file)


def startScreen():
    while True:
        fillBackground()
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
    screen_text = pygame.font.SysFont("comicsansms", 15).render("Score: " + str(score), True, black)
    gameDisplay.blit(screen_text, (display_width - scoreOffsetX, scoreOffsetY + 20))

    high_score = pygame.font.SysFont("comicsansms", 15).render("High Score: " + str(highScore), True, black)

    if new:
        high_score = pygame.font.SysFont("comicsansms", 15).render("New High Score!", True, red)

    gameDisplay.blit(high_score, (display_width - scoreOffsetX, scoreOffsetY))


def pause():
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitProgram()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        put_message_center("Game Paused", black, fontSize=30)
        put_message_custom("Click to resume..", black, fontSize=30, offsetY=50)
        pygame.display.update()


def randomApple():
    global randAppleX
    global randAppleY
    randAppleX = round(random.randint(block_size, display_width - scoreOffsetX - (block_size * 2)) / block_size) * \
                 block_size
    randAppleY = round(random.randint(block_size, display_height - scoreOffsetY - (block_size * 2)) / block_size) * \
                 block_size

    while randAppleX in snakeList and lead_y in snakeList:
        randAppleX = round(random.randint(block_size, display_width - scoreOffsetX - (block_size * 2)) / block_size) * \
                     block_size
        randAppleY = round(random.randint(block_size, display_height - 30 - (block_size * 2)) / block_size) * block_size


def snake(snakeList):
    rotatedHead = pygame.transform.rotate(snakeHeadImage, degrees)

    gameDisplay.blit(rotatedHead, (snakeList[-1][0], snakeList[-1][1]))

    for coor in snakeList[:-1]:
        gameDisplay.fill(green, [coor[0], coor[1], block_size, block_size])


def put_message_center(message, color):
    screen_text = bodyFont.render(message, True, color)
    gameDisplay.blit(screen_text, [(display_width / 2) - (screen_text.get_rect().width / 2),
                                   (display_height / 2) - (screen_text.get_rect().height / 2)])


def put_message_custom(message, color, offsetY, fontSize=50):
    screen_text = pygame.font.SysFont("comicsansms", fontSize).render(message, True, color)
    gameDisplay.blit(screen_text, [(display_width / 2) - (screen_text.get_rect().width / 2),
                                   ((display_height / 2) - (screen_text.get_rect().height / 2) + offsetY)])


def quitProgram():
    pygame.quit()
    exit()


def fillBackground():
    gameDisplay.fill(black)
    gameDisplay.fill(white, [block_size, block_size, boundX, boundY])

def reset():
    global degrees
    global randAppleX
    global randAppleY
    global lead_x
    global lead_y
    global lead_x_change
    global lead_y_change
    global appleCounter
    global highScore
    global snakeList

    degrees = 270
    randAppleX, randAppleY, appleCounter = (0,) * 3
    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = block_size
    lead_y_change = 0
    snakeList = []


def gameLoop():
    global lead_x
    global lead_y
    global lead_x_change
    global lead_y_change
    global degrees
    global appleCounter
    global highScore
    global snakeList
    lead_x_change = block_size
    lead_y_change = 0
    gameOver = False

    randomApple()

    while True:
        events = pygame.event.get()

        while gameOver:
            if highScore < appleCounter:
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
            fillBackground()
            showScores(appleCounter, highScore < appleCounter)
            put_message_center("Game Over!", red)
            put_message_custom("Click to play again.", black, fontSize=30, offsetY=50)
            pygame.display.update()

        for event in events:
            if event.type == pygame.QUIT:
                quitProgram()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                    degrees = 90
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                    degrees = 270
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                    degrees = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                    degrees = 180
                elif event.key == pygame.K_p:
                    pause()

        lead_x += lead_x_change
        lead_y += lead_y_change

        if lead_x == randAppleX and lead_y == randAppleY:
            randomApple()
            appleCounter += 1

        fillBackground()
        gameDisplay.blit(appleImage, (randAppleX, randAppleY))

        snakeHead = [lead_x, lead_y]

        if snakeHead in snakeList[:-1] or \
                (lead_x > boundX or lead_x < block_size or lead_y > boundY or lead_y < block_size):
            gameOver = True

        snakeList.append(snakeHead)
        snake(snakeList)

        if len(snakeList) > appleCounter:
            del snakeList[0]

        with open('score.dat', 'rb') as file:
            highScore = pickle.load(file)

        showScores(appleCounter, highScore < appleCounter)
        pygame.display.update()
        clock.tick(FPS)

startScreen()
