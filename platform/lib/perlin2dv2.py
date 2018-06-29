import math
import random


class Perlin2D(object):

    def __init__(self):
        self._rnd = random.Random()

    def generate_point_value(self, point):
        p0 = math.floor(point)
        p1 = p0 + 1

        pass

    def fade(self, v):
        return v*v*v*(v*(v*6.0 - 15.0) + 10.0)

    def grad(self, v):
        r = self._rnd.random()
        if r > 0.5:
            return 1.0
        else:
            return -1.0

    def noise(self, p):
        p0 = math.floor(p)
        p1 = p0 + 1.0
        t = p - p0
        fade_t = self.fade(t)
        g0 = self.grad(p0)
        g1 = self.grad(p1)
        return (1.0 - fade_t) * g0 * (p - p0) + fade_t * g1 * (p - p1)