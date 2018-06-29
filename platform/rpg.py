import pygame
from platform import constants
from platform.model.world.gameworld import TileMap, TileType
from platform.model.world.generate import generate_height_map
import random


class RPG(object):
    def __init__(self):
        # placeholder BS for testing
        self._air_color = (0, 162, 232)
        #####
        self._display = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self._running = True
        self._states = {}
        self._active_state = None
        self._delta_time = 0
        self._clock = pygame.time.Clock()
        self._trigger_state_change = False
        self._trigger_state_change_to = None
        self._initialize_states()
        self._camera = pygame.sprite.Sprite()
        self._camera.rect = pygame.Rect(0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        self._images = {}

    def run(self):
        self._load_images()
        tiles = self._build_tile_map()
        while self._running:
            m_pos = pygame.mouse.get_pos()
            ptx = m_pos[0]
            if ptx != 0:
                ptx = ptx // 16
            pty = m_pos[1]
            if pty != 0:
                pty = pty // 16
            m_str = "Mouse({}, {})".format(ptx, pty)
            pygame.display.set_caption(m_str)
            self._display.fill(self._air_color)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self._running = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        del tiles
                        tiles = self._build_tile_map()
            tiles.draw(self._display)
            pygame.display.update()
            self._delta_time = self._clock.tick(60)
            pygame.event.pump()
        pygame.quit()

    def stop(self):
        # public exit interface
        self._running = False

    def _change_state(self):
        """
        Facilitates changing states, fails silently if invalid state key or no state key provided.
        :return:
        """
        if self._trigger_state_change_to:  # ensure we got a state to change to
            if self._trigger_state_change_to in self._states.keys():
                self._active_state.on_exit()
                self._active_state = self._states[self._trigger_state_change_to]
                self._active_state.on_enter()
                self._trigger_state_change = False
                self._trigger_state_change_to = None

    def _initialize_states(self):
        pass

    def _load_images(self):
        sprite_sheet = pygame.image.load("resources\\images\\grass_dirt_sheet_80x32.png").convert()
        sprite_sheet.set_colorkey((255, 0, 255))
        self._images['air-grass-1'] = sprite_sheet.subsurface((0, 0, 16, 16))
        self._images['grass-slope-1'] = sprite_sheet.subsurface((16, 0, 16, 16))
        self._images['grass-no-slope'] = sprite_sheet.subsurface((32, 0, 16, 16))
        self._images['grass-slope-2'] = sprite_sheet.subsurface((48, 0, 16, 16))
        self._images['air-grass-2'] = sprite_sheet.subsurface((64, 0, 16, 16))
        self._images['grass-slope-3'] = sprite_sheet.subsurface((0, 16, 16, 16))
        self._images['dirt'] = sprite_sheet.subsurface((32, 16, 16, 16))
        self._images['grass-slope-4'] = sprite_sheet.subsurface((64, 16, 16, 16))
        tmp_surf = pygame.image.load("resources\\images\\rock_16x16.png").convert()
        self._images['stone'] = tmp_surf.copy()
        sky = pygame.Surface([16, 16])
        sky.fill(self._air_color)
        self._images['air'] = sky

    def _build_tile_map(self):
        tx = 800 // 16
        ty = 600 // 16
        min_up_rnd = ty - (ty // 3)
        tiles = TileMap(tx, ty, 16)
        h_map = generate_height_map(tx, ty, 3)
        marker_red = pygame.Surface([16, 16])
        marker_red.fill((255, 0, 0))
        for i in range(0, len(h_map)):
            h = h_map[i]
            tiles.tile_at(i, h).change_image(self._images['grass-no-slope'])
            tiles.tile_at(i, h).tile_type = TileType.GRASS
            # change any tiles above to air
            for j in range(0, ty):
                if j < h:
                    tiles.tile_at(i, j).change_image(self._images['air'])
                    tiles.tile_at(i, j).tile_type = TileType.AIR
        # pretend random walk here
        # start with a random X position
        rnd = random.Random()
        points = rnd.randint(4, 8)
        start_points = set()
        for i in range(0, points):
            rnd_x = rnd.randint(0, tx-1)
            rnd_pos = rnd_x, h_map[rnd_x]
            start_points.add(rnd_pos)
        # okay so we should have some random starting heights
        # each step, we can go down, right or left
        for pos in start_points:
            steps = rnd.randint(10, 100)
            n_pos = pos
            for _ in range(0, steps):
                # we can move down, left, or right
                choice = rnd.choice(['d', 'l', 'r', 'u'])
                if choice == 'd':
                    n_pos = n_pos[0], n_pos[1] + 1
                if choice == 'l':
                    n_pos = n_pos[0] - 1, n_pos[1]
                if choice == 'r':
                    n_pos = n_pos[0] + 1, n_pos[1]
                if choice == 'u':
                    if n_pos[1] >= min_up_rnd:  # only go up if we're below our 1/3 threshold
                        n_pos = n_pos[0], n_pos[1] - 1
                    else:
                        n_pos = n_pos[0], n_pos[1] + 1
                # keep the positions in range
                if n_pos[0] < 0:
                    n_pos = 0, n_pos[1]
                if n_pos[0] >= tx:
                    n_pos = tx - 1, n_pos[1]
                if n_pos[1] < 0:
                    n_pos = n_pos[0], 0
                if n_pos[1] >= ty:
                    n_pos = n_pos[0], ty - 1
                tiles.tile_at(n_pos[0], n_pos[1]).change_image(self._images['stone'])
                tiles.tile_at(n_pos[0], n_pos[1]).tile_type = TileType.STONE
        # now we can do a neighbor check
        for y in range(0, ty):
            for x in range(0, tx):
                if tiles.tile_at(x, y).tile_type == TileType.DIRT:
                    tile_neighbors = tiles.tile_neighbors(x, y, TileType.STONE)
                    if tile_neighbors == 255:
                        print("Tile at {},{} full surround: {}".format(x, y, tile_neighbors))
                        tiles.tile_at(x, y).change_image(marker_red)
                elif tiles.tile_at(x, y).tile_type == TileType.GRASS:
                    tile_neighbors = tiles.tile_neighbors(x, y, TileType.GRASS)
                    if tile_neighbors == 0b00010010:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-1'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-1'))
                    elif tile_neighbors == 0b00010001 or tile_neighbors == 0b00000001 or tile_neighbors == 0b00010000:
                        tiles.tile_at(x, y).change_image(self._images['grass-no-slope'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-no-slope'))
                    elif tile_neighbors == 0b00001001:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-2'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-2'))
                    elif tile_neighbors == 0b00100000 or tile_neighbors == 0b00100010:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-3'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-3'))
                    elif tile_neighbors == 0b10000000 or tile_neighbors == 0b10001000:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-4'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-4'))
                elif tiles.tile_at(x, y).tile_type == TileType.AIR:
                    tile_neighbors = tiles.tile_neighbors(x, y, TileType.GRASS)
                    if tile_neighbors == 0b00010100:
                        tiles.tile_at(x, y).change_image(self._images['air-grass-1'])
                        print("Tile at {},{} air neighbors: {}".format(x, y, tile_neighbors))
                    elif tile_neighbors == 0b00000101:
                        tiles.tile_at(x, y).change_image(self._images['air-grass-2'])
                        print("Tile at {},{} air neighbors: {}".format(x, y, tile_neighbors))
        # do grass again, fucking wonky bullshit going on here
        for y in range(0, ty):
            for x in range(0, tx):
                if tiles.tile_at(x, y).tile_type == TileType.GRASS:
                    tile_neighbors = tiles.tile_neighbors(x, y, TileType.GRASS)
                    if tile_neighbors == 0b00010010:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-1'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-1'))
                    elif tile_neighbors == 0b00010001 or tile_neighbors == 0b00000001 or tile_neighbors == 0b00010000:
                        tiles.tile_at(x, y).change_image(self._images['grass-no-slope'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-no-slope'))
                    elif tile_neighbors == 0b00001001:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-2'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-2'))
                    elif tile_neighbors == 0b00100000 or tile_neighbors == 0b00100010:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-3'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-3'))
                    elif tile_neighbors == 0b10000000 or tile_neighbors == 0b10001000:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-4'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-4'))
        return tiles

    def _tile_mask(self, tiles):
        tx = 800 // 16
        ty = 600 // 16
        for y in range(0, ty):
            for x in range(0, tx):
                if tiles.tile_at(x, y).tile_type == TileType.GRASS:
                    tile_neighbors = tiles.tile_neighbors(x, y, TileType.GRASS)
                    if tile_neighbors == 0b00010010:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-1'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-1'))
                    elif tile_neighbors == 0b00010001 or tile_neighbors == 0b00000001 or tile_neighbors == 0b00010000:
                        tiles.tile_at(x, y).change_image(self._images['grass-no-slope'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-no-slope'))
                    elif tile_neighbors == 0b00001001:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-2'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-2'))
                    elif tile_neighbors == 0b00100000 or tile_neighbors == 0b00100010:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-3'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-3'))
                    elif tile_neighbors == 0b10000000 or tile_neighbors == 0b10001000:
                        tiles.tile_at(x, y).change_image(self._images['grass-slope-4'])
                        print("Tile at {},{} grass neighbors: {} - {}".format(x, y, tile_neighbors, 'grass-slope-4'))
