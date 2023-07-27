from GameClasses.dinosaur import Dinosaur
from GameClasses.cloud import Cloud
from GameClasses.bird import Bird
from GameClasses.smallcactus import SmallCactus
from GameClasses.largecactus import LargeCactus
from constants import PATH, DINO_DEAD, BLACK, RESET, WIDTH, WHITE
import pygame
import random


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.obstacles = []
        self.game_speed = 10
        self.game_max_speed = 30.0
        self.x_background = 0
        self.y_background = 580
        self.score = 0
        self.hi_score = 0

        self.reset_img = RESET
        self.reset_rect = self.reset_img.get_rect()
        self.reset_rect.x = 680
        self.reset_rect.y = 200
        self.pause = False

        self.dinosaur = Dinosaur()
        self.clouds = [Cloud(), Cloud(), Cloud(), Cloud(), Cloud(), Cloud(), Cloud(), Cloud(), Cloud()]

    def game_reset(self):
        self.obstacles = []
        self.game_speed = 10
        self.x_background = 0
        self.hi_score = self.hi_score if self.score <= self.hi_score else self.score
        self.score = 0

        self.pause = False

        self.dinosaur = Dinosaur()

    def draw_dinosaur(self):
        self.screen.blit(self.dinosaur.image, (self.dinosaur.dino_rect.x,
                                               self.dinosaur.dino_rect.y))

    def draw_death_dinosaur(self):
        self.screen.blit(DINO_DEAD, (self.dinosaur.dino_rect.x,
                                     self.dinosaur.dino_rect.y))

    def draw_cloud(self):
        for cloud in self.clouds:
            self.screen.blit(cloud.image, (cloud.x, cloud.y))

    def draw_bird(self, bird: Bird):
        if bird.index >= 9:
            bird.index = 0
        self.screen.blit(bird.image[bird.index//5], bird.rect)
        bird.index += 1

    def draw_obstacle(self):
        for obstacle in self.obstacles:
            if isinstance(obstacle, Bird) and not self.pause:
                self.draw_bird(obstacle)
            else:
                self.screen.blit(obstacle.image[obstacle.frame], obstacle.rect)

    def draw_hi_score(self, x: int = 800, y: int = 30):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Hi-Score: " + str(self.hi_score), True, BLACK)
        self.screen.blit(text, (x, y))

    def draw_score(self, x: int = 1000, y: int = 30):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Score: " + str(self.score), True, BLACK)
        self.screen.blit(text, (x, y))

    def draw_speed(self, x: int = 1200, y: int = 30):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Speed: " + str(round(self.game_speed, 1)), True, BLACK)
        self.screen.blit(text, (x, y))

    def draw_background(self):
        image_width = PATH.get_width()
        self.screen.blit(PATH, (self.x_background, self.y_background))
        self.screen.blit(PATH, (image_width + self.x_background, self.y_background))

        if self.x_background <= - image_width:
            self.screen.blit(PATH, (image_width + self.x_background, self.y_background))
            self.x_background = 0

        self.x_background -= self.game_speed

    def draw_game(self):
        self.screen.fill(WHITE)
        self.draw_background()
        self.draw_obstacle()
        self.draw_cloud()
        self.draw_hi_score()
        self.draw_score()
        self.draw_speed()
        self.draw_dinosaur()

    def draw_game_over(self):
        self.game_speed = 0
        self.draw_death_dinosaur()

        font = pygame.font.SysFont('comicsansms', 60, True, False)
        text_over = font.render("Game Over", True, BLACK)

        font = pygame.font.SysFont('comicsansms', 25, True, False)
        text_restart = font.render("Press Enter to reset the Game", True, BLACK)

        self.screen.blit(text_over, (600, 100))
        self.screen.blit(text_restart, (570, 330))
        self.screen.blit(self.reset_img, self.reset_rect)

    def create_obstacles(self):
        num_birds = 0
        num_cactus = 0

        for obstacle in self.obstacles:
            if isinstance(obstacle, Bird):
                num_birds += 1
            elif isinstance(obstacle, LargeCactus) or isinstance(obstacle, SmallCactus):
                num_cactus += 1

        num_obstacles = num_birds + num_cactus

        if num_obstacles == 0 or self.obstacles[-1].rect.x < WIDTH - random.randint(450, 500):
            if random.randint(0, 1) == 0 and num_cactus <= 2:
                if random.randint(0, 1) == 0:
                    self.obstacles.append(LargeCactus())
                else:
                    self.obstacles.append(SmallCactus())
            elif random.randint(0, 1) == 1 and num_birds <= 2:
                self.obstacles.append(Bird())

    def there_was_collision(self):
        dino_mask = self.dinosaur.get_mask()
        for obstacle in self.obstacles:
            obstacle_mask = obstacle.get_mask()
            distance = (obstacle.rect.x - self.dinosaur.dino_rect.x,
                        round(obstacle.rect.y) - round(self.dinosaur.dino_rect.y))

            if dino_mask.overlap(obstacle_mask, distance):
                return True

        return False

    def update_clouds(self):
        for cloud in self.clouds:
            cloud.update(self.game_speed)

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0 and self.game_speed < self.game_max_speed:
            self.game_speed += 0.1

    def update_obstacles(self):
        for idx, obstacle in enumerate(self.obstacles):
            obstacle.update(self.obstacles, self.game_speed, idx)
