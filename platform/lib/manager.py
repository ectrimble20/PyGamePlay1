class ImageManager(object):

    def __init__(self):
        self._images = {}

    def get_image(self, key):
        return self._images.get(key, None)

    def add_image(self, key, image):
        self._images[key] = image

    def delete_image(self, key):
        del self._images[key]


class FontManager(object):

    def __init__(self):
        self._fonts = {}

    def get_font(self, key):
        return self._fonts.get(key, None)

    def add_font(self, key, font):
        self._fonts[key] = font

    def delete_font(self, key):
        del self._fonts[key]

