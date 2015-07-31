import pygame, sys, math
from pygame.locals import *

pygame.init()

# set up constants
WIDTH = 1280
HEIGHT = 720

# set up game constants
ROTSPEED = 1
ROTDIR = 1 # CCW
MOVSPEED = 20

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
  def __init__(self, image_file, location):
    pygame.sprite.Sprite.__init__(self) # sprite initializer
    self.direction = 0 # direction sprite is facing (in degrees)
    self.spinning = True # if false, then must be moving
    self.image = pygame.image.load(image_file)
    self.rect = self.image.get_rect()
    self.rect.left, self.rect.top = location

  # tick the direction
  def tick_direction(self):
    self.direction = (self.direction +  ROTDIR * ROTSPEED) % 360 

 
  # tick the position (using direction)
  def tick_position(self):
    angle = math.radians(self.direction)
    velocity = (MOVSPEED*math.cos(angle), -MOVSPEED*math.sin(angle))
    print((sprite.rect.left, sprite.rect.top))
    sprite.rect.left, sprite.rect.top = tuple(map(sum, zip((sprite.rect.left, sprite.rect.top), velocity)))
    print((sprite.rect.left, sprite.rect.top))

  # tick sprite 
  def tick(self):
    if self.spinning:
      self.tick_direction()
    else:
      self.tick_position()

sprite = Sprite('assets/inmate0.png', [200, 200])

while True:
  # event handling
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      sprite.spinning = False
    elif event.type == pygame.KEYUP:
      sprite.spinning = True
    elif event.type == QUIT:
      pygame.quit()
      sys.exit()

  # updating
  sprite.tick()
 
  # drawing
  screen.fill(WHITE)
  screen.blit(BackGround.image, BackGround.rect)
  img = pygame.transform.rotate(sprite.image, sprite.direction)
  screen.blit(img, sprite.rect)
  pygame.display.update()
