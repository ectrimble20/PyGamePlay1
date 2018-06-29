import random
import math


class Perlin2D(object):
    """
    Perlin 2D

    Generates a 2 dimensional noise map using a variation of the Perlin noise algorithm.
    https://en.wikipedia.org/wiki/Perlin_noise

    This particular implementation will produce an array of width*height with a variation
    from 0 - 255.  This is useful for generating height maps as well as random color patterns.
    """
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.gradient_table = [(0, 0) for _ in range(0, self.w*self.h)]
        self._build_gradient_table()
        self.noise_map = [0 for _ in range(0, self.w*self.h)]
        x0, y0 = 0.0, 0.0
        zx = 0.2
        zy = 0.9
        for y in range(0, self.h):
            for x in range(0, self.w):
                self.noise_map[y*self.h+x] = self._noise2d(x0, y0)
                x0 += zx
            y0 += zy

    def _build_gradient_table(self):
        """
        Builds and populates the gradient table using random variations in the width/height
        :return:
        """
        random_generator = random.Random()
        for i in range(0, self.h):
            for j in range(0, self.w):
                x = float((random_generator.randint(1, 2*self.w)) - self.w) / self.h
                y = float((random_generator.randint(1, 2*self.h)) - self.h) / self.w
                s = math.sqrt((x * x) + (y * y))
                if s != 0:
                    x /= s
                    y /= s
                else:
                    x = 0
                    y = 0
                self.gradient_table[i*self.h+j] = (x, y)

    def _dot(self, v1, v2):
        """
        Gets the "dot product" between the gradient vector (v1) and the distance vector (v2).  This determines which
        grid cell to place a specific point.
        :param v1: vector 1 - gradient
        :param v2: vector 2 - distance
        :return: float: dot product
        """
        return (v1[0]*v2[0]) + (v1[1]*v2[1])

    def _gradient(self, x, y):
        return self.gradient_table[y*self.h+x]

    def _curve(self, x):
        return (3*x*x) - (2*x*x*x)

    def _noise2d(self, x, y):
        x0 = math.floor(x)
        y0 = math.floor(y)
        x1 = x0 + 1.0
        y1 = y0 + 1.0
        ix0, ix1, iy0, iy1 = int(x0), int(x1), int(y0), int(y1)
        s = self._dot(self._gradient(ix0, iy0), (x - x0, y - y0))
        t = self._dot(self._gradient(ix1, iy0), (x - x1, y - y0))
        u = self._dot(self._gradient(ix0, iy1), (x - x0, y - y1))
        v = self._dot(self._gradient(ix1, iy1), (x - x1, y - y1))
        sx = self._curve(x - x0)
        a = s + sx*t - sx*s
        b = u + sx*v - sx*u
        sy = self._curve(y - y0)
        return a + sy*b - sy*a
