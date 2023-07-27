from constants import *
from IA.game_ia import GameIA
import numpy as np
import pygame
import sys
import os


def main():
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = '20,80'

    game = GameIA(pygame.display.set_mode((WIDTH, HEIGHT)), 80, 200, 40000, number_of_elitists=3)
    pygame.display.set_caption("Dino Game")
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game.end = True
                    game.draw_game_over()
                    game.genetic_alg.result_and_save()

                if event.key == pygame.K_r:
                    game.game_reset()

        if not game.pause and not game.end:
            game.draw_game()
            game.draw_graphics_score()

            game.create_obstacles()
            game.update_obstacles()

            for dinosaur in game.dinosaurs:
                if not dinosaur.dead:
                    info = game.info_game(dinosaur)
                    decision = dinosaur.decision(np.array(info))
                    dinosaur.ia_move(decision)

            game.there_was_collision()

            if game.end_game():
                game.pause = True

            game.update_clouds()
            game.update_score_and_speed()

        if game.current_generation >= game.genetic_alg.num_generations and not game.end:
            game.end = True
            game.draw_game_over()
            game.genetic_alg.result_and_save()

        elif game.pause and not game.end:
            game.game_reset()

        pygame.display.update()


if __name__ == '__main__':
    main()
