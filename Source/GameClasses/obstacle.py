from constants import WIDTH
import pygame


class Obstacle:

    def __init__(self, image, frame: int, distance):
        self.distance = distance
        self.image = image
        self.frame = frame
        self.rect = self.image[self.frame].get_rect()
        self.rect.x = WIDTH + self.distance

    def update(self, list_obstacles, game_speed, idx):
        self.rect.x -= game_speed
        if self.rect.x < - self.image[self.frame].get_width():
            list_obstacles.pop(idx)

    def get_mask(self):
        return pygame.mask.from_surface(self.image[self.frame])
