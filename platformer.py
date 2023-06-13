#get ready
import pygame
from random import randint
pygame.init()
#functions
def playlevel():
    #variables
    posX = 200
    posY = 550
    velX = 0
    velY = 0
    wall = [False, False]
    facing = False
    jump = False
    ground = False
    down = 2
    timer = 0
    deaths = 0
    #count
    for i in range(3):
        #inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    facing = "r"
                elif event.key == pygame.K_LEFT:
                    facing = "l"
                elif event.key == pygame.K_q:
                    gameDisplay.fill(dark_red)
                    pygame.display.update()
                    clock.tick(20)
                    return False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    down = 5
                elif event.key == pygame.K_RIGHT and facing == "r" :
                    facing = False
                elif event.key == pygame.K_LEFT and facing == "l":
                    facing = False
        #draw
        gameDisplay.fill(backgroundcolor)
        #text
        for message in text:
            say(message[0], black, message[1], font1)
        say("Press q to quit", black, (105,25), font1)
        say(digtime(timer), black, (60,55), font1)
        say("level: "+str(level+1), black ,(60,80), font1)
        say("deaths: "+str(deaths), dark_red, (75,105), font1)
        #player
        pygame.draw.rect(gameDisplay, green, [posX, posY, 25, 25])
        #normal blocks
        for block in blocks:
            pygame.draw.rect(gameDisplay, dark_brown, block)
            #grass
            pygame.draw.rect(gameDisplay, dark_green, [block[0], block[1], block[2], 10])
            pygame.draw.rect(gameDisplay, dark_green, [block[0], block[1]+10, 10, 10])
            pygame.draw.rect(gameDisplay, dark_green, [block[0], block[1]+20, 5, 5])
            pygame.draw.rect(gameDisplay, dark_green, [block[0]+block[2]-10, block[1]+10, 10, 10])
            pygame.draw.rect(gameDisplay, dark_green, [block[0]+block[2]-5, block[1]+20, 5, 5])
            for j in range(block[2]//50):
                pygame.draw.rect(gameDisplay, dark_green, [block[0]+j*50+6.25, block[1]+10, 12.5, 5])
                pygame.draw.rect(gameDisplay, dark_green, [block[0]+j*50+31.25, block[1]+10, 12.5, 5])
        #red blocks
        for block in blocks2:
            pygame.draw.rect(gameDisplay, red, block)
        #key
        pygame.draw.circle(gameDisplay, yellow, [keyX, keyY], 10, 5)
        pygame.draw.rect(gameDisplay, yellow, [keyX+8, keyY-2.5, 22, 5])
        pygame.draw.rect(gameDisplay, yellow, [keyX+15, keyY+2.5, 10, 5])
        #count
        say(str(3-i), black, (625,325), ("impact",150))
        #show + wait
        pygame.display.update()
        clock.tick(2)
    #play
    while True:
        #inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    facing = "r"
                elif event.key == pygame.K_LEFT:
                    facing = "l"
                elif (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and ground:
                    jump = True
                    ground = False
                elif event.key == pygame.K_q:
                    gameDisplay.fill(dark_red)
                    pygame.display.update()
                    clock.tick(20)
                    return False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    down = 5
                elif event.key == pygame.K_RIGHT and facing == "r" :
                    facing = False
                elif event.key == pygame.K_LEFT and facing == "l":
                    facing = False
        #change Y-velocity
        if jump:
            velY = -20
            jump = False
        elif not ground:
            if velY > -10 and down < 5:
                down = 3
            if velY+down < 30:
                velY += down
            else:
                velY = 30
        #change X-velocity
        if facing == "r" and not wall[0]:
            if velX < 0:
                velX += 4
            elif velX < 18:
                velX += 2
                wall[1] = False
            else:
                velX = 20
        elif facing == "l" and not wall[1] :
            if velX > 0:
                velX += -4
            elif velX > -18:
                velX += -2
                wall[0] = False
            else:
                velX = -20
        else:
            if velX < 0:
                velX += 1
            elif velX > 0:
                velX += -1
        #move
        posX += velX
        posY += velY
        #check collisions + death
        if posX < 0 or posX > 1225 or posY < 0 or posY > 625:
            posX = 200
            posY = 550
            velX = 0
            velY = 0
            deaths += 1
            gameDisplay.fill(dark_red)
            pygame.display.update()
            clock.tick(20)
            timer+=1
        ground = False
        wall = [False,False]
        for block in blocks2:
            if posX+25 > block[0] and posX < block[0]+block[2] and posY+25 >= block[1] and posY < block[1]+block[3]:
                posX = 200
                posY = 550
                velX = 0
                velY = 0
                deaths += 1
                gameDisplay.fill(dark_red)
                pygame.display.update()
                clock.tick(20)
                timer+=1
                break
        for block in blocks:
            if posX+25 > block[0] and posX < block[0]+block[2] and posY+25 >= block[1] and posY < block[1]+block[3]:
                if posY-velY+25 <= block[1]:
                    posY = block[1]-25
                    velY = 0
                    ground = True
                    down = 2
                elif posY-velY > block[1]+block[3]:
                    posY = block[1]+block[3]
                    velY = 0
                elif posX-velX+25 <= block[0]:
                    posX = block[0]-25
                    velX = 0
                    wall[0] = True
                elif posX-velX >= block[0]+block[2]:
                    posX = block[0]+block[2]
                    velX = 0
                    wall[1] = True
        #check win
        if posX+35 >= keyX and posX <= keyX+30 and posY+35 >= keyY and posY <= keyY+10:
            return timer
        #draw
        gameDisplay.fill(backgroundcolor)
        #text
        for message in text:
            say(message[0], black, message[1], font1)
        say("Press q to quit", black, (105,25), font1)
        say(digtime(timer), black, (60,55), font1)
        say("level: "+str(level+1), black ,(60,80), font1)
        say("deaths: "+str(deaths), dark_red, (75,105), font1)
        #player
        pygame.draw.rect(gameDisplay, green, [posX, posY, 25, 25])
        #normal blocks
        for block in blocks:
            pygame.draw.rect(gameDisplay, dark_brown, block)
            #grass
            pygame.draw.rect(gameDisplay, dark_green, [block[0], block[1], block[2], 10])
            pygame.draw.rect(gameDisplay, dark_green, [block[0], block[1]+10, 10, 10])
            pygame.draw.rect(gameDisplay, dark_green, [block[0], block[1]+20, 5, 5])
            pygame.draw.rect(gameDisplay, dark_green, [block[0]+block[2]-10, block[1]+10, 10, 10])
            pygame.draw.rect(gameDisplay, dark_green, [block[0]+block[2]-5, block[1]+20, 5, 5])
            for i in range(block[2]//50):
                pygame.draw.rect(gameDisplay, dark_green, [block[0]+i*50+6.25, block[1]+10, 12.5, 5])
                pygame.draw.rect(gameDisplay, dark_green, [block[0]+i*50+31.25, block[1]+10, 12.5, 5])
        #red blocks
        for block in blocks2:
            pygame.draw.rect(gameDisplay, red, block)
        #key
        pygame.draw.circle(gameDisplay, yellow, [keyX, keyY], 10, 5)
        pygame.draw.rect(gameDisplay, yellow, [keyX+8, keyY-2.5, 22, 5])
        pygame.draw.rect(gameDisplay, yellow, [keyX+15, keyY+2.5, 10, 5])
        #show + wait
        pygame.display.update()
        clock.tick(20)
        timer += 1
def say(message, color, point, Font):
    font = pygame.font.SysFont(Font[0],Font[1])
    tekst = font.render(message, False, color)
    tekstRect = tekst.get_rect()
    tekstRect.center = point
    gameDisplay.blit(tekst, tekstRect)
def digtime(nr):
    return str(nr//1200)+":"+str(nr%1200//200)+str(nr%200//20)+","+str(nr%20//2)+str(nr%2*5)
#variables
gameDisplay = pygame.display.set_mode((1250, 650))
clock = pygame.time.Clock()
font1 = (None, 35)
besttimes = [False, False, False, False]
level  = 0
finished = 0
play = False
#colors
backgroundcolor = (40, 180, 200)
black = (0, 0, 0)
white = (255, 255, 255)
red = (223, 0, 0)
dark_red = (127, 0, 0)
green = (0, 255, 0)
dark_green = (0, 127, 0)
yellow = (255,255,0)
light_blue = (0, 255, 255)
dark_brown = (92, 64, 51)
while True:
    play = False
    #inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and level < finished:
                level += 1
            elif event.key == pygame.K_LEFT and level:
                level -= 1
            elif event.key == pygame.K_SPACE:
                play = True
    #play?
    if finished >= level and play:
        #levels
        if level == 0:
            blocks = [[0,600,400,50], [500,550,150,100],[750,450,200,50], [1050,400,100,40]]
            blocks2 = []
            text = [["use < > to move and ^ or space to jump",(350, 450)], ["Grab the key to win the level", (1000, 340)]]
            keyX = 1090
            keyY = 380
        elif level == 1:
            blocks = [[0,600,1250,50], [550,500,50,50], [800,400,50,50], [950,300,100,50], [550,200,150,50], [200,100,100,40]]
            blocks2 = [[680,445,100,50], [870,380,150,50], [720,220,100,50], [100,300,50,300]]
            text = [["If you touch a red block, you will die", (400, 350)]]
            keyX = 40
            keyY = 580
        elif level == 2:
            blocks = [[0,600,450,50], [650,550,50,100], [950,470,200,50], [1150,370,100,35], [900,265,50,35], [425,360,50,35], [200,265,100,35], [0,175,100,35], [250,100,50,35], [500,125,50,35], [800,100,50,35], [1100,100,100,40]]
            blocks2 = [[970,280,30,20], [1020,120,60,30]]
            text = [["Are you getting the hang of it?", (900, 200)]]
            keyX = 1140
            keyY = 80
        elif level == 3:
            blocks = [[200,600,50,50], [500,600,100,50]]
            blocks2 = [[200,450,400,50]]
            text = [["the last jump of level 3 to show it is possible", (400,400)]]
            keyX = 540
            keyY = 580
        #playing + screen afterwards
        time = playlevel()
        if time:
            if level == finished:
                finished += 1
                besttimes[level] = time
            elif besttimes[level] > time:
                besttimes[level] = time
            gameDisplay.fill(green)
            say("your time: "+digtime(time), black, (625,200), ("impact", 60))
            say("best time: "+digtime(besttimes[level]), black, (625,300), ("impact", 60))
            say("press space to continue", black, (625,450), ("arial", 30))
            pygame.display.update()
            exit = False
            while not exit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            exit = True
    #draw
    gameDisplay.fill(backgroundcolor)
    say("platformer", green, (625,100), ("impact", 100))
    for i in range(finished):
        pygame.draw.aaline(gameDisplay, white, (255+i*200,300), (395+i*200,300))
    color = green
    for i in range(4):
        pos = (225+i*200,300)
        if i == level:
            pygame.draw.rect(gameDisplay, white, [pos[0]-30,pos[1]-30,60,60])
        say(str(i+1), black, pos, ("arial", 50))
        if finished == i:
            color = red
        pygame.draw.aalines(gameDisplay, color, True, [(pos[0]-30,pos[1]-30),(pos[0]+30,pos[1]-30),(pos[0]+30,pos[1]+30),(pos[0]-30,pos[1]+30)])
        if besttimes[i]:
            say(digtime(besttimes[i]), black, (pos[0], pos[1]+50), (None, 30))
    if finished == 4:
        pygame.draw.rect(gameDisplay, green, [0,550,1250,100])
        say(digtime(besttimes[0]+besttimes[1]+besttimes[2]+besttimes[3]), black, (625,600), (None, 50))
    #throphy
    if finished == 4:
        color = yellow
    else:
        color = black
    pygame.draw.circle(gameDisplay, color, (995,260), 30, 3, False, False, True)
    pygame.draw.circle(gameDisplay, color, (1055,260), 30, 3, False, False, False, True)
    pygame.draw.circle(gameDisplay, color, (975,260), 10, 3, False, True)
    pygame.draw.circle(gameDisplay, color, (1075,260), 10, 3, True)
    pygame.draw.circle(gameDisplay, color, (1025,295), 30)
    pygame.draw.rect(gameDisplay, color, [995,245,60,50])
    pygame.draw.rect(gameDisplay, color, [1022,325,6,25])
    pygame.draw.rect(gameDisplay, color, [995,348,60,3])
    pygame.draw.rect(gameDisplay, color, [975,250,100,3])
    pygame.display.update()
    clock.tick(20)