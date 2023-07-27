from GameClasses.obstacle import Obstacle
from constants import LARGE_CACT
import random


class LargeCactus(Obstacle):
    def __init__(self, distance: int = 0):
        self.frame = random.randint(0, 2)
        super().__init__(LARGE_CACT, self.frame, distance)
        self.rect.y = 560
