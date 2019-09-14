import numpy
import pygame

ALPHA_COLORKEY = (255, 0, 255)


class Terrain:
    def __init__(self, width, height, foreground):
        self.width = width
        self.height = height

        self.terrain = numpy.zeros(width * height, numpy.uint32)
        self.load_foreground_as_terrain(foreground)

        self.terrainImage = pygame.Surface((width, height))
        self.terrainImage.set_colorkey(ALPHA_COLORKEY)
        self.draw_terrain(0, 0, width, height)

    def explode_circle(self, x, y, radius):
        self.midpoint_circle(x, y, radius)
        self.draw_terrain(x - radius, y - radius, 2 * radius + 1, 2 * radius + 1)

    def draw_terrain(self, sx: int, sy: int, width: int, height: int):
        for x in range(sx, sx + width):
            for y in range(sy, sy + height):
                if not self.valid_position(x, y):
                    continue
                color = (255, 0, 255)
                cell = self.terrain[x + y * self.width]
                if cell != 0:
                    color = ((cell >> 16) & 0xFF, (cell >> 8) & 0xFF, cell & 0xFF)
                self.terrainImage.set_at((x, y), color)

    def midpoint_circle(self, x0, y0, radius):
        """Make circle explosion"""

        def set_line(x1, x2, y_):
            for x_ in range(x1, x2 + 1):
                if self.valid_position(x_, y_):
                    self.terrain[x_ + y_ * self.width] = 0

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
        for x in range(self.width):
            for y in range(self.height):
                pix = image.get_at((x, y))
                if pix[3] != 0:  # Not transparent
                    # Store color data in one integer using bitwise operators
                    data = ((pix[0] << 16) & 0xFF0000) | ((pix[1] << 8) & 0x00FF00) | pix[2] & 0x0000FF
                    self.terrain[x + y * self.width] = data

    def get_block_data(self, x, y):
        return self.terrain[int(x) + int(y) * self.width]

    def valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    @property
    def size(self):
        return self.width, self.height
