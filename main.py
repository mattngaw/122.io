import pygame
import Walls, Heroes, pickups

pygame.init()
screen = pygame.display.set_mode((1010, 510))
done = False
FPS = 60
clock = pygame.time.Clock()

players_list = pygame.sprite.Group()
plane = None
plane_list = pygame.sprite.Group()
pencil = None
pencil_list = pygame.sprite.Group()

player1 = Heroes.Taylor()
player1.rect.x = 50
player1.rect.y = 40
players_list.add(player1)

player2 = Heroes.Kosbie()
player2.rect.x = 900
player2.rect.y = 440
players_list.add(player2)
startImg= pygame.image.load('images/splashScreen.jpg')
startImg = pygame.transform.scale(startImg, (1010, 510))
intructionsImg = pygame.image.load('images/instructionsScreen.jpg')
intructionsImg = pygame.transform.scale(intructionsImg, (1010, 510))
gameover1=  pygame.image.load('images/gameover1.jpg')
gameover1 = pygame.transform.scale(gameover1, (1010, 510))
gameover2=  pygame.image.load('images/gameover2.jpg')
gameover2 = pygame.transform.scale(gameover2, (1010, 510))

def startScreen(screen, intro):
    while intro == True:
        screen.blit(startImg, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                intro = False
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
startScreen(screen, True)

def instructionsScreen(screen, start):
    while start == True:
        screen.blit(intructionsImg, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                start = False
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
instructionsScreen(screen, True)

def endScreen(name,screen):
    if name=="taylor":
        screen.blit(gameover2, (0,0))
        pygame.display.update()
    else:
        screen.blit(gameover1, (0,0))
        pygame.display.update()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.rect.y > 0: player1.direction[1] = 1
    elif keys[pygame.K_s] and player1.rect.y + 28 < 505: player1.direction[1] = -1
    else: player1.direction[1] = 0
    if keys[pygame.K_d] and player1.rect.x + 28 < 1005: player1.direction[0] = 1
    elif keys[pygame.K_a] and player1.rect.x > 0: player1.direction[0] = -1
    else: player1.direction[0] = 0
    if keys[pygame.K_SPACE]: 
        plane_list.empty()
        plane = player1.attack()
        plane_list.add(plane)

    if keys[pygame.K_UP] and player2.rect.y > 0: player2.direction[1] = 1
    elif keys[pygame.K_DOWN] and player2.rect.y + 28 < 505: player2.direction[1] = -1
    else: player2.direction[1] = 0
    if keys[pygame.K_RIGHT] and player2.rect.x + 28 < 1005: player2.direction[0] = 1
    elif keys[pygame.K_LEFT] and player2.rect.x > 0: player2.direction[0] = -1
    else: player2.direction[0] = 0
    if keys[pygame.K_RETURN]: 
        pencil_list.empty()
        pencil = player2.attack()
        pencil_list.add(pencil)

    if player1.direction != [0, 0]: player1.move()
    if player2.direction != [0, 0]: player2.move()

    for key in Walls.walls:
        x,y = Walls.getCellBounds(key[0],key[1])
        if pencil and Heroes.checkcollision(pencil.rect.x, pencil.rect.y, pencil.rect.width, pencil.rect.height, x, y, 20, 20):
            pencil_list.empty()
            pencil = None
        if plane and Heroes.checkcollision(plane.rect.x, plane.rect.y, plane.rect.width, plane.rect.height, x, y, 20, 20):
            plane_list.empty()
            plane = None

    if pencil and Heroes.checkcollision(pencil.rect.x, pencil.rect.y, pencil.rect.width, pencil.rect.height, player1.rect.x, player1.rect.y, 28, 28):
        player1.health -= pencil.damage - (player1.armor * 0.5)
        pencil = None
        pencil_list.empty()
    if plane and Heroes.checkcollision(plane.rect.x, plane.rect.y, plane.rect.width, plane.rect.height, player2.rect.x, player2.rect.y, 28, 28):
        player2.health -= plane.damage - (player2.armor * 0.5)
        plane = None
        plane_list.empty()

    if pencil: pencil.move()
    if plane: plane.move()

    screen.fill((0, 0, 0))
    Walls.redrawAll(screen)
    pickups.redrawAll(screen)
    players_list.draw(screen)
    plane_list.draw(screen)
    pencil_list.draw(screen)

    pygame.draw.rect(screen, (150,150,150), (player1.rect.x,player1.rect.y-5, 28, 5))
    pygame.draw.rect(screen, (255,0,0), (player1.rect.x,player1.rect.y-5,(28*(.01*player1.health)),5))
    pygame.draw.rect(screen, (150,150,150), (player2.rect.x,player2.rect.y-5,28, 5))
    pygame.draw.rect(screen, (255,0,0), (player2.rect.x,player2.rect.y-5, (28*(.01*player2.health)), 5))
    Heroes.hitBlue(player1, player1.rect.x,player1.rect.y, pickups.pickups)
    Heroes.hitHeart(player1,player1.rect.x,player1.rect.y, pickups.pickups )
    Heroes.hitBlue(player2, player2.rect.x,player2.rect.y, pickups.pickups)
    Heroes.hitHeart(player2,player2.rect.x,player2.rect.y, pickups.pickups )
    
    if player1.health<=0:
        endScreen("taylor",screen)
    elif player2.health<=0:
        endScreen("mike",screen)
    pygame.display.flip()
    clock.tick(FPS)
