import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from GameClasses.cloud import Cloud
from GameClasses.bird import Bird
from GameClasses.smallcactus import SmallCactus
from GameClasses.largecactus import LargeCactus
from constants import PATH, BLACK, RESET, WHITE, WIDTH
from GA.GA import GA
import pygame
import random

matplotlib.use("Agg")


class GameIA:

    def __init__(self, screen, num_generations, population_size, target_score, number_of_elitists: int = 4):
        # Game Attributes
        self.pause = False
        self.end = False
        self.screen = screen
        self.obstacles = []
        self.game_speed = 10
        self.game_max_speed = 20.0
        self.x_background = 0
        self.y_background = 580
        self.score = 0
        self.max_score = 0
        self.hi_score = 0
        self.best_scores = [0]
        self.mean_scores = [0]
        self.clouds = [Cloud(), Cloud(), Cloud(), Cloud(), Cloud(), Cloud(), Cloud(), Cloud(), Cloud()]

        self.reset_img = RESET
        self.reset_rect = self.reset_img.get_rect()
        self.reset_rect.x = 480
        self.reset_rect.y = 200

        # Genetic Attributes
        self.number_of_elitists = number_of_elitists
        self.genetic_alg = GA(num_generations, population_size, target_score, number_of_elitists=self.number_of_elitists
                              ,inferior_limit_pos=220, upper_limit_pos=221)
        self.genetic_alg.start_population()

        self.dinosaurs = self.genetic_alg.population
        self.current_generation = 1

        # Plot Attributes
        self.not_create_fig = True
        self.raw_data_fig = None
        self.size_fig = None

    def game_reset(self):
        # Reset game attributes
        self.pause = False
        self.obstacles = []
        self.game_speed = 10
        self.game_max_speed = 20.00
        self.x_background = 0

        # Define Info
        self.max_score = self.score
        self.hi_score = self.hi_score if self.hi_score > self.max_score else self.max_score
        self.score = 0

        # Reset figure plot
        self.not_create_fig = True
        plt.close('all')

        # Renewing population if necessary
        if self.current_generation % 11 == 0 and self.current_generation * 450 > self.hi_score:

            averages_the_last_best_score = np.mean(self.best_scores[len(self.best_scores) - 15:len(self.best_scores)])

            print("\t\t\t\t\t\t\t\tRenewing population")

            self.best_scores.append(self.max_score)
            self.mean_scores.append(np.array(self.best_scores).mean())

            self.genetic_alg.start_population()
            self.dinosaurs = self.genetic_alg.population

            self.hi_score = 0
            self.best_scores = [0]
            self.mean_scores = [0]
            self.current_generation = 0

        # Create new population
        else:
            self.genetic_alg.evaluation()
            self.genetic_alg.elitism()

            self.best_scores.append(self.max_score)
            self.mean_scores.append(self.genetic_alg.get_mean_score())
            self.genetic_alg.info_betters()

            self.genetic_alg.create_new_population()
            self.genetic_alg.update_rates()

            self.dinosaurs = self.genetic_alg.population

        self.current_generation += 1

    def draw_dinosaur(self):
        for dino in self.dinosaurs:
            if not dino.dead and dino.dino_rect.y <= dino.y_pos_down:
                self.screen.blit(dino.image, (dino.dino_rect.x, dino.dino_rect.y))

    def draw_cloud(self):
        for cloud in self.clouds:
            self.screen.blit(cloud.image, (cloud.x, cloud.y))

    def draw_bird(self, bird: Bird):
        if bird.index >= 9:
            bird.index = 0
        self.screen.blit(bird.image[bird.index // 5], bird.rect)
        bird.index += 1

    def draw_obstacle(self):
        for obstacle in self.obstacles:
            if isinstance(obstacle, Bird) and not self.pause:
                self.draw_bird(obstacle)
            else:
                self.screen.blit(obstacle.image[obstacle.frame], obstacle.rect)

    def draw_hiscore(self):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Hi-Sore: " + str(self.hi_score), True, BLACK)
        self.screen.blit(text, (1100, 10))

    def draw_score(self):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Score: " + str(self.score), True, BLACK)
        self.screen.blit(text, (1100, 35))

    def draw_max_score(self):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Max Score: " + str(self.max_score), True, BLACK)
        self.screen.blit(text, (1100, 60))

    def draw_speed(self):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Speed: " + str(round(self.game_speed, 2)), True, BLACK)
        self.screen.blit(text, (1100, 85))

    def draw_live_dino(self):
        count = 0
        for dino in self.dinosaurs:
            if not dino.dead:
                count += 1
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Live Dinosaurs: " + str(count), True, BLACK)
        self.screen.blit(text, (1100, 110))

    def draw_generation(self):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Generation: " + str(self.current_generation), True, BLACK)
        self.screen.blit(text, (1100, 135))

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
        self.draw_hiscore()
        self.draw_score()
        self.draw_max_score()
        self.draw_speed()
        self.draw_live_dino()
        self.draw_dinosaur()
        self.draw_generation()

    def draw_game_over(self):
        self.game_speed = 0

        font = pygame.font.SysFont('comicsansms', 60, True, False)
        text_over = font.render("Game Over", True, BLACK)

        font = pygame.font.SysFont('comicsansms', 25, True, False)
        text_restart = font.render("Press Enter to reset the Game", True, BLACK)

        self.screen.blit(text_over, (400, 100))
        self.screen.blit(text_restart, (370, 330))
        self.screen.blit(self.reset_img, self.reset_rect)

    def draw_graphics_score(self):
        if self.not_create_fig:
            self.not_create_fig = False
            fig, ax = plt.subplots(figsize=(10, 3), nrows=1, ncols=2)
            ax[0].plot(self.best_scores, color="green")
            ax[0].set_title("Highest Score of generation")
            ax[1].plot(self.mean_scores)
            ax[1].set_title("Mean Score of generation")

            canvas = fig.canvas
            canvas.draw()
            renderer = canvas.get_renderer()
            self.raw_data_fig = renderer.tostring_rgb()
            self.size_fig = canvas.get_width_height()

            surface = pygame.image.fromstring(self.raw_data_fig, self.size_fig, "RGB")
            self.screen.blit(surface, (0, 0))
            pygame.display.flip()

        elif not self.not_create_fig:
            surface = pygame.image.fromstring(self.raw_data_fig, self.size_fig, "RGB")
            self.screen.blit(surface, (0, 0))
            pygame.display.flip()

    def create_obstacles(self):
        num_obstacles = len(self.obstacles)
        if num_obstacles == 0 or self.obstacles[-1].rect.x < WIDTH - np.random.randint(400, 500):
            if random.randint(0, 1) == 0:
                if random.randint(0, 1) == 0:
                    self.obstacles.append(LargeCactus())
                else:
                    self.obstacles.append(SmallCactus())
            elif random.randint(0, 1) == 1:
                self.obstacles.append(Bird())

    def there_was_collision(self):
        for dino in self.dinosaurs:
            if not dino.dead:
                dino_mask = dino.get_mask()
                for obstacle in self.obstacles:
                    obstacle_mask = obstacle.get_mask()
                    distance = (obstacle.rect.x - dino.dino_rect.x,
                                round(obstacle.rect.y) - round(dino.dino_rect.y))
                    if dino_mask.overlap(obstacle_mask, distance):
                        dino.dead = True

    def update_clouds(self):
        for cloud in self.clouds:
            cloud.update(self.game_speed)

    def update_score_and_speed(self):
        self.score += 1

        for dino in self.dinosaurs:
            if not dino.dead:
                dino.score = self.score

        if self.score % 100 == 0 and self.game_speed < self.game_max_speed:
            self.game_speed += 0.1

    def update_obstacles(self):
        for idx, obstacle in enumerate(self.obstacles):
            obstacle.update(self.obstacles, self.game_speed, idx)

    def end_game(self):
        dead_list = []
        for dino in self.dinosaurs:
            dead_list.append(dino.dead)

        return all(dead_list)

    def info_game(self, dinosaur):
        distance_x = 0
        height_obs = 0
        width_obs = 0
        distance_ground_obs = 0
        height_dino = 0

        if len(self.obstacles) > 0:
            for obs in self.obstacles:
                if obs.rect.x > dinosaur.dino_rect.x:
                    distance_x = (obs.rect.x - dinosaur.dino_rect.x)
                    height_obs = (obs.rect.y - 490)
                    width_obs = obs.image[obs.frame].get_width()
                    distance_ground_obs = (obs.rect.y + height_obs) - 510
                    height_dino = (dinosaur.dino_rect.y - 490)
                    break

        return [distance_x, height_dino, round(dinosaur.current_jump_vel, 2),
                distance_ground_obs, height_obs, width_obs, round(self.game_speed, 2)]
