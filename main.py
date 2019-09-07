import os

import pygame

from toolbox import loader


def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    pygame.init()
    pygame.font.init()

    mode = 0
    # if pygame.version.vernum >= (2, 0):  # Scale is SDL2 only
    #     mode |= pygame.SCALED

    pygame.display.set_icon(pygame.image.load(os.path.join("res", "images", "worm.png")))
    screen = pygame.display.set_mode((640, 480), mode)
    pygame.display.set_caption("worms.py")
    pygame.mouse.set_visible(False)

    loader.init()
    from game import worms
    game = worms.Worms([640, 480])

    now_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    clock.tick_busy_loop()
    while True:
        dt = clock.tick_busy_loop() / 1000
        # Limit low fps (otherwise game wil compute physics on big time
        #  and worms will jump even if the were still)
        screen.fill((0, 0, 0))  # Clear screen (better not do it)

        game.event(dt)
        game.update(dt)

        game.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
