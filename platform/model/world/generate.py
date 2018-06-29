from platform.lib.perlin2d import Perlin2D
from random import Random
import math


def generate_world(width, height):
    print("Generate {}x{}".format(width, height))
    perlin = Perlin2D(width, height)
    h_map = [None for _ in range(0, width*height)]
    for i in range(0, width*height):
        weight = perlin.noise_map[i]
        if weight > 0:
            h_map[i] = 1
        else:
            h_map[i] = 0
    return h_map


def generate_height_map(width, height, scale=8, min_from_top=10):
    height_map = [0 for _ in range(0, width)]
    rnd = Random()
    # we want to pick a random height, but we know it needs to be somewhere around the 3/4 mark
    r_pts = (math.ceil(height // 4 - 10), math.floor(height // 4 + 10))
    rnd_starting_position = rnd.randint(min(r_pts), max(r_pts))
    if rnd_starting_position < min_from_top:
        rnd_starting_position = min_from_top
    height_map[0] = rnd_starting_position  # set as the starting position
    # so what we do is pick a random length, somewhere a few spaces away, this is to create flat spots in the terrain
    # map.  To do this, we would like to get a point that is between 1 and 8 spots from our start
    idx = 1  # current index we're working at
    # what we're going to do now is enter a while loop, the index point will basically control
    # when this ends as we're going to move forward N spaces, then build the map between idx and N
    # then move forward and continue until we reach the end
    loops = 0
    while idx < width:
        loops += 1
        rnd_rng = rnd.randint(1, scale)
        rnd_point = rnd.randint(1, rnd_rng)
        rnd_height = rnd.randint(-1, 1)  # we don't want our height to be greater than our distance
        # we now roll for "up" or "down"
        end_point = idx + rnd_point
        # make sure we don't over-flow the array index
        if end_point > width:
            end_point = width
        for i in range(idx, end_point):
            height_map[i] = height_map[i-1] + rnd_height
            # enforce min from top by reversing if we hit the min
            if height_map[i] < min_from_top:
                height_map[i] = height_map[i-1] - rnd_height
        idx = end_point
    return height_map

"""
Okay, need a place to jot down ideas and notes about how to generate the world, what kinds of terrain we should do
and what I need to figure out to make it all come together.


Worlds should be something along the lines of 1024x256, maybe a bit deeper, like 1024x512 or even 2048x512.  I think we
can get away with this scale in pygame if we're efficient about how we store our data.


Terrain Types:
dirt - common, used as fill for higher ground 0-100 layer, patches found below 100
stone - common, used as fill for deeper ground 100-: layer, small patches found above 100
ore - various ores found is patches

Terrain entities:
Tree
Bush
Vine

Crafted things - figure these out later


So the terrain generation process should go something like this:
generate tile array x/y so tiles[x][y] or [y][x] is probably more accurate.
generate a height map and apply the height map.  This map will be just grass.
Once grass is applied, apply air, everything higher than the grass is air.
next apply stone filter, everything below 100 that is dirt, becomes stone.
**todo we need to make sure our height map never generates a start below like 75.
**todo look into method for generating caves.
after caves are generated, make pass on grass tiles, we'll need them to check their
neighbors and adjust to the proper image depending on the slope etc.
Next we're going to want to generate our ore patches.
Next we'll generate vegetation

From here, we should have a somewhat usable map.

**todo we'll need to figure out some kind of a liquid system.

"""