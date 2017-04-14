import pygame, sys
from pygame.locals import *

Sprite = pygame.sprite.Sprite
Surface = pygame.Surface
Rect = pygame.Rect

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
DISPLAY = [WIN_WIDTH, WIN_HEIGHT]

YELLOW = (255,255,0)
RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (200,200,200)

LEVEL = [
		"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
		"W                                          W",
		"W                                          W",
		"W                                          W",
		"W                    PPPPPPPPPPP           W",
		"W                                          W",
		"W                                          W",
		"W                                          W",
		"W    PPPPPPPP                              W",
		"W                                          W",
		"W                          PPPPPPP         W",
		"W                 PPPPPP                   W",
		"W                                          W",
		"W         PPPPPPP                          W",
		"W                                          W",
		"W                     PPPPPP               W",
		"W                                          W",
		"W   PPPPPPPPPPP                            W",
		"W                                          W",
		"W                 PPPPPPPPPPP              W",
		"W                                          W",
		"W                                          W",
		"W                                          W",
		"W                                          W",
		"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",]

LEVEL_WIDTH  = len(LEVEL[0]) * 32
LEVEL_HEIGHT = len(LEVEL) * 32

# BACKGROUND_TILE.fill(BLACK)

class Camera():
	def __init__(self):
		self.offset = [0,0]

	def update(self, player):
		x = player.rect.x
		y = player.rect.y
		offset_x = -x + HALF_WIDTH
		offset_y = -y + HALF_HEIGHT

		offset_x = min(0, offset_x)
		offset_x = max(-LEVEL_WIDTH + WIN_WIDTH, offset_x)

		offset_y = min(0, offset_y)
		offset_y = max(-LEVEL_HEIGHT + WIN_HEIGHT, offset_y)

		self.offset = [offset_x, offset_y]

	def apply(self, target):
		updated_x = target.rect.x + self.offset[0]
		updated_y = target.rect.y + self.offset[1]
		return [updated_x, updated_y]

class Player(Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load('./assets/player.png').convert_alpha()
		# self.image.fill(BLUE)
		# self.image.convert()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.xspeed = 0
		self.yspeed = 0
		self.onGround = False

	def update(self, platforms):
		# increment and correct movement in x direction
		self.rect.x += self.xspeed
		self.correct_x(platforms)
		
		# increment and correct movement in y direction
		self.rect.y += self.yspeed
		self.onGround = False;
		self.correct_y(platforms)

		# apply gravity
		if not self.onGround:
			self.yspeed += 0.3

	def correct_x(self, platforms):
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				if self.xspeed > 0:
					self.rect.right = p.rect.left
				if self.xspeed < 0:
					self.rect.left = p.rect.right

	def correct_y(self, platforms):
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				if self.yspeed > 0:
					self.rect.bottom = p.rect.top
					self.onGround = True
					self.yspeed = 0
				if self.yspeed < 0:
					self.rect.top = p.rect.bottom

class Platform(Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load('./assets/grass_32x32.png').convert()
		# self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

class Wall(Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load('./assets/dirt_32x32.png').convert()
		# self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

# Initial pygame and game objects
pygame.init()
pygame.mixer.init()
jump_sound = pygame.mixer.Sound('./assets/jump.wav')
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Use arrows to move!")
clock = pygame.time.Clock()
camera = Camera()
BACKGROUND_TILE = pygame.image.load('./assets/background.png').convert()

# Create sprite collections
entities = pygame.sprite.Group()
platforms = []

# Create and add player sprite
player = Player(32, 32)
entities.add(player)

# Create and add level sprites
x = 0
y = 0
for row in LEVEL:
	for col in row:
		if col == "P":
			p = Platform(x, y)
			platforms.append(p)
			entities.add(p)
		if col == "W":
			w = Wall(x, y)
			platforms.append(w)
			entities.add(w)
		x += 32
	y += 32
	x = 0


# GAME LOOP

while True:
	# GET USER INPUT
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()

	pressed = pygame.key.get_pressed()

	if pressed[K_UP]:
		if player.onGround:
			jump_sound.play()
			player.yspeed = -10
			
	if pressed[K_LEFT]:
		player.xspeed = -8
	elif pressed[K_RIGHT]:
		player.xspeed = 8
	else:
		player.xspeed = 0

	# UPDATE DATA
	camera.update(player)
	player.update(platforms)

	# DRAW
	for y in range(32):
		for x in range(32):
			screen.blit(BACKGROUND_TILE, (x * 32, y * 32))

	for e in entities:
		screen.blit(e.image, camera.apply(e))

	pygame.display.update()

	clock.tick(60)
