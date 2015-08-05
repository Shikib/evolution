import pygame, sys, math
from pygame.locals import *
from random import randint

pygame.init()

# set up constants
WIDTH = 1280
HEIGHT = 720

# set up game constants
ROTSPEED = 1
ROTDIR = 1 # CCW
MOVSPEED = 5
RADIUS = 30

LEFTPOS = (200, 200)
LEFTANG = 0
RIGHTPOS = (600, 200)
RIGHTANG = 180

# set up board boundaries
LEFTBOUND = 0
RIGHTBOUND = 900
UPBOUND = 0
DOWNBOUND = 400

# set up FPS
FPS = 60
fpsClock = pygame.time.Clock()

# set up drawing constants
WALKTIME = FPS / 3
NOARMSTIME = 6

# set up window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('evolution')

# set up colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Background initialization
class Background(pygame.sprite.Sprite):
  def __init__(self, image_file, location):
    pygame.sprite.Sprite.__init__(self) # sprite initializer
    self.image = pygame.image.load(image_file)
    self.rect = self.image.get_rect()
    self.rect.left, self.rect.top = location

BackGround = Background('assets/background3.png', [0, 0])

# Background initialization
class Background(pygame.sprite.Sprite):
  def __init__(self, image_file, location):
    pygame.sprite.Sprite.__init__(self) # sprite initializer
    self.image = pygame.image.load(image_file)
    self.rect = self.image.get_rect()
    self.rect.left, self.rect.top = location

BackGround = Background('assets/background3.png', [0, 0])

# Sprite initialization
class Sprite(pygame.sprite.Sprite):
  # image_file refers to the image for the sprite,
  # image_walk1 refers to walking image 1 
  # image_walk2 refers to walking image 2
  # side is true if sprite is on the left, false if on the right
  # cop is true if sprite is cop, false if robber
  def __init__(self, image_file, image_walk1, image_walk2, side, cop):
    pygame.sprite.Sprite.__init__(self) # sprite initializer
    # game fields
    self.spinning = True # if false, then must be moving
    self.cop = cop
    self.score = 0
    # drawing fields
    self.image = pygame.image.load(image_file)
    self.walkimg = pygame.image.load(image_walk1)
    self.walkimg2 = pygame.image.load(image_walk2)
    self.rect = self.image.get_rect()
    self.walkit = 0 # walk iteration
    self.init_position(side)

  # initialize sprite position (left/right)
  def init_position(self, side):
    if (side):
      self.rect.left, self.rect.top = LEFTPOS
      self.direction = LEFTANG
    else:
      self.rect.left, self.rect.top = RIGHTPOS
      self.direction = RIGHTANG

  # correct the position in case that sprite is out of bounds
  def correct_position(self):
    print(police.rect.bottom)
    print(police.rect.right)
    if self.rect.left < LEFTBOUND:
      self.rect.left = LEFTBOUND
    if self.rect.right > RIGHTBOUND:
      self.rect.right = RIGHTBOUND
    if self.rect.top < UPBOUND:
      self.rect.top = UPBOUND
    if self.rect.bottom > DOWNBOUND:
      self.rect.bottom = DOWNBOUND


  # tick the direction
  def tick_direction(self):
    self.direction = (self.direction +  ROTDIR * ROTSPEED) % 360 

 
  # tick the position (using direction)
  def tick_position(self):
    angle = math.radians(self.direction)
    velocity = (MOVSPEED*math.cos(angle), -MOVSPEED*math.sin(angle))
    self.rect.left, self.rect.top = tuple(map(sum, zip((self.rect.left, self.rect.top), velocity)))
    self.correct_position() 

  # tick walk iteration (used in drawing):
  def tick_walkit(self):
    self.walkit = (self.walkit + 1) % WALKTIME 

  # tick sprite 
  def tick(self):
    if self.spinning:
      self.tick_direction()
    else:
      self.tick_position()
    self.tick_walkit() 

  # rotate sprite image
  def rotate_img(self, img):
    img = pygame.transform.rotate(img, self.direction)
    self.rect = img.get_rect(center=self.rect.center)
    return img

  def draw(self):
    if self.spinning:
      img = self.rotate_img(self.image)
    elif self.walkit < WALKTIME / 2 - NOARMSTIME / 2:
      img = self.rotate_img(self.walkimg)
    elif self.walkit < WALKTIME / 2 + NOARMSTIME / 2:
      img = self.rotate_img(self.image)
    else:
      img = self.rotate_img(self.walkimg2)

    screen.blit(img, self.rect)
  
# check collision between police and robber
def check_collision():
  dx = police.rect.center[0] - robber.rect.center[0]
  dy = police.rect.center[1] - robber.rect.center[1]
  return (dx**2 + dy**2)**0.5 <= 2*RADIUS


# handle collision by resetting to initial positions
def handle_collision():
  pos = randint(0, 1)
  robber.init_position(pos)
  police.init_position(not pos)


# init game
pos = randint(0, 1)
robber = Sprite('assets/inmate0.png', 'assets/inmate1.png', 'assets/inmate2.png', pos, False)
police = Sprite('assets/police0.png', 'assets/police1.png', 'assets/police2.png', not pos, True)

while True:
  # event handling
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      robber.spinning = False
      police.spinning = False
    elif event.type == pygame.KEYUP:
      robber.spinning = True
      police.spinning = True
    elif event.type == QUIT:
      pygame.quit()
      sys.exit()

  # updating
  robber.tick()
  police.tick()

  # check for collision
  if (check_collision()):
    handle_collision()

  # drawing
  screen.fill(WHITE)
  screen.blit(BackGround.image, BackGround.rect)
  robber.draw()
  police.draw()

  pygame.display.update()
  fpsClock.tick(FPS)
