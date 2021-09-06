import numpy as np  # I'm too used to arrays
import random
import snake_stack as s_s


def make_grid(y_len, x_len):
    grid = np.zeros((x_len, y_len))
    place_fruit(grid)
    return grid


def make_snake(grid):
    half_point_x = int(len(grid[0]) / 2) - 1
    half_point_y = int(len(grid) / 2) - 1
    head = s_s.SnakeStack(half_point_y, half_point_x)
    for i in range(1, 5):
        head.add_segment(half_point_y, half_point_x - i)
    return head


def draw_snake(grid, head):
    cur_snake = head
    while cur_snake is not None:
        grid[cur_snake.y_loc, cur_snake.x_loc] = 1
        cur_snake = cur_snake.next_snake
    place_fruit(grid)


def place_fruit(grid):
    spots = len(grid) * len(grid[0])
    num = random.randint(0, spots - 1)
    while grid[int(num / len(grid)), num % len(grid[0])] == 1:
        num = random.randint(0, spots - 1)
    grid[int(num / len(grid)), num % len(grid[0])] = 2
    return num


if __name__ == '__main__':
    my_grid = make_grid(10, 10)
    my_head = make_snake(my_grid)
    draw_snake(my_grid, my_head)
    print(my_grid)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
