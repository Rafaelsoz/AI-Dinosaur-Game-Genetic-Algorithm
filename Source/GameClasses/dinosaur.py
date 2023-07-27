from constants import DINO_RUN, DINO_DOWN, DINO_JUMP
import pygame


class Dinosaur:
    def __init__(self):
        self.down_img = DINO_DOWN
        self.run_img = DINO_RUN
        self.jump_img = DINO_JUMP

        self.run = True
        self.down = False
        self.jump = False
        self.descend = False

        self.step_index = 0
        self.jump_vel = 6.5
        self.current_jump_vel = self.jump_vel
        self.current_down_vel = 0
        self.x_pos = 80
        self.y_pos = 310
        self.y_pos_down = 340

        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
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
            self.dino_rect.y -= self.current_jump_vel * 2
            self.current_jump_vel -= 0.55
        if self.current_jump_vel < - self.jump_vel:
            self.jump = False
            self.current_jump_vel = self.jump_vel
            self.dino_rect.y = self.y_pos

    def descend_dinosaur(self):
        if self.jump and self.descend:
            self.dino_rect.y += self.current_down_vel * 3
            self.current_down_vel += 0.8

        if self.current_down_vel > self.jump_vel:
            self.jump = False
            self.descend = False
            self.current_jump_vel = self.jump_vel
            self.current_down_vel = 0
            self.dino_rect.y = self.y_pos

    def move(self, key):
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

        if key[pygame.K_UP] and not self.jump and not self.descend:
            self.down = False
            self.run = False
            self.jump = True
            self.descend = False

        elif key[pygame.K_DOWN] and not self.jump and not self.descend:
            self.down = True
            self.run = False
            self.jump = False
            self.descend = False

        elif key[pygame.K_DOWN] and self.jump and not self.descend:
            self.down = False
            self.run = False
            self.descend = True

        elif not(self.jump or key[pygame.K_DOWN]) and not self.descend:
            self.down = False
            self.run = True
            self.jump = False
            self.descend = False

    def get_mask(self):
        return pygame.mask.from_surface(self.image)
