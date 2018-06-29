import pygame


class TileType(object):
    NULL = 0
    AIR = 1
    DIRT = 2
    GRASS = 3
    STONE = 4


class Tile(pygame.sprite.Sprite):

    def __init__(self, *groups, tile_type=TileType.NULL, image=None, x=0, y=0):
        super().__init__(*groups)
        self._tile_type = tile_type
        if image:
            self.image = image
        else:
            # default empty white square if no image
            self.image = pygame.Surface([16, 16])
            self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    @property
    def tile_type(self):
        return self._tile_type

    @tile_type.setter
    def tile_type(self, tile_type):
        self._tile_type = tile_type

    @property
    def position(self):
        return self.rect.topleft

    def change_image(self, new_image):
        self.image = new_image
        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height


class TileMap(object):

    def __init__(self, width, height, tile_size):
        self._w = width
        self._h = height
        self._tiles = [[None for _ in range(0, self._w)] for _ in range(0, self._h)]
        image = pygame.image.load("resources\\images\\dirt_16x16.png")
        for y in range(0, self._h):
            for x in range(0, self._w):
                # replace this with a manager
                t = Tile(image=image, x=x*tile_size, y=y*tile_size, tile_type=TileType.DIRT)
                try:
                    self._tiles[y][x] = t
                except IndexError as e:
                    print("Index error trying to access {}, {}".format(x, y))
                    raise e

    def draw(self, display):
        for y in range(0, self._h):
            for x in range(0, self._w):
                display.blit(self._tiles[y][x].image, self._tiles[y][x].rect)

    def tile_at(self, x, y) -> Tile:
        return self._tiles[y][x]

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    @property
    def tiles(self):
        return self._tiles

    def tile_neighbors(self, x, y, tile_type):
        t = 0
        if 0 < x - 1 < self._w and 0 < y - 1 < self._h and self.tile_at(x-1, y-1).tile_type == tile_type:
            t |= 128
        if 0 < x < self._w and 0 < y - 1 < self._h and self.tile_at(x, y-1).tile_type == tile_type:
            t |= 64
        if 0 < x + 1 < self._w and 0 < y - 1 < self._h and self.tile_at(x+1, y-1).tile_type == tile_type:
            t |= 32
        if 0 < x + 1 < self._w and 0 < y < self._h and self.tile_at(x+1, y).tile_type == tile_type:
            t |= 16
        if 0 < x + 1 < self._w and 0 < y + 1 < self._h and self.tile_at(x+1, y+1).tile_type == tile_type:
            t |= 8
        if 0 < x < self._w and 0 < y + 1 < self._h and self.tile_at(x, y+1).tile_type == tile_type:
            t |= 4
        if 0 < x - 1 < self._w and 0 < y + 1 < self._h and self.tile_at(x-1, y+1).tile_type == tile_type:
            t |= 2
        if 0 < x - 1 < self._w and 0 < y < self._h and self.tile_at(x-1, y).tile_type == tile_type:
            t |= 1
        return t
