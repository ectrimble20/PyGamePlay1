from pygame import Rect


class Camera(object):

    def __init__(self, width, height):
        self._half_width = width // 2
        self._half_height = height // 2
        self._pos = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self._pos.topleft)

    def update(self, target):
        self._pos = self._complex_camera(target.rect)

    def _complex_camera(self, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = self._pos
        l, t, _, _ = -l+self._half_width, -t+self._half_height, w, h

        l = min(0, l)                                       # stop scrolling at the left edge
        l = max(-(self._pos.width-self._half_width), l)     # stop scrolling at the right edge
        t = max(-(self._pos.height-self._half_height), t)  # stop scrolling at the bottom
        t = min(0, t)                                       # stop scrolling at the top
        return Rect(l, t, w, h)
