from GameClasses.game import Game
from GameClasses.dinosaur import Dinosaur
from GameClasses.ia_dinosaur import DinosaurIA
from GameClasses.largecactus import LargeCactus
from GameClasses.smallcactus import SmallCactus
from constants import WHITE, DINO_DEAD, PURPLE_DINO_DEAD
import numpy as np
import pickle


# Load best, saved as Elitist object
def load_dino(path: str = "Saves/dino_trained.obj"):
    with open(path, "rb") as f:
        best = pickle.load(f)

    dinosaur = DinosaurIA(color="purple")
    dinosaur.neurons = best.nn

    return dinosaur


class GameVS(Game):
    def __init__(self, screen):
        super().__init__(screen)
        self.ia_dinosaur = load_dino()

    def game_reset(self):
        self.obstacles = []
        self.game_speed = 10
        self.x_background = 0
        self.hi_score = self.hi_score if self.score <= self.hi_score else self.score
        self.score = 0

        self.pause = False

        self.dinosaur = Dinosaur()
        self.ia_dinosaur = load_dino()

    def draw_dinosaurs(self):
        if not self.ia_dinosaur.dead and self.ia_dinosaur.dino_rect.y <= self.ia_dinosaur.y_pos_down:
            self.screen.blit(self.ia_dinosaur.image, (self.ia_dinosaur.dino_rect.x, self.ia_dinosaur.dino_rect.y))
        self.draw_dinosaur()

    def draw_death_dinosaur(self):
        if self.dinosaur.dead:
            self.screen.blit(DINO_DEAD, (self.dinosaur.dino_rect.x,
                                         self.dinosaur.dino_rect.y))
        if self.ia_dinosaur.dead:
            self.screen.blit(PURPLE_DINO_DEAD, (self.dinosaur.dino_rect.x,
                                                self.dinosaur.dino_rect.y))

    def draw_game(self):
        self.screen.fill(WHITE)
        self.draw_background()
        self.draw_obstacle()
        self.draw_cloud()
        self.draw_score()
        self.draw_hi_score()
        self.draw_speed()
        self.draw_dinosaurs()

    def there_was_collision(self):
        dino_mask = self.dinosaur.get_mask()
        ia_dino_mask = self.ia_dinosaur.get_mask()

        for obstacle in self.obstacles:
            obstacle_mask = obstacle.get_mask()

            distance = (obstacle.rect.x - self.dinosaur.dino_rect.x,
                        round(obstacle.rect.y) - round(self.dinosaur.dino_rect.y))

            ia_distance = (obstacle.rect.x - self.ia_dinosaur.dino_rect.x,
                           round(obstacle.rect.y) - round(self.ia_dinosaur.dino_rect.y))

            if dino_mask.overlap(obstacle_mask, distance):
                self.dinosaur.dead = True
                return True

            if ia_dino_mask.overlap(obstacle_mask, ia_distance):
                self.ia_dinosaur.dead = True
                return True

        return False

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

    def move_ia_dinosaur(self):
        if not self.ia_dinosaur.dead:
            info = self.info_game(self.ia_dinosaur)
            decision = self.ia_dinosaur.decision(np.array(info))
            self.ia_dinosaur.ia_move(decision)
