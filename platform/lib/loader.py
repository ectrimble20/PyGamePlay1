from platform.constants import IMAGE_DIRECTORY
import os
import pygame


def load_image(file_name):
    file_path = os.path.join(IMAGE_DIRECTORY, file_name)
    if not os.path.isfile(file_path):
        raise FileNotFoundError("Unable to load image file {} expected at {}".format(file_name, IMAGE_DIRECTORY))
    image_surface = pygame.image.load(file_path).convert_alpha()
    if image_surface:
        return image_surface
    else:
        raise RuntimeError("Unable to load image {}, image exists but was unable to be read properly".format(file_path))


# this expects that you're loading from the constants
def load_font(font_file, size):
    if not os.path.isfile(font_file):
        raise FileNotFoundError("Unable to load font file {}, does not exist".format(font_file))
    afs = [12, 18, 24, 36, 48, 60, 72]
    if size not in afs:
        raise RuntimeError("Please select an appropriate font size, {} is not allowed, must be {}".format(size, afs))
    font = pygame.font.Font(font_file, size)
    if font:
        return font
    else:
        raise RuntimeError("Unable to load font {}, file exists but was unable to read properly".format(font_file))
