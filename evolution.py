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
MOVSPEED = 20
RADIUS = 40

LEFTPOS = (200, 200)
LEFTANG = 0
RIGHTPOS = (600, 200)
RIGHTANG = 180

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
  # image_file refers to the image for the sprite
  # side is true if sprite is on the left, false if on the right
  # cop is true if sprite is cop, false if robber
  def __init__(self, image_file, side, cop):
    pygame.sprite.Sprite.__init__(self) # sprite initializer
    self.spinning = True # if false, then must be moving
    self.cop = cop
    self.image = pygame.image.load(image_file)
    self.rect = self.image.get_rect()
    self.init_position(side)

  # initialize sprite position (left/right)
  def init_position(self, side):
    if (side):
      self.rect.left, self.rect.top = LEFTPOS
      self.direction = LEFTANG
    else:
      self.rect.left, self.rect.top = RIGHTPOS
      self.direction = RIGHTANG

  # tick the direction
  def tick_direction(self):
    self.direction = (self.direction +  ROTDIR * ROTSPEED) % 360 

 
  # tick the position (using direction)
  def tick_position(self):
    angle = math.radians(self.direction)
    velocity = (MOVSPEED*math.cos(angle), -MOVSPEED*math.sin(angle))
    self.rect.left, self.rect.top = tuple(map(sum, zip((self.rect.left, self.rect.top), velocity)))

  # tick sprite 
  def tick(self):
    if self.spinning:
      self.tick_direction()
    else:
      self.tick_position()

  # rotate sprite image
  def rotate_img(self):
    img = pygame.transform.rotate(self.image, self.direction)
    self.rect = img.get_rect(center=self.rect.center)
    return img

  def draw(self):
    img = self.rotate_img()
    screen.blit(img, self.rect)
  
# p and q represent two sprites
def check_collision(p, q):
  dx = q.rect.center[0] - p.rect.center[0]
  dy = q.rect.center[1] - p.rect.center[1]
  if (dx**2 + dy**2)**0.5 <= 2*RADIUS:
    print("collision")

pos = randint(0, 1)
robber = Sprite('assets/inmate0.png', pos, False)
police = Sprite('assets/police0.png', not pos, True)

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
  check_collision(robber, police)

  # drawing
  screen.fill(WHITE)
  screen.blit(BackGround.image, BackGround.rect)
  robber.draw()
  police.draw()
  pygame.display.update()
