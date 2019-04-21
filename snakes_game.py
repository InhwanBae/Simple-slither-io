import pygame
import random
import argparse

pygame.init()
fancy_graphic = False

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

display_width = 800
display_height = 800

block_size = 20
apple_count = 300

# Game Speed
fps = 15
font = pygame.font.SysFont("arialback", 50)
smallfont = pygame.font.SysFont("arialblack", 25)
largefont = pygame.font.SysFont("arialblack", 80)
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("SLITHER.IO")

img = pygame.image.load("snakeEye.png")
bg = pygame.image.load("background.png")

bodyimg = []
for i in range(1, 9):
    bodyimg.append(pygame.image.load("snakeBody" + str(i) + ".png"))

eyeimg = []
for i in range(1, 9):
    eyeimg.append(pygame.image.load("snakeEye" + str(i) + ".png"))

shader = pygame.image.load("snakeShader40.png")

return_direction = [0, 0, 0, 0, 0, 0, 0]


def snake(block_size, snakelist, slot):
    if fancy_graphic:
        body = bodyimg[0]

        if slot in range(1, 9):
            body = bodyimg[slot-1]

        # Generate 1/2 points
        bodylist = []
        for i in range(len(snakelist)):
            if i < len(snakelist) - 1:
                bodylist.append(
                    [(snakelist[i][0] + snakelist[i + 1][0]) / 2, (snakelist[i][1] + snakelist[i + 1][1]) / 2])
        snakebody = []
        snakebody.append(snakelist[0])
        for i in range(len(bodylist)):
            snakebody.append(bodylist[i])

            if i < len(bodylist) - 1:
                snakebody.append([(bodylist[i][0] + bodylist[i + 1][0]) / 2, (bodylist[i][1] + bodylist[i + 1][1]) / 2])
        snakebody.append(snakelist[-1])

        # Generate 1/4 points
        bodylist2 = []
        for i in range(len(snakebody)):
            if i < len(snakebody) - 1:
                bodylist2.append(
                    [(snakebody[i][0] + snakebody[i + 1][0]) / 2, (snakebody[i][1] + snakebody[i + 1][1]) / 2])
        snakebody2 = []
        snakebody2.append(snakebody[0])
        for i in range(len(bodylist2)):
            snakebody2.append(bodylist2[i])

            if i < len(bodylist2) - 1:
                snakebody2.append(
                    [(bodylist2[i][0] + bodylist2[i + 1][0]) / 2, (bodylist2[i][1] + bodylist2[i + 1][1]) / 2])
        snakebody2.append(snakebody[-1])

        for i in range(len(snakebody2)):
            if not i % 2 == 1:
                gameDisplay.blit(shader, (snakebody2[i][0] - 10, snakebody2[i][1] - 8))

        for XnY in snakebody2:
            gameDisplay.blit(body, (XnY[0] - 2, XnY[1] - 2))

        # Draw eye
        if len(snakelist) > 1:
            if snakebody2[-1][0] == snakebody2[-3][0] and snakebody2[-1][1] < snakebody2[-3][1]:
                gameDisplay.blit(eyeimg[0], (snakelist[-1][0] - 2, snakelist[-1][1] - 2))
            if snakebody2[-1][0] > snakebody2[-3][0] and snakebody2[-1][1] < snakebody2[-3][1]:
                gameDisplay.blit(eyeimg[1], (snakelist[-1][0] - 2, snakelist[-1][1] - 2))
            if snakebody2[-1][0] > snakebody2[-3][0] and snakebody2[-1][1] == snakebody2[-3][1]:
                gameDisplay.blit(eyeimg[2], (snakelist[-1][0] - 2, snakelist[-1][1] - 2))
            if snakebody2[-1][0] > snakebody2[-3][0] and snakebody2[-1][1] > snakebody2[-3][1]:
                gameDisplay.blit(eyeimg[3], (snakelist[-1][0] - 2, snakelist[-1][1] - 2))
            if snakebody2[-1][0] == snakebody2[-3][0] and snakebody2[-1][1] > snakebody2[-3][1]:
                gameDisplay.blit(eyeimg[4], (snakelist[-1][0] - 2, snakelist[-1][1] - 2))
            if snakebody2[-1][0] < snakebody2[-3][0] and snakebody2[-1][1] > snakebody2[-3][1]:
                gameDisplay.blit(eyeimg[5], (snakelist[-1][0] - 2, snakelist[-1][1] - 2))
            if snakebody2[-1][0] < snakebody2[-3][0] and snakebody2[-1][1] == snakebody2[-3][1]:
                gameDisplay.blit(eyeimg[6], (snakelist[-1][0] - 2, snakelist[-1][1] - 2))
            if snakebody2[-1][0] < snakebody2[-3][0] and snakebody2[-1][1] < snakebody2[-3][1]:
                gameDisplay.blit(eyeimg[7], (snakelist[-1][0] - 2, snakelist[-1][1] - 2))
        else:
            gameDisplay.blit(eyeimg[0], (snakelist[-1][0] - 2, snakelist[-1][1] - 2))

    else:
        if slot == 1:
            color = white
        elif slot == 2:
            color = blue
        elif slot == 3:
            color = blue
        elif slot == 4:
            color = blue
        elif slot == 5:
            color = blue
        elif slot == 6:
            color = blue
        elif slot == 7:
            color = blue
        elif slot == 8:
            color = blue

        for XnY in snakelist:
            pygame.draw.rect(gameDisplay, color, [XnY[0], XnY[1], block_size, block_size])

        gameDisplay.blit(img, (snakelist[-1][0], snakelist[-1][1]))


def snakeBot(_snakeList, _appleList, _enemyList):
    # Define cardinal points
    #    1
    # 3  0  4
    #    2

    snakeHead = _snakeList[-1]
    xhead = snakeHead[0]
    yhead = snakeHead[1]

    xpos = [xhead - block_size * 3, xhead - block_size * 2, xhead - block_size, xhead,
            xhead + block_size, xhead + block_size * 2, xhead + block_size * 3]
    ypos = [yhead - block_size * 3, yhead - block_size * 2, yhead - block_size, yhead,
            yhead + block_size, yhead + block_size * 2, yhead + block_size * 3]
    xapos = [xhead - block_size * 5, xhead - block_size * 4, xhead - block_size * 3, xhead - block_size * 2,
             xhead - block_size, xhead, xhead + block_size, xhead + block_size * 2, xhead + block_size * 3,
             xhead + block_size * 4, xhead + block_size * 5]
    yapos = [yhead - block_size * 5, yhead - block_size * 4, yhead - block_size * 3, yhead - block_size * 2,
             yhead - block_size, yhead, yhead + block_size, yhead + block_size * 2, yhead + block_size * 3,
             yhead + block_size * 4, yhead + block_size * 5]
    xabpos = [xhead - block_size, xhead, xhead + block_size]
    yabpos = [yhead - block_size, yhead, yhead + block_size]

    snakeList = []
    appleList = []
    enemyList = []

    for i in _snakeList:
        if xhead - block_size * 5 <= i[0] <= xhead + block_size * 5 and yhead - block_size * 5 <= i[1] <= yhead + block_size * 5:
            snakeList.append(i)
    for j in _appleList:
        if xhead - block_size * 5 <= j[0] <= xhead + block_size * 5 and yhead - block_size * 5 <= j[1] <= yhead + block_size * 5:
            appleList.append(j)
    for k in _enemyList:
        if xhead - block_size * 5 <= k[0] <= xhead + block_size * 5 and yhead - block_size * 5 <= k[1] <= yhead + block_size * 5:
            enemyList.append(k)

    # Random weights with a random number between 0 and 1
    up = random.random()
    down = random.random()
    left = random.random()
    right = random.random()

    # AI path calculation using weights
    for i in xapos:
        for j in yapos:
            for apple in appleList:
                if [i, j] == apple:
                    if xhead <= apple[0] and yhead <= apple[1]:
                        right += 20
                        down += 20
                    if xhead <= apple[0] and yhead >= apple[1]:
                        right += 20
                        up += 20
                    if xhead >= apple[0] and yhead <= apple[1]:
                        left += 20
                        down += 20
                    if xhead >= apple[0] and yhead >= apple[1]:
                        left += 20
                        up += 20

    for i in xabpos:
        for j in yabpos:
            for apple in appleList:
                if [i, j] == apple:
                    if xhead <= apple[0] and yhead <= apple[1]:
                        right += 200
                        down += 200
                    if xhead <= apple[0] and yhead >= apple[1]:
                        right += 200
                        up += 200
                    if xhead >= apple[0] and yhead <= apple[1]:
                        left += 200
                        down += 200
                    if xhead >= apple[0] and yhead >= apple[1]:
                        left += 200
                        up += 200

    for i in xpos:
        for j in ypos:
            for apple in appleList:
                if [i, j] == apple:
                    if xhead <= apple[0] and yhead <= apple[1]:
                        right += 80
                        down += 80
                    if xhead <= apple[0] and yhead >= apple[1]:
                        right += 80
                        up += 80
                    if xhead >= apple[0] and yhead <= apple[1]:
                        left += 80
                        down += 80
                    if xhead >= apple[0] and yhead >= apple[1]:
                        left += 80
                        up += 80

            for enemy in enemyList:
                if [i, j] == enemy:
                    if xhead < enemy[0] and yhead < enemy[1]:
                        right -= 600 / abs(enemy[0] - xhead)
                        down -= 600 / abs(enemy[1] - yhead)
                    if xhead < enemy[0] and yhead > enemy[1]:
                        right -= 600 / abs(enemy[0] - xhead)
                        up -= 600 / abs(enemy[1] - yhead)
                    if xhead > enemy[0] and yhead < enemy[1]:
                        left -= 600 / abs(enemy[0] - xhead)
                        down -= 600 / abs(enemy[1] - yhead)
                    if xhead > enemy[0] and yhead > enemy[1]:
                        left -= 600 / abs(enemy[0] - xhead)
                        up -= 600 / abs(enemy[1] - yhead)

            for body in snakeList:
                if [i, j] == body:
                    if xhead <= body[0] and yhead <= body[1]:
                        right -= 100 / (abs(body[0] - xhead) + 20)
                        down -= 100 / (abs(body[1] - yhead) + 20)
                    if xhead <= body[0] and yhead >= body[1]:
                        right -= 100 / (abs(body[0] - xhead) + 20)
                        up -= 100 / (abs(body[1] - yhead) + 20)
                    if xhead >= body[0] and yhead <= body[1]:
                        left -= 100 / (abs(body[0] - xhead) + 20)
                        down -= 100 / (abs(body[1] - yhead) + 20)
                    if xhead >= body[0] and yhead >= body[1]:
                        left -= 100 / (abs(body[0] - xhead) + 20)
                        up -= 100 / (abs(body[1] - yhead) + 20)

    if [xhead, yhead - block_size] in snakeList:
        up -= 10000
    if [xhead, yhead + block_size] in snakeList:
        down -= 10000
    if [xhead - block_size, yhead] in snakeList:
        left -= 10000
    if [xhead + block_size, yhead] in snakeList:
        right -= 10000

    if [xhead, yhead - block_size] in appleList:
        up += 2000
    if [xhead, yhead + block_size] in appleList:
        down += 2000
    if [xhead - block_size, yhead] in appleList:
        left += 2000
    if [xhead + block_size, yhead] in appleList:
        right += 2000

    if yhead - block_size < 0:
        up -= 1000
    if yhead + block_size >= display_height:
        down -= 1000
    if xhead - block_size < display_width:
        left -= 1000
    if xhead + block_size >= display_width:
        right -= 1000

    #print("up: " + str(up) + ", down: " + str(down) + ", left: " + str(left) + ", right: " + str(right))
    if up > down and up > left and up > right:
        return 1
    elif down > up and down > left and down > right:
        return 2
    elif left > up and left > down and left > right:
        return 3
    elif right > up and right > down and right > left:
        return 4

    direction = round(random.randrange(0, 5) / 4) * 4 + 1
    return direction


def snakeBotMulti(botData):
    """Multiprocessing functions"""
    # print("Process start")
    direction = snakeBot(botData[1], botData[2], botData[3])
    return_direction[botData[0]] = direction
    #print("bot", botData[0] + 2, "direction:", direction)
    # print("Process end")


def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = font.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def gameLoop():
    # Game end condition
    start = 0
    end = 0

    # Game definition
    gameExit = False
    gameOver = False

    # Earthworm definition
    snakeList = []
    snakeList2 = []
    snakeList3 = []
    snakeList4 = []
    snakeList5 = []
    snakeList6 = []
    snakeList7 = []
    snakeList8 = []

    # Definition of snake length
    snakeLength = 3
    snakeLength2 = 3
    snakeLength3 = 3
    snakeLength4 = 3
    snakeLength5 = 3
    snakeLength6 = 3
    snakeLength7 = 3
    snakeLength8 = 3

    lead_x = round(random.randrange(0, display_width - block_size) / 20.0) * 20.0
    lead_y = round(random.randrange(0, display_width - block_size) / 20.0) * 20.0
    lead_x_change = 0
    lead_y_change = 0

    appleList = []

    # Creation of the location of snakes
    while True:
        randPosition = [round(random.randrange(0, display_width - block_size) / 20.0) * 20.0,
                      round(random.randrange(0, display_width - block_size) / 20.0) * 20.0]

        # Specify a value
        if len(snakeList) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
            snakeList.append([lead_x, lead_y])
            continue
        if len(snakeList2) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
            snakeList2.append(randPosition)
            continue
        if len(snakeList3) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
            snakeList3.append(randPosition)
            continue
        if len(snakeList4) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
            snakeList4.append(randPosition)
            continue
        if len(snakeList5) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
            snakeList5.append(randPosition)
            continue
        if len(snakeList6) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
            snakeList6.append(randPosition)
            continue
        if len(snakeList7) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
            snakeList7.append(randPosition)
            continue
        if len(snakeList8) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
            snakeList8.append(randPosition)
            continue

        # Termination condition
        if len(snakeList) > 0 and len(snakeList2) > 0 and len(snakeList3) > 0 and len(snakeList4) > 0 and len(snakeList5) > 0 and len(snakeList6) > 0 and len(snakeList7) > 0 and len(snakeList8) > 0:
            break

    # Generate apple
    while len(appleList) <= apple_count:
        randAppleX = round(random.randrange(0, display_width - block_size) / 20.0) * 20.0
        randAppleY = round(random.randrange(0, display_height - block_size) / 20.0) * 20.0
        genApple = [randAppleX, randAppleY]

        # Avoid apples in the same location
        noApple = True
        for apple in appleList:
            if genApple == apple:
                noApple = False
        # Avoiding apples on snakes
        for snakeAll in [snakeList, snakeList2, snakeList3, snakeList4, snakeList5, snakeList6, snakeList7, snakeList8]:
            for snakeBody in snakeAll:
                if genApple == snakeBody:
                    noApple = False

        if noApple == True:
            appleList.append(genApple)

    # Game implementation
    while not gameExit:

        # When the game is over
        while gameOver == True:
            gameDisplay.fill(black)
            message("Game Over", white, -50, "large")
            message("Score: " + str(snakeLength - 3), white, 50, size="medium")
            message("Game Over, press C to play again or Q to quit", white, 100, size="small")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameLoop()
                    elif event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False

        # User input processing statement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                start = 1
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0

        # Death when leaving the map
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        # When ate an apple
        for apple in appleList:
            if snakeList[-1] == apple:
                snakeLength += 1
                appleList.remove(apple)
            if snakeList2[-1] == apple:
                snakeLength2 += 1
                appleList.remove(apple)
            if snakeList3[-1] == apple:
                snakeLength3 += 1
                appleList.remove(apple)
            if snakeList4[-1] == apple:
                snakeLength4 += 1
                appleList.remove(apple)
            if snakeList5[-1] == apple:
                snakeLength5 += 1
                appleList.remove(apple)
            if snakeList6[-1] == apple:
                snakeLength6 += 1
                appleList.remove(apple)
            if snakeList7[-1] == apple:
                snakeLength7 += 1
                appleList.remove(apple)
            if snakeList8[-1] == apple:
                snakeLength8 += 1
                appleList.remove(apple)

        # Generate apple
        while len(appleList) <= apple_count and len(appleList) + len(snakeList) + len(snakeList2) + len(snakeList3) + len(snakeList4) + len(snakeList5) + len(snakeList6) + len(snakeList7) + len(snakeList8) < 50*50:
            randAppleX = round(random.randrange(0, display_width - block_size) / 20.0) * 20.0
            randAppleY = round(random.randrange(0, display_height - block_size) / 20.0) * 20.0
            genApple = [randAppleX, randAppleY]

            # Avoid apples in the same location
            noApple = True
            for apple in appleList:
                if genApple == apple:
                    noApple = False
            # Avoiding apples on snakes
            for snakeAll in [snakeList, snakeList2, snakeList3, snakeList4, snakeList5, snakeList6, snakeList7, snakeList8]:
                for snakeBody in snakeAll:
                    if genApple == snakeBody:
                        noApple = False

            if noApple == True:
                appleList.append(genApple)


        # Add head position
        lead_x += lead_x_change
        lead_y += lead_y_change

        # Move head, add list and remove last tail
        snakeList.append([lead_x, lead_y])
        if len(snakeList) > snakeLength:
            del snakeList[0]

        # Move Snake Bot
        #bot2
        status = snakeBot(snakeList2, appleList,
                          snakeList + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8)
        if status == 1:
            snakeList2.append([snakeList2[-1][0], snakeList2[- 1][1] - block_size])
        elif status == 2:
            snakeList2.append([snakeList2[-1][0], snakeList2[-1][1] + block_size])
        elif status == 3:
            snakeList2.append([snakeList2[-1][0] - block_size, snakeList2[-1][1]])
        elif status == 4:
            snakeList2.append([snakeList2[-1][0] + block_size, snakeList2[-1][1]])
        if len(snakeList2) > snakeLength2:
            del snakeList2[0]

        # bot3
        status = snakeBot(snakeList3, appleList,
                          snakeList + snakeList2 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8)
        if status == 1:
            snakeList3.append([snakeList3[-1][0], snakeList3[-1][1] - block_size])
        elif status == 2:
            snakeList3.append([snakeList3[-1][0], snakeList3[-1][1] + block_size])
        elif status == 3:
            snakeList3.append([snakeList3[-1][0] - block_size, snakeList3[-1][1]])
        elif status == 4:
            snakeList3.append([snakeList3[-1][0] + block_size, snakeList3[-1][1]])
        if len(snakeList3) > snakeLength3:
            del snakeList3[0]

        # bot4
        status = snakeBot(snakeList4, appleList,
                          snakeList + snakeList2 + snakeList3 + snakeList5 + snakeList6 + snakeList7 + snakeList8)
        if status == 1:
            snakeList4.append([snakeList4[-1][0], snakeList4[-1][1] - block_size])
        elif status == 2:
            snakeList4.append([snakeList4[-1][0], snakeList4[-1][1] + block_size])
        elif status == 3:
            snakeList4.append([snakeList4[-1][0] - block_size, snakeList4[-1][1]])
        elif status == 4:
            snakeList4.append([snakeList4[-1][0] + block_size, snakeList4[-1][1]])
        if len(snakeList4) > snakeLength4:
            del snakeList4[0]

        # bot5
        status = snakeBot(snakeList5, appleList,
                          snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList6 + snakeList7 + snakeList8)
        if status == 1:
            snakeList5.append([snakeList5[-1][0], snakeList5[-1][1] - block_size])
        elif status == 2:
            snakeList5.append([snakeList5[-1][0], snakeList5[-1][1] + block_size])
        elif status == 3:
            snakeList5.append([snakeList5[-1][0] - block_size, snakeList5[-1][1]])
        elif status == 4:
            snakeList5.append([snakeList5[-1][0] + block_size, snakeList5[-1][1]])
        if len(snakeList5) > snakeLength5:
            del snakeList5[0]

        # bot6
        status = snakeBot(snakeList6, appleList,
                          snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList7 + snakeList8)
        if status == 1:
            snakeList6.append([snakeList6[-1][0], snakeList6[-1][1] - block_size])
        elif status == 2:
            snakeList6.append([snakeList6[-1][0], snakeList6[-1][1] + block_size])
        elif status == 3:
            snakeList6.append([snakeList6[-1][0] - block_size, snakeList6[-1][1]])
        elif status == 4:
            snakeList6.append([snakeList6[-1][0] + block_size, snakeList6[-1][1]])
        if len(snakeList6) > snakeLength6:
            del snakeList6[0]

        # bot7
        status = snakeBot(snakeList7, appleList,
                          snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList8)
        if status == 1:
            snakeList7.append([snakeList7[-1][0], snakeList7[-1][1] - block_size])
        elif status == 2:
            snakeList7.append([snakeList7[-1][0], snakeList7[-1][1] + block_size])
        elif status == 3:
            snakeList7.append([snakeList7[-1][0] - block_size, snakeList7[-1][1]])
        elif status == 4:
            snakeList7.append([snakeList7[-1][0] + block_size, snakeList7[-1][1]])
        if len(snakeList7) > snakeLength7:
            del snakeList7[0]

        # bot8
        status = snakeBot(snakeList8, appleList,
                          snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7)
        if status == 1:
            snakeList8.append([snakeList8[-1][0], snakeList8[-1][1] - block_size])
        elif status == 2:
            snakeList8.append([snakeList8[-1][0], snakeList8[-1][1] + block_size])
        elif status == 3:
            snakeList8.append([snakeList8[-1][0] - block_size, snakeList8[-1][1]])
        elif status == 4:
            snakeList8.append([snakeList8[-1][0] + block_size, snakeList8[-1][1]])
        if len(snakeList8) > snakeLength8:
            del snakeList8[0]


        # When the head of the player and the body of the other player are hit, the game ends
        if start != 0:
            if snakeList[-1] in snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
                gameOver = True

        # If the computer crashes or goes out, replaced with apple and reset
        appleAddList = []
        removeSnake2 = removeSnake3 = removeSnake4 = removeSnake5 = removeSnake6 = removeSnake7 = removeSnake8 = False

        if snakeList2[-1] in snakeList + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
            appleAddList += snakeList2
            removeSnake2 = True
        if snakeList3[-1] in snakeList + snakeList2 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
            appleAddList += snakeList3
            removeSnake3 = True
        if snakeList4[-1] in snakeList + snakeList2 + snakeList3 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
            appleAddList += snakeList4
            removeSnake4 = True
        if snakeList5[-1] in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList6 + snakeList7 + snakeList8:
            appleAddList += snakeList5
            removeSnake5 = True
        if snakeList6[-1] in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList7 + snakeList8:
            appleAddList += snakeList6
            removeSnake6 = True
        if snakeList7[-1] in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList8:
            appleAddList += snakeList7
            removeSnake7 = True
        if snakeList8[-1] in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7:
            appleAddList += snakeList8
            removeSnake8 = True

        if snakeList2[-1][0] >= display_width or snakeList2[-1][0] < 0 or snakeList2[-1][1] >= display_height or snakeList2[-1][1] < 0:
            #appleAddList += snakeList2
            removeSnake2 = True
        if snakeList3[-1][0] >= display_width or snakeList3[-1][0] < 0 or snakeList3[-1][1] >= display_height or snakeList3[-1][1] < 0:
            #appleAddList += snakeList3
            removeSnake3 = True
        if snakeList4[-1][0] >= display_width or snakeList4[-1][0] < 0 or snakeList4[-1][1] >= display_height or snakeList4[-1][1] < 0:
            #appleAddList += snakeList4
            removeSnake4 = True
        if snakeList5[-1][0] >= display_width or snakeList5[-1][0] < 0 or snakeList5[-1][1] >= display_height or snakeList5[-1][1] < 0:
            #appleAddList += snakeList5
            removeSnake5 = True
        if snakeList6[-1][0] >= display_width or snakeList6[-1][0] < 0 or snakeList6[-1][1] >= display_height or snakeList6[-1][1] < 0:
            #appleAddList += snakeList6
            removeSnake6 = True
        if snakeList7[-1][0] >= display_width or snakeList7[-1][0] < 0 or snakeList7[-1][1] >= display_height or snakeList7[-1][1] < 0:
            #appleAddList += snakeList7
            removeSnake7 = True
        if snakeList8[-1][0] >= display_width or snakeList8[-1][0] < 0 or snakeList8[-1][1] >= display_height or snakeList8[-1][1] < 0:
            #appleAddList += snakeList8
            removeSnake8 = True

        if removeSnake2:
            snakeList2.clear()
            snakeLength2 = 3
        if removeSnake3:
            snakeList3.clear()
            snakeLength3 = 3
        if removeSnake4:
            snakeList4.clear()
            snakeLength4 = 3
        if removeSnake5:
            snakeList5.clear()
            snakeLength5 = 3
        if removeSnake6:
            snakeList6.clear()
            snakeLength6 = 3
        if removeSnake7:
            snakeList7.clear()
            snakeLength7 = 3
        if removeSnake8:
            snakeList8.clear()
            snakeLength8 = 3

        for apple in appleAddList:
            if apple not in appleList:
                appleList.append(apple)

        while True:
            randPosition = [round(random.randrange(0, display_width - block_size) / 20.0) * 20.0,
                            round(random.randrange(0, display_width - block_size) / 20.0) * 20.0]

            # Specify computer values
            if len(snakeList2) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
                snakeList2.append(randPosition)
                continue
            if len(snakeList3) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
                snakeList3.append(randPosition)
                continue
            if len(snakeList4) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
                snakeList4.append(randPosition)
                continue
            if len(snakeList5) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
                snakeList5.append(randPosition)
                continue
            if len(snakeList6) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
                snakeList6.append(randPosition)
                continue
            if len(snakeList7) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
                snakeList7.append(randPosition)
                continue
            if len(snakeList8) == 0 and randPosition not in snakeList + snakeList2 + snakeList3 + snakeList4 + snakeList5 + snakeList6 + snakeList7 + snakeList8:
                snakeList8.append(randPosition)
                continue

            # Termination condition
            if len(snakeList) > 0 and len(snakeList2) > 0 and len(snakeList3) > 0 and len(snakeList4) > 0 and len(
                    snakeList5) > 0 and len(snakeList6) > 0 and len(snakeList7) > 0 and len(snakeList8) > 0:
                break

        # Implemented on the game screen
        gameDisplay.fill(black)
        if fancy_graphic:
            gameDisplay.blit(bg, (0, 0))

        for apple in appleList:
            pygame.draw.rect(gameDisplay, red, [apple[0], apple[1], block_size, block_size])

        snake(block_size, snakeList, 1)
        snake(block_size, snakeList2, 2)
        snake(block_size, snakeList3, 3)
        snake(block_size, snakeList4, 4)
        snake(block_size, snakeList5, 5)
        snake(block_size, snakeList6, 6)
        snake(block_size, snakeList7, 7)
        snake(block_size, snakeList8, 8)

        # Screen update
        pygame.display.update()

        # Wait till next tick
        clock.tick(fps)

    pygame.quit()
    quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='--fancy: Fancy Graphics')
    parser.add_argument("-f", "--fancy", required=False)
    args = parser.parse_args()
    fancy = args.fancy
    if fancy in ["True", "true", "TRUE", "t", "T"]:
        fancy_graphic = True
    #fancy_graphic = True
    gameLoop()



