import matplotlib.pyplot as plt
import numpy as np


def construct_map(map_array):
    m, n = map_array.shape
    new_map_array = np.zeros((m, n))
    robot_position = np.argwhere(map_array == 'r')[0]
    new_map_array[robot_position[0], robot_position[1]] = -1

    obstacle_positions = np.argwhere(map_array == '*')

    for obstacle_position in obstacle_positions:
        new_map_array[obstacle_position[0], obstacle_position[1]] = 1

    return new_map_array


def display_map(map_array, s=3):
    map_array = np.flipud(map_array)
    x = np.arange(map_array.shape[1])
    y = np.arange(map_array.shape[0])

    plt.imshow(map_array, cmap='gray', interpolation='none', extent=[x.min() - 0.5, x.max() + 0.5, y.min() - 0.5, y.max() + 0.5])

    plt.xticks(x - 0.50, np.arange(x.min(), x.max() + 1) * s)
    plt.yticks(y - 0.50, np.arange(y.min(), y.max() + 1) * s)
    plt.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True)
    plt.gca().invert_yaxis()

    plt.show()


def get_obstacle_coordinates(map_array, s):
    angles = [0, 90, 180, 270]
    obstacle_coordinates = {}

    robot_position = np.where(map_array == -1)
    robot_x, robot_y = robot_position[1][0], robot_position[0][0]

    for angle in angles:
        angle_rad = np.radians(angle)
        dy = int(-np.cos(angle_rad))
        dx = int(np.sin(angle_rad))

        x, y = robot_x, robot_y
        real_x, real_y = robot_x * s, robot_y * s

        while 0 <= x + dx < map_array.shape[1] and 0 <= y + dy < map_array.shape[0] and \
                map_array[y + dy, x + dx] != 1:
            x += dx
            y += dy
            real_x += dx * s
            real_y += dy * s

        obstacle_coordinates[angle] = (real_x + (abs(dy) * 0.5 * s) + (dx == 1) * s, real_y + (abs(dx) * 0.5 * s) + (dy == 1) * s)

    return obstacle_coordinates


s = 1
map_array = np.array([
        [' ', ' ', ' ', ' ', '*', '*', '*'],
        ['*', ' ', 'r', ' ', ' ', ' ', '*'],
        ['*', ' ', ' ', ' ', ' ', ' ', '*'],
        ['*', ' ', ' ', '*', ' ', ' ', '*'],
        ['*', ' ', ' ', ' ', ' ', ' ', ' '],
])

map_array = construct_map(map_array)

obstacle_coordinates = get_obstacle_coordinates(map_array, s)

for angle, coordinates in obstacle_coordinates.items():
    print(f"{angle}: {coordinates}")

display_map(map_array, s)
