import pygame
from GameClasses.cloud import Cloud
from constants import WIDTH, HEIGHT, WHITE, BLACK, GREY, PATH, DINO_RUN
from constants import draw_esc
from show_ai_game import start_ai_game
from normal_game import start_game
from player_vs_ai import start_vs_game
import sys
import os


def draw_board(screen):
    screen.fill(WHITE)
    screen.blit(PATH, (0, 580))
    screen.blit(DINO_RUN[0], (100, 560))

    for i in range(13):
        cloud = Cloud()
        cloud.x = i * 125 + 60
        cloud.y = 400 if (i + 1) % 2 == 0 else 440
        screen.blit(cloud.image, (cloud.x, cloud.y))

    font = pygame.font.SysFont('comicsansms', 60, True, False)
    screen.blit(font.render("Dino Game", True, BLACK), (590, 100))

    font = pygame.font.SysFont('comicsansms', 25, True, False)
    screen.blit(font.render("Choose game mode, press the key", True, BLACK), (540, 220))

    font = pygame.font.SysFont('comicsansms', 20, True, False)

    pygame.draw.rect(screen, GREY, (pygame.Rect(590, 300, 310, 60)))
    screen.blit(font.render("1 :: Solo mode", True, WHITE), (660, 315))

    pygame.draw.rect(screen, GREY, (pygame.Rect(590, 390, 310, 60)))
    screen.blit(font.render("2 :: Vs IA mode", True, WHITE), (653, 405))

    pygame.draw.rect(screen, GREY, (pygame.Rect(590, 480, 310, 60)))
    screen.blit(font.render("3 :: Show GA and NN", True, WHITE), (635, 495))

    draw_esc(screen)


def main():
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS'] = '20,80'

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dino Game")
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        draw_board(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    start_game(screen)

                if event.key == pygame.K_2:
                    start_vs_game(screen)

                if event.key == pygame.K_3:
                    start_ai_game(screen, 80, 200)

        pygame.display.flip()


if __name__ == "__main__":
    main()
