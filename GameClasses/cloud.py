from constants import CLOUD, WIDTH
import random


class Cloud:

    def __init__(self):
        self.x = WIDTH + random.randint(600, 1000)
        self.y = random.randint(20, 150)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, game_speed):
        self.x -= game_speed

        if self.x < -self.width:
            self.x = WIDTH + random.randint(2000, 3000)
            self.y = random.randint(350, 450)
