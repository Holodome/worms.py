import pygame

import os
import time

SCREEN_SIZE = (640, 480)


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    pygame.font.init()

    mode = 0
    # if pygame.version.vernum >= (2, 0):  # Scale is SDL2 only
    #     mode |= pygame.SCALED

    pygame.display.set_icon(pygame.image.load(os.path.join("res/icon.ico")))
    screen = pygame.display.set_mode(SCREEN_SIZE, mode)
    pygame.display.set_caption("worms.py")

    import worms

    game = worms.Worms(SCREEN_SIZE)

    now_time = time.perf_counter()
    while True:
        dt = time.perf_counter() - now_time
        now_time += dt
        screen.fill((0, 0, 0))  # Clear screen (better not do it)

        game.event(dt)
        game.update(dt)

        game.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
