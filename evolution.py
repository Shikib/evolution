import pygame, sys
from pygame.locals import *

pygame.init()

# set up constants
WIDTH = 1280
HEIGHT = 720

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

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  screen.fill(WHITE)
  screen.blit(BackGround.image, BackGround.rect)
  pygame.display.update()
