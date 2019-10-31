import numpy
import pygame

import engine.utils as utils


class Terrain:
    IMAGE_COLORKEY = 0xFF00FF

    def __init__(self, width: int, height: int, foreground_image: pygame.Surface):
        self.width: int = width
        self.height: int = height

        self.cells = numpy.zeros(width * height, numpy.bool)

        self.terrainImage = pygame.Surface((width, height))
        self.terrainImage.set_colorkey(Terrain.IMAGE_COLORKEY)
        self.load_foreground_as_terrain(foreground_image)

    def explode_circle(self, x: int, y: int, radius: int):
        self.midpoint_circle(x, y, radius)
        self.draw_terrain(x - radius, y - radius, 2 * radius + 1, 2 * radius + 1)

    def draw_terrain(self, sx: int, sy: int, width: int, height: int):
        terrain_array = pygame.PixelArray(self.terrainImage)
        sx = utils.clamp(sx, 0, self.width - width)
        sy = utils.clamp(sy, 0, self.height - height)
        for x in range(sx, sx + width):
            for y in range(sy, sy + height):
                if not self.cells[x + y * self.width]:
                    terrain_array[x, y] = Terrain.IMAGE_COLORKEY
        terrain_array.close()

    def midpoint_circle(self, x0, y0, radius):
        def set_line(x1, x2, y_):
            for x_ in range(x1, x2 + 1):
                if self.valid_position(x_, y_):
                    self.cells[x_ + y_ * self.width] = False

        f = 1 - radius
        ddf_x, ddf_y = 1, -2 * radius
        x, y = 0, radius
        set_line(x0 - radius, x0 + radius, y0)
        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x
            set_line(x0 - x, x0 + x, y0 + y)
            set_line(x0 - x, x0 + x, y0 - y)
            set_line(x0 - y, x0 + y, y0 + x)
            set_line(x0 - y, x0 + y, y0 - x)

    def load_foreground_as_terrain(self, image: pygame.Surface):
        out_array = pygame.PixelArray(self.terrainImage)
        in_array = pygame.PixelArray(image)
        for x in range(self.width):
            for y in range(self.height):
                pix = in_array[x, y]
                if pix >> 24 & 0xFF != 0:  # If alpha is not 0
                    self.cells[x + y * self.width] = True
                    out_array[x, y] = pix
                else:
                    out_array[x, y] = Terrain.IMAGE_COLORKEY
        out_array.close()
        in_array.close()

    def get_block_data(self, x: int, y: int):
        return self.cells[x + y * self.width]

    def valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
