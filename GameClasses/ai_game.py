import matplotlib
import matplotlib.pyplot as plt
from GameClasses.game import Game
from GameClasses.largecactus import LargeCactus
from GameClasses.smallcactus import SmallCactus
from constants import BLACK, WHITE
import pygame

matplotlib.use("Agg")


class GameIA(Game):

    def __init__(self, screen):
        # Game Attributes
        super().__init__(screen)
        self.dinosaurs = []
        self.end = False
        self.reset = False

        self.max_score = 0
        self.hi_score = 0
        self.best_scores = [0]
        self.mean_scores = [0]

        # Plot Attributes
        self.not_create_fig = True
        self.raw_data_fig = None
        self.size_fig = None

        # Genetic Attributes
        self.current_generation = 1
        self.resets_generation = 0

    def game_reset(self):
        # Reset game attributes
        self.reset = False
        self.obstacles = []
        self.game_speed = 10
        self.x_background = 0

        # Define Info
        self.max_score = self.score
        self.hi_score = self.hi_score if self.hi_score > self.max_score else self.max_score
        self.score = 0

        # Reset figure plot
        self.not_create_fig = True
        plt.close('all')

    # Draw Functions
    def draw_dinosaur(self):
        for dino in self.dinosaurs:
            if not dino.dead and dino.dino_rect.y <= dino.y_pos_down:
                self.screen.blit(dino.image, (dino.dino_rect.x, dino.dino_rect.y))

    def draw_hiscore(self):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Hi-Sore: " + str(self.hi_score), True, BLACK)
        self.screen.blit(text, (1100, 10))

    def draw_max_score(self):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Max Score: " + str(self.max_score), True, BLACK)
        self.screen.blit(text, (1100, 35))

    def draw_live_dino(self):
        count = 0
        for dino in self.dinosaurs:
            if not dino.dead:
                count += 1
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Live Dinosaurs: " + str(count), True, BLACK)
        self.screen.blit(text, (1100, 110))

    def draw_resets_generation(self):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Resets Generation: " + str(self.resets_generation), True, BLACK)
        self.screen.blit(text, (1100, 135))

    def draw_stagnant_generations(self, stagnant_generations):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Stagnant Generations: " + str(stagnant_generations), True, BLACK)
        self.screen.blit(text, (1100, 160))

    def draw_expected_score(self, expected_score):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Expected Score: " + str(round(expected_score, 2)), True, BLACK)
        self.screen.blit(text, (1100, 185))

    def draw_generation(self):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Generation: " + str(self.current_generation), True, BLACK)
        self.screen.blit(text, (1100, 185))

    def draw_cross_rate(self, cross_rate):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Cross Rate: " + str(round(cross_rate, 4)), True, BLACK)
        self.screen.blit(text, (1100, 235))

    def draw_mutation_rate(self, mutation_rate):
        font = pygame.font.SysFont('comicsansms', 20, True, False)
        text = font.render("Mutation Rate: " + str(round(mutation_rate, 4)), True, BLACK)
        self.screen.blit(text, (1100, 210))

    def draw_game(self):
        self.screen.fill(WHITE)
        self.draw_background()
        self.draw_obstacle()
        self.draw_cloud()
        self.draw_hiscore()
        self.draw_score(x=1100, y=60)
        self.draw_max_score()
        self.draw_speed(x=1100, y=85)
        self.draw_live_dino()
        self.draw_resets_generation()
        self.draw_generation()

        self.draw_dinosaur()

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
            self.screen.blit(surface, (0, 40))
            pygame.display.flip()

        elif not self.not_create_fig:
            surface = pygame.image.fromstring(self.raw_data_fig, self.size_fig, "RGB")
            self.screen.blit(surface, (0, 40))
            pygame.display.flip()

    def draw_finished_test(self):
        self.draw_game()
        self.draw_graphics_score()

        font = pygame.font.SysFont('comicsansms', 40, True, False)
        text_result = font.render("Finished Test", True, BLACK)

        self.screen.blit(text_result, (600, 400))

    # Game Functions
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

    def update_score_and_speed(self):
        self.score += 1

        for dino in self.dinosaurs:
            if not dino.dead:
                dino.score = self.score

        if self.score % 100 == 0 and self.game_speed < self.game_max_speed:
            self.game_speed += 0.1

    def end_game(self):
        dead_list = []
        for dino in self.dinosaurs:
            dead_list.append(dino.dead)

        return all(dead_list)

    def info_game(self, dinosaur):
        distance = 0
        speed = round(self.game_speed, 2)
        altitude = 0
        width = 0
        height = 0
        altitude_dino = 0

        if len(self.obstacles) > 0:
            for obs in self.obstacles:
                if obs.rect.x > dinosaur.dino_rect.x:
                    distance = obs.rect.x - dinosaur.dino_rect.x
                    width = obs.image[obs.frame].get_width()

                    if isinstance(obs, LargeCactus) or isinstance(obs, SmallCactus):
                        height = 48
                        altitude = 0
                    else:
                        height = obs.image[obs.frame].get_height()
                        altitude = self.y_background - obs.rect.y

                    altitude_dino = self.y_background - dinosaur.dino_rect.y
                    break

        return [distance, width, height, altitude, altitude_dino, speed]
