from GameClasses.obstacle import Obstacle
from constants import SMALL_CACT
import random


class SmallCactus(Obstacle):
    def __init__(self, distance: int = 0):
        self.frame = random.randint(0, 2)
        super().__init__(SMALL_CACT, self.frame, distance)
        self.rect.y = 565
        