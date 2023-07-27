from GameClasses.obstacle import Obstacle
from constants import BIRD
import numpy as np


class Bird(Obstacle):
    def __init__(self, distance: int = 0):
        super().__init__(BIRD, 0, distance)
        self.frame = 0
        self.rect.y = np.random.randint(475, 530)
        self.index = 0
