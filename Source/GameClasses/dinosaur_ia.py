from IA.nn import NN
from constants import DINO_RUN, DINO_DOWN, DINO_JUMP
from constants import RED_DINO_RUN, RED_DINO_JUMP, RED_DINO_DOWN
from constants import GREEN_DINO_RUN, GREEN_DINO_JUMP, GREEN_DINO_DOWN
from constants import ORANGE_DINO_RUN, ORANGE_DINO_JUMP, ORANGE_DINO_DOWN
import numpy as np
import pygame


class DinosaurIA:
    def __init__(self, x_pos: int = 200, color: str = "grey"):
        # NN Dinosar
        self.neurons = NN(np.array([7, 5, 5, 2]))

        # Attributes to fitness Dinosar
        self.dead = False
        self.score = 0
        self.performance = 0

        # Colors
        if color == "grey":
            self.down_img = DINO_DOWN
            self.run_img = DINO_RUN
            self.jump_img = DINO_JUMP
        elif color == "red":
            self.down_img = RED_DINO_DOWN
            self.run_img = RED_DINO_RUN
            self.jump_img = RED_DINO_JUMP
        elif color == "green":
            self.down_img = GREEN_DINO_DOWN
            self.run_img = GREEN_DINO_RUN
            self.jump_img = GREEN_DINO_JUMP
        elif color == "orange":
            self.down_img = ORANGE_DINO_DOWN
            self.run_img = ORANGE_DINO_RUN
            self.jump_img = ORANGE_DINO_JUMP

        self.run = True
        self.down = False
        self.jump = False
        self.descend = False

        self.step_index = 0
        self.jump_vel = 6.5
        self.current_jump_vel = self.jump_vel
        self.current_down_vel = 0
        self.x_pos = x_pos
        self.y_pos = 560
        self.y_pos_down = 590

        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_down
        self.step_index += 1

    def down_dinosaur(self):
        self.image = self.down_img[self.step_index // 5]
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_down
        self.step_index += 1

    def run_dinosaur(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.step_index += 1

    def jump_dinosaur(self):
        self.image = self.jump_img
        if self.jump:
            self.dino_rect.y -= self.current_jump_vel * 1.5
            self.current_jump_vel -= 0.3
        if self.current_jump_vel < - self.jump_vel:
            self.jump = False
            self.current_jump_vel = self.jump_vel
            self.dino_rect.y = self.y_pos

    def descend_dinosaur(self):
        if self.jump and self.descend:
            self.dino_rect.y += self.current_down_vel * 2
            self.current_down_vel += 0.5

        if self.current_down_vel > self.jump_vel:
            self.jump = False
            self.descend = False
            self.current_jump_vel = self.jump_vel
            self.current_down_vel = 0
            self.dino_rect.y = self.y_pos

    def ia_move(self, key):
        # 0 = Jump, 1 = Down
        if self.down:
            self.down_dinosaur()

        if self.run:
            self.run_dinosaur()

        if self.jump and not self.descend:
            self.jump_dinosaur()

        if self.jump and self.descend:
            self.descend_dinosaur()

        if self.step_index >= 10 or self.jump:
            self.step_index = 0

        if key == 0 and not self.jump and not self.descend:
            self.down = False
            self.run = False
            self.jump = True
            self.descend = False

        elif key == 1 and not self.jump and not self.descend:
            self.down = True
            self.run = False
            self.jump = False
            self.descend = False

        elif key == 1 and self.jump and not self.descend:
            self.down = False
            self.run = False
            self.descend = True

        elif not (self.jump or key == 1) and not self.descend:
            self.down = False
            self.run = True
            self.jump = False
            self.descend = False

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def decision(self, input_array: np.array):
        return self.neurons.forward_nn(input_array)
