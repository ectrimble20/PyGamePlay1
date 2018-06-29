from platform.model.world.generate import generate_height_map


if __name__ == '__main__':

    height_map = generate_height_map(800, 600)

    print(height_map)
