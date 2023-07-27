import pygame


HEIGHT = 700
WIDTH = 1500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DINO = pygame.image.load('Assets/Dino/Grey/Dino.png')
DINO_DEAD = pygame.image.load('Assets/Dino/Grey/Dino_dead.png')
DINO_DOWN = [pygame.image.load('Assets/Dino/Grey/Dino_down1.png'),
             pygame.image.load('Assets/Dino/Grey/Dino_down2.png')]
DINO_JUMP = pygame.image.load('Assets/Dino/Grey/Dino_jump.png')
DINO_RUN = [pygame.image.load('Assets/Dino/Grey/Dino_run1.png'),
            pygame.image.load('Assets/Dino/Grey/Dino_run2.png')]

GREEN_DINO = pygame.image.load('Assets/Dino/Green/Dino.png')
GREEN_DINO_DEAD = pygame.image.load('Assets/Dino/Green/Dino_dead.png')
GREEN_DINO_DOWN = [pygame.image.load('Assets/Dino/Green/Dino_down1.png'),
                   pygame.image.load('Assets/Dino/Green/Dino_down2.png')]
GREEN_DINO_JUMP = pygame.image.load('Assets/Dino/Green/Dino_jump.png')
GREEN_DINO_RUN = [pygame.image.load('Assets/Dino/Green/Dino_run1.png'),
                  pygame.image.load('Assets/Dino/Green/Dino_run2.png')]

RED_DINO = pygame.image.load('Assets/Dino/Red/Dino.png')
RED_DINO_DEAD = pygame.image.load('Assets/Dino/Red/Dino_dead.png')
RED_DINO_DOWN = [pygame.image.load('Assets/Dino/Red/Dino_down1.png'),
                 pygame.image.load('Assets/Dino/Red/Dino_down2.png')]
RED_DINO_JUMP = pygame.image.load('Assets/Dino/Red/Dino_jump.png')
RED_DINO_RUN = [pygame.image.load('Assets/Dino/Red/Dino_run1.png'),
                pygame.image.load('Assets/Dino/Red/Dino_run2.png')]

SMALL_CACT = [pygame.image.load('Assets/Cactus/Small_cactus1.png'),
              pygame.image.load('Assets/Cactus/Small_cactus2.png'),
              pygame.image.load('Assets/Cactus/Small_cactus3.png')]

ORANGE_DINO = pygame.image.load('Assets/Dino/Orange/Dino.png')
ORANGE_DINO_DEAD = pygame.image.load('Assets/Dino/Orange/Dino_dead.png')
ORANGE_DINO_DOWN = [pygame.image.load('Assets/Dino/Orange/Dino_down1.png'),
                    pygame.image.load('Assets/Dino/Orange/Dino_down2.png')]
ORANGE_DINO_JUMP = pygame.image.load('Assets/Dino/Orange/Dino_jump.png')
ORANGE_DINO_RUN = [pygame.image.load('Assets/Dino/Orange/Dino_run1.png'),
                   pygame.image.load('Assets/Dino/Orange/Dino_run2.png')]

LARGE_CACT = [pygame.transform.scale(pygame.image.load('Assets/Cactus/Large_cactus1.png'), (24, 48)),
              pygame.transform.scale(pygame.image.load('Assets/Cactus/Large_cactus2.png'), (50, 48)),
              pygame.transform.scale(pygame.image.load('Assets/Cactus/Large_cactus3.png'), (65, 48))]

BIRD = [pygame.image.load('Assets/Bird/Bird1.png'), pygame.image.load('Assets/Bird/Bird2.png')]

CLOUD = pygame.image.load('Assets/Scenery/Cloud.png')

PATH = pygame.image.load('Assets/Scenery/Path.png')

RESET = pygame.transform.scale(pygame.image.load('Assets/Scenery/Reset.png'), (150, 180))
