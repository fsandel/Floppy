import pygame,sys
import random
import time

pygame.init()
Clock = pygame.time.Clock()
FPS = 60
size = [1000,800]
bg = [0,0,0]
white = (255, 255, 255)
blue = (173, 216, 230)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy bird")

def game_lost():
	sys.exit()

class Player:
	def __init__(self,x:int,y:int, move_key):
		self.vel_y = 0
		self.x = x
		self.y = y
		self.points = 0
		self.maxfallspeed = -15
		self.maxjumpspeed = 20
		self.jumpheight = 3
		self.fall_acc = 1
		self.image = pygame.image.load("./sprites/player.png")
		self.rect = self.image.get_rect()
		self.rect.center = [self.x, self.y]
		self.move_key = move_key

	def jump(self):
		k = pygame.key.get_pressed()
		if k[self.move_key] and self.vel_y < self.maxjumpspeed:
			if self.vel_y < 0:
				self.vel_y = 0
			self.vel_y += self.jumpheight

	def fall(self):
		if self.vel_y > self.maxfallspeed:
			self.vel_y -= self.fall_acc

	def move(self):
		self.y -= self.vel_y
		self.rect.center = [self.x, self.y]
		self.points += 1

	def draw(self):
		screen.blit(self.image, self.rect)


	def death(self):
		if self.y < 0 or self.y > 800:
			game_lost()

	def do(self):
		self.move()
		self.jump()
		self.draw()
		self.fall()
		self.death()

class Pipe(pygame.sprite.Sprite):
	def __init__(self, player_list, y):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 5
		self.x = size[0]
		self.size = 920
		self.gap = 400
		self.y = y
		
	def move(self):
		self.x -= self.speed
		self.rect.center = [self.x, self.y]

	def death(self, player_list):
		for player in player_list:
			if (self.rect.colliderect(player.rect)):
				game_lost()
	
	def delete(self):
		if self.x < -100:
			self.kill()

	def update(self):
		self.death(player_list)
		self.move()
		self.delete()

class DownPipe(Pipe):
	def __init__(self, player:Player, y:int):
		pygame.sprite.Sprite.__init__(self)
		Pipe.__init__(self, player, y)
		self.y += self.size / 2 + self.gap / 2
		self.image = pygame.image.load("./sprites/r_unten.png")
		self.rect = self.image.get_rect()
		self.rect.center = [self.x, self.y]

class UpPipe(Pipe):
	def __init__(self, player:Player, y:int):
		pygame.sprite.Sprite.__init__(self)
		Pipe.__init__(self, player, y)
		self.y -= (self.size / 2 + self.gap / 2)
		self.image = pygame.image.load("./sprites/r_oben.png")
		self.rect = self.image.get_rect()
		self.rect.center = [self.x, self.y]

class Cloud(pygame.sprite.Sprite):
	def __init__(self, y):
		pygame.sprite.Sprite.__init__(self)
		self.x = size[0]
		self.y = y
		self.speed = 2
		self.image = pygame.image.load("./sprites/cloud.png")
		self.rect = self.image.get_rect()
		self.rect.center = [self.x, self.y]
	
	def move(self):
		self.x -= self.speed
		self.rect.center = [self.x, self.y]

	def update(self):
		self.move()

class Background:
	def __init__(self):
		self.color = blue

	def draw(self):
		screen.fill(self.color)

	def do(self):
		self.draw()

cloud_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
background = Background()
player_list = [Player(size[0]/2, size[1]/2, pygame.K_UP), Player(size[0]/4, size[1]/2, pygame.K_w)]



def spawn_pipe(pipe_group:pygame.sprite.Group):
	y = random.randint(100, size[1] - 100)
	pipe_down_0 = DownPipe(player_list, y)
	pipe_up_0 = UpPipe(player_list, y)
	pipe_group.add(pipe_down_0)
	pipe_group.add(pipe_up_0)

def spawn_cloud(cloud_group:pygame.sprite.Group):
	y = random.randint(50, size[1] / 2)
	cloud = Cloud(y)
	cloud_group.add(cloud)

spawn_cloud(cloud_group)
spawn_pipe(pipe_group)
before = time.time()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
			sys.exit()

	background.do()
	cloud_group.draw(screen)
	cloud_group.update()
	after = time.time()
	if after > before + 1:
		spawn_cloud(pipe_group)
		spawn_pipe(pipe_group)
		before = after
	pipe_group.draw(screen)
	pipe_group.update()
	for player in player_list:
		player.do()

	Clock.tick(FPS)
	pygame.display.flip()
