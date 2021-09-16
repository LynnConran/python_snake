import numpy as np  # I'm too used to arrays
import random
import tkinter as tk
import snake_stack as s_s
from pynput import keyboard
import time

fruit = (-1, -1)
snake_dir = 0
running = True
head = s_s.SnakeStack(-1, -1)
WAIT_TIME = 0.25
WIN_X = 500
WIN_Y = 300
PIXELS = 20 # how many pixels should each section of the grid contain

#     1
# 2       0
#     3


def make_grid(y_len, x_len):
    grid = np.zeros((x_len, y_len))
    return grid


# ensures that the snake can't go backwards into itself
def safety_check(dir):
    global head
    if dir == 0:
        if head.next_snake.x_loc == head.x_loc - 1:
            return False
    elif dir == 1:
        if head.next_snake.y_loc == head.y_loc - 1:
            return False
    elif dir == 2:
        if head.next_snake.x_loc == head.x_loc + 1:
            return False
    elif dir == 3:
        if head.next_snake.y_loc == head.y_loc + 1:
            return False
    return True


def on_press(key):
    global snake_dir, running
    if key == keyboard.Key.up:
        if safety_check(1):
            snake_dir = 1
    elif key == keyboard.Key.left:
        if safety_check(2):
            snake_dir = 2
    elif key == keyboard.Key.down:
        if safety_check(3):
            snake_dir = 3
    elif key == keyboard.Key.right:
        if safety_check(0):
            snake_dir = 0
    elif key == keyboard.Key.esc:
        running = False


def make_snake(grid):
    half_point_x = int(len(grid[0]) / 2) - 1
    half_point_y = int(len(grid) / 2) - 1
    global head
    head = s_s.SnakeStack(half_point_y, half_point_x)
    for i in range(1, 5):
        head.add_segment(half_point_y, half_point_x - i)


def draw_snake(grid):
    global head
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
        num_x = random.randint(0, len(grid[0]) - 1)
        num_y = random.randint(0, len(grid) - 1)
        while grid[num_y][num_x] == 1:
            num_x = random.randint(0, len(grid[0]) - 1)
            num_y = random.randint(0, len(grid) - 1)
        fruit = (num_y, num_x)
    grid[fruit[0]][fruit[1]] = 2


# internal method used to move the snake
def move_snake(grid):
    global fruit, head, running
    y_max = len(grid) - 1
    x_max = len(grid[0]) - 1
    if snake_dir == 0:
        if head.x_loc == x_max or head.check_for_snake(head.y_loc, head.x_loc + 1):
            running = False
            return
        new_pos = (head.y_loc, head.x_loc + 1)
    elif snake_dir == 1:
        if head.y_loc == 0 or head.check_for_snake(head.y_loc - 1, head.x_loc):
            running = False
            return
        new_pos = (head.y_loc - 1, head.x_loc)
    elif snake_dir == 2:
        if head.x_loc == 0 or head.check_for_snake(head.y_loc, head.x_loc - 1):
            running = False
            return
        new_pos = (head.y_loc, head.x_loc - 1)
    else:
        if head.y_loc == y_max or head.check_for_snake(head.y_loc + 1, head.x_loc):
            running = False
            return
        new_pos = (head.y_loc + 1, head.x_loc)
    new = s_s.SnakeStack(new_pos[0], new_pos[1])
    new.next_snake = head
    head = new
    grow = new_pos == fruit
    head.move_loc(grow)
    if grow:
        fruit = (-1, -1)
    draw_snake(grid)


def draw_grid(canvas, grid):
    global WIN_X, WIN_Y, PIXELS
    for x in range(int(WIN_X / PIXELS)):
        for y in range(int((WIN_Y - 20) / PIXELS)):
            x1, y1, x2, y2 = x * PIXELS, y * PIXELS, x * PIXELS + PIXELS, y * PIXELS + PIXELS
            if grid[y][x] == 1:
                canvas.create_rectangle(x1, y1, x2, y2, fill='red')
            elif grid[y][x] == 2:
                canvas.create_rectangle(x1, y1, x2, y2, fill='pink')
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill='grey')
    for i in range(int(WIN_X / PIXELS)):
        x1, y1, x2, y2 = i * PIXELS, 20, i * PIXELS, WIN_Y
        canvas.create_line(x1, y1, x2, y2, fill='black')
    for i in range(int((WIN_Y - 20) / PIXELS)):
        x1, y1, x2, y2 = 0, i * PIXELS, WIN_X, i * PIXELS
        canvas.create_line(x1, y1, x2, y2, fill='black')


if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    my_grid = make_grid(int(WIN_X / PIXELS), int((WIN_Y - 20) / PIXELS))
    make_snake(my_grid)
    root = tk.Tk()
    root.title("Snake")
    root.geometry(str(WIN_X) + 'x' + str(WIN_Y))
    canvas = tk.Canvas(root, height=WIN_Y, width=WIN_X, bg="grey")
    draw_grid(canvas, my_grid)
    canvas.pack()
    label = tk.Label(root, textvar="Hello, World!", bg="yellow").place(x=0, y=0)
    root.update()

    while running:
        time.sleep(WAIT_TIME)
        move_snake(my_grid)
        draw_grid(canvas, my_grid)
        root.update()
