import pygame

# Cache
loaded_fonts = {}
loaded_images = {}

COLORKEY = (255, 0, 255)


def init():
    # Load all fonts and images needed
    load_image("arrow", set_colorkey=True)
    load_image("crosshair", set_colorkey=True)
    load_image("worm", set_colorkey=True)
    load_image("grenade", convert=True)
    load_image("cluster_bomb", convert=True)
    load_image("cluster", convert=True)

    load_font(True, "consolas", 10)
    load_font(False, "title.TTF", 40)
    load_font(False, "worldName.TTF", 20)
    load_font(True, "consolas", 15)


def load_font(sys_font: bool, font_name: str, font_size: int, *args, **kwargs) -> pygame.font.FontType:
    key = font_name.lower() + " " + str(font_size)
    if loaded_fonts.get(font_name) is None:
        if sys_font:
            loaded_fonts[key] = pygame.font.SysFont(font_name, font_size, *args, **kwargs)
        else:
            loaded_fonts[key] = pygame.font.Font("res/fonts/" + font_name, font_size, *args, **kwargs)
    return loaded_fonts[key]


def load_image(name: str, convert=False, convert_alpha=False, set_colorkey=False) -> pygame.Surface:
    assert not (convert and convert_alpha) or not (convert_alpha and set_colorkey)

    if loaded_images.get(name) is None:
        image = pygame.image.load("res/images/" + name + ".png")
        if set_colorkey:
            image.set_colorkey(COLORKEY)
        if convert:
            image.convert()
        if convert_alpha:
            image.convert_alpha()
        loaded_images[name] = image
    return loaded_images[name]


def get_image(name: str) -> pygame.Surface:
    return loaded_images[name.lower()]


def get_font(name: str, size: int) -> pygame.font.FontType:
    return loaded_fonts[(name + " " + str(size)).lower()]
