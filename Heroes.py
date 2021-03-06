import pygame
import os
import math
import weapons
import Walls

def checkcollision(x,y,w,h,x2,y2,w2,h2):
    if x + w >= x2 and y + h >= y2 and x <= x2 + w2 and y <= y2 + h2:
        return True
    else:
        return False

def hitBlue(player, x, y, s):
    L = list(s["SizeBoosters"])
    i = 0
    while i < len(L):
        (x1,y1)= Walls.getCellBounds(L[i][0], L[i][1])
        if checkcollision(x, y, 28, 28, x1,y1, 20, 20):
            L.pop(i)
            s["SizeBoosters"]= L
            player.armor += 1
        else:
            i += 1
    
def hitHeart(player, x, y, s):
    L = list(s["Hearts"])
    i = 0
    while i < len(L):
        (x1,y1)= Walls.getCellBounds(L[i][0], L[i][1])
        if checkcollision(x, y, 28, 28, x1,y1, 20, 20):
            L.pop(i)
            s["Hearts"]= L
            if player.health<=90:
                player.health += 10
            elif player.health>90:
                player.health+=(100-player.health)
        else:
            i += 1
class Hero(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.dx = 0
        self.dy = 0
        self.speed = 3
        self.health = 100
        self.armor = 0
        self.direction = [0, 0] # dx, dy
        self.facing = [0, -1]
        self.images = []
        for i in range(4):
            img = pygame.image.load(os.path.join("images", f"{self.name}{str(i)}.png"))
            img = pygame.transform.scale(img,(28,28))
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.y = 0

    def move(self):
        angles = [
            [None,  270,    90],
            [0,     315,    45],
            [180,   225,    135]
        ]
        i, j = self.direction
        if i == 0 and j == 1: 
            self.facing = [0, 1]
            self.image = self.images[3]
        if i == 0 and j == -1: 
            self.facing = [0, -1]
            self.image = self.images[0]
        if i == 1 and j == 0: 
            self.facing = [1, 0]
            self.image = self.images[1]
        if i == -1 and j == 0: 
            self.facing = [-1, 0]
            self.image = self.images[2]
        angle = angles[i][j] * math.pi / 180
        self.dx = self.speed * math.cos(angle)
        self.dy = self.speed * math.sin(angle)
        self.rect.x += self.dx
        self.rect.y += self.dy
        for key in Walls.walls:
            x,y = Walls.getCellBounds(key[0],key[1])
            if checkcollision(self.rect.x, self.rect.y, 28, 28, x, y, 20, 20):
                self.rect.x -= self.dx
                self.rect.y -= self.dy

        if self.rect.x<5 or self.rect.y<5:
            self.rect.x -= self.dx
            self.rect.y -= self.dy
        if self.rect.x>980 or self.rect.y>480:
            self.rect.x -= self.dx
            self.rect.y -= self.dy
            
class Kosbie(Hero):
    def __init__(self):
        self.name = "koz"
        Hero.__init__(self)

    #def attack(self, projectilesList):
    def attack(self):
        return weapons.Pencil(self.rect.x, self.rect.y, self.facing)
        #projectilesList.append(Pencil(self.rect.x, self.rect.y, self.facing))

class Taylor(Hero):
    def __init__(self):
        self.name = "taylor"
        Hero.__init__(self)

    #def attack(self, projectilesList):
    def attack(self):
        return weapons.Plane(self.rect.x, self.rect.y, self.facing)
        #projectilesList.append(Plane(self.rect.x, self.rect.y, self.facing))
