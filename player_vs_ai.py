from GameClasses.vs_game import GameVS
from constants import draw_esc
import pygame
import sys


def start_vs_game(screen):
    game = GameVS(screen)
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        game.draw_game()
        draw_esc(game.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        if not game.pause:
            key_pressed = pygame.key.get_pressed()
            game.dinosaur.move(key_pressed)
            game.move_ia_dinosaur()

            game.create_obstacles()
            game.update_obstacles()

            if game.there_was_collision():
                game.pause = True

            game.update_clouds()
            game.update_score()

        if game.pause:
            game.draw_game_over()
            draw_esc(game.screen)
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RETURN]:
                game.game_reset()

        pygame.display.update()
