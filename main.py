import os

import pygame

SCREEN_SIZE = (640, 480)


def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"

    pygame.init()
    pygame.font.init()

    mode = 0
    # if pygame.version.vernum >= (2, 0):  # Scale is SDL2 only
    #     mode |= pygame.SCALED

    pygame.display.set_icon(pygame.image.load(os.path.join("res", "images", "worm.png")))
    screen = pygame.display.set_mode(SCREEN_SIZE, mode)
    pygame.display.set_caption("worms.py")

    import worms  # Import here so game can load and convert images properly
    game = worms.Worms(SCREEN_SIZE)

    now_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    clock.tick_busy_loop()
    while True:
        dt = min(0.05, clock.tick_busy_loop() / 1000)
        # Limit low fps (otherwise game wil compute physics on big time
        #  and worms will jump even if the were still)
        screen.fill((0, 0, 0))  # Clear screen (better not do it)

        game.event(dt)
        game.update(dt)

        game.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
