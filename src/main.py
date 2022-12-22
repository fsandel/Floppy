import pygame,sys
import random

pygame.init()
Clock = pygame.time.Clock()
FPS = 60
size = [1000,800]
bg = [0,0,0]
white = (255, 255, 255)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy bird")

class Player:
    def __init__(self,x,y):
        self.vel_y = 0
        self.x = x
        self.y = y
        self.maxfallspeed = -15
        self.maxjumpspeed = 20
        self.jumpheight = 3
        self.fall_acc = 1
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

    def jump(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_UP] and self.vel_y < self.maxjumpspeed:
            if self.vel_y < 0:
                self.vel_y = 0
            self.vel_y += self.jumpheight

    def fall(self):
        if self.vel_y > self.maxfallspeed:
            self.vel_y -= self.fall_acc

    def move(self):
        self.y -= self.vel_y
        self.rect.center = [self.x, self.y]

    def draw(self):
        #pygame.draw.rect(screen,white,(self.x,self.y,50,50))
        screen.blit(self.image, self.rect)


    def death(self):
        if self.y < 0 or self.y > 800:
            pygame.quit()

    def do(self):
        self.move()
        self.jump()
        self.draw()
        self.fall()
        self.death()

class Pipe:
    def __init__(self, start_x, player:Player):
        self.speed = 5
        self.weidth = 40
        self.x = size[0] + start_x
        self.gap = 100
        self.y = random.randint(self.gap * 2, size[0] - self.gap * 2)
        self.hitbox_x = 50
        self.image = pygame.image.load("both.png")
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        
    def move(self):
        self.x -= self.speed
        self.rect.center = [self.x, self.y]

    def draw(self):
        screen.blit(self.image, self.rect)

    def reset(self):
        if self.x < 1:
            self.x = size[0]
            self.y = random.randint(self.gap * 2, size[0] - self.gap * 2)

    def death(self, player:Player):
        if abs(player.x - self.x) < self.hitbox_x:
            if (player.y > self.y + self.gap) or (player.y < self.y - self.gap):
                pygame.quit()

    def do(self):
        self.death(player)
        self.move()
        self.draw()
        self.reset()


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int):
        self.color = (255, 255, 255)
        self.x = x
        self.y = y
        self.radius = 20
        self.width = 50
        self.speed = 2
        self.image = pygame.image.load("cloud.png")
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
    
    def move(self):
        self.x -= self.speed
        self.rect.center = [self.x, self.y]


    def draw(self):
        screen.blit(self.image, self.rect)

    def reset(self):
        if self.x < -self.width:
            self.x = size[0]
            self.rect.center = [self.x, self.y]

    
    def do(self):
        self.draw()
        self.move()
        self.reset()


class Background:
    def __init__(self):
        self.color = (173, 216, 230)

    def draw(self):
        screen.fill(self.color)

    def do(self):
        self.draw()

#cloud_group = pygame.sprite.Group()
cloud1 = Cloud(size[0]/2, size[1]/8)
cloud2 = Cloud(size[0], size[1]/8)
cloud3 = Cloud(size[0]/4*3, size[1]/3)
cloud4 = Cloud(size[0]/4, size[1]/3)
#cloud_group.add(cloud1)
#cloud_group.add(cloud2)
#cloud_group.add(cloud3)
#cloud_group.add(cloud4)


background = Background()
player = Player(size[0]/2, size[1]/2)
pipe0 = Pipe(0, player)
pipe1 = Pipe(size[0]/3, player)
pipe2 = Pipe(size[0]/3*2, player)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    background.do()
    #cloud_group.draw(screen)
    cloud1.do()
    cloud2.do()
    cloud3.do()
    cloud4.do()
    player.do()
    pipe0.do()
    pipe1.do()
    pipe2.do()

    Clock.tick(FPS)
    pygame.display.flip()
