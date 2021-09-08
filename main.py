import numpy as np  # I'm too used to arrays
import random
import snake_stack as s_s
from pynput import keyboard

fruit = (-1, -1)
snake_dir = 0
running = True

#     1
# 2       0
#     3


def make_grid(y_len, x_len):
    grid = np.zeros((x_len, y_len))
    return grid


def on_press(key):
    global snake_dir, running
    if key == keyboard.Key.up:
        snake_dir = 1
    elif key == keyboard.Key.left:
        snake_dir = 2
    elif key == keyboard.Key.down:
        snake_dir = 3
    elif key == keyboard.Key.right:
        snake_dir = 0
    elif key == keyboard.Key.esc:
        running = False


def make_snake(grid):
    half_point_x = int(len(grid[0]) / 2) - 1
    half_point_y = int(len(grid) / 2) - 1
    head = s_s.SnakeStack(half_point_y, half_point_x)
    for i in range(1, 5):
        head.add_segment(half_point_y, half_point_x - i)
    return head


def draw_snake(grid, head):
    cur_snake = head
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = 0
    while cur_snake is not None:
        grid[cur_snake.y_loc, cur_snake.x_loc] = 1
        cur_snake = cur_snake.next_snake
    place_fruit(grid)


def place_fruit(grid):
    global fruit
    if fruit == (-1, -1):
        spots = len(grid) * len(grid[0])
        num = random.randint(0, spots - 1)
        while grid[int(num / len(grid)), num % len(grid[0])] == 1:
            num = random.randint(0, spots - 1)
        fruit = (int(num / len(grid)), num % len(grid[0]))
    grid[fruit[0]][fruit[1]] = 2


def move_snake(grid, head):
    if snake_dir == 0:
        new_pos = (head.y_loc, head.x_loc + 1)
    elif snake_dir == 1:
        new_pos = (head.y_loc - 1, head.x_loc)
    elif snake_dir == 2:
        new_pos = (head.y_loc, head.x_loc - 1)
    else:
        new_pos = (head.y_loc + 1, head.x_loc)
    new = s_s.SnakeStack(new_pos[0], new_pos[1])
    new.next_snake = head
    head = new
    global fruit
    grow = new_pos == fruit
    head.move_loc(grow)
    if grow:
        fruit = (-1, -1)
    draw_snake(grid, head)
    return head


if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    my_grid = make_grid(10, 10)
    my_head = make_snake(my_grid)
    my_head = move_snake(my_grid, my_head)
    my_head = move_snake(my_grid, my_head)
    print(my_grid)
    while running:
        pass
