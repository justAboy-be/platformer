#klaarzetten
import pygame
pygame.init()
#variabelen
gameDisplay = pygame.display.set_mode((1250, 650))
gameExit = False
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
blocks = [[0,600,1250,50], [400,500,200,80],[600,300,650,180]]
blocks2 = []
keyX = 1100
keyY = 280
coordX = 200
coordY = 550
snelheidX = 0
snelheidY = 0
wall = [False, False]
richting = False
jump = False
ground = False
down = 1
level = 0
#kleuren
achtergrondkleur = (40, 180, 255)
zwart = (0, 0, 0)
wit = (255, 255, 255)
rood = (255, 0, 0)
blauw = (0, 255, 0)
lichtblauw = (0,255, 255)
groen = (0, 0, 255)
geel = (255,255,0)
#functies
def bericht(bericht, kleur, punt):
    tekst = font.render(bericht, False, kleur)
    tekstRect = tekst.get_rect()
    tekstRect.center = punt
    gameDisplay.blit(tekst, tekstRect)
#het spelen
while not gameExit:
    #inputs verwerken
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                richting = "r"
            elif event.key == pygame.K_LEFT:
                richting = "l"
            elif event.key == pygame.K_UP and ground == True:
                jump = True
                ground = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                richting = False
            elif event.key == pygame.K_UP:
                down = 3
    #snelheid aanpassen
    if jump:
        snelheidY = -20
        jump = False
    elif not ground:
        if snelheidY > -5:
            down = 3
        if snelheidY+down < 20:
            snelheidY += down
        else:
            snelheidY = 20
    if richting == "r" and wall[0] == False:
        if snelheidX < 0:
            snelheidX += 4
        elif snelheidX < 18:
            snelheidX += 2
            wall[1] = False
        else:
            snelheidX = 20
    elif richting == "l" and wall[1] == False:
        if snelheidX > 0:
            snelheidX += -4
        elif snelheidX > -18:
            snelheidX += -2
            wall[0] = False
        else:
            snelheidX = -20
    else:
        if snelheidX < 0:
            snelheidX += 1
        elif snelheidX > 0:
            snelheidX += -1
    #bewegen
    coordX += snelheidX
    coordY += snelheidY
    #positie corrigeren
    if coordX < 0 or coordX > 1225 or coordY < 0:
        coordX = 400
        coordY = 550
        snelheidX = 0
        snelheidY = 0
    else:    
        ground = False
        wall = [False,False]
        for block in blocks2:
            if coordX+25 > block[0] and coordX < block[0]+block[2] and coordY+25 >= block[1] and coordY < block[1]+block[3]:
                coordX = 400
                coordY = 550
                snelheidX = 0
                snelheidY = 0
        for block in blocks:
            if coordX+25 > block[0] and coordX < block[0]+block[2] and coordY+25 >= block[1] and coordY < block[1]+block[3]:
                if coordY < block[1]:
                    coordY = block[1]-25
                    snelheidY = 0
                    ground = True
                    down = 1
                elif coordY+25 > block[1]+block[3]:
                    coordY = block[1]+block[3]
                    snelheidY = 0
                elif coordX < block[0]:
                    coordX = block[0]-25
                    snelheidX = 0
                    richting = False
                    wall[0] = True
                elif coordX+25 > block[0]+block[2]:
                    coordX = block[0]+block[2]
                    snelheidX = 0
                    richting = False
                    wall[1] = True
    #levelup checken
    if coordX+25 >= keyX and coordX < keyX+10 and coordY+25 >= keyY and coordY < keyY+10:
        if level == 1:
            level = 0
        else:
            level += 1
        if level == 0:
            blocks = [[0,600,1250,50], [400,500,200,80],[600,300,650,180]]
            blocks2 = []
            keyX = 1100
            keyY = 280
        elif level == 1:
            blocks = [[0,600,1250,50], [300,400,100,50], [200,200,100,50], [450,500,50,50], [900,450,100,50], [700,300,100,50], [700,545,150,50]]
            blocks2 = [[575,275,100,50], [100,400,100,50]]
            keyX = 245
            keyY = 180
    #tekenen
    gameDisplay.fill(achtergrondkleur)
    for block in blocks:
        pygame.draw.rect(gameDisplay, lichtblauw, block)
    for block in blocks2:
        pygame.draw.rect(gameDisplay, rood, block)
    pygame.draw.rect(gameDisplay, blauw, [coordX,coordY,25,25])
    pygame.draw.rect(gameDisplay, geel, [keyX,keyY,10,10])
    pygame.display.update()
    clock.tick(20)
pygame.quit()
quit()
