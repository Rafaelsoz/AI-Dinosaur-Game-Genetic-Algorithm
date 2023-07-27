from constants import *
from NormalGame.game import Game
import pygame
import sys
import os


def main():
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = '20,80'

    game = Game(pygame.display.set_mode((WIDTH, HEIGHT)))
    pygame.display.set_caption("Dino Game")
    clock = pygame.time.Clock()

    while True:
        clock.tick(45)
        game.draw_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game.pause:
            key_pressed = pygame.key.get_pressed()
            game.dinosaur.move(key_pressed)

            game.create_obstacles()
            game.update_obstacles()

            if game.there_was_collision():
                game.pause = True

            game.update_clouds()
            game.update_score()

        if game.pause:
            game.draw_gama_over()
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RETURN]:
                game.game_reset()

        pygame.display.update()


if __name__ == '__main__':
    main()
