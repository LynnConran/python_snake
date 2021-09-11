class SnakeStack:

    def __init__(self, y_loc, x_loc):
        self.y_loc = y_loc
        self.x_loc = x_loc
        self.next_snake = None

    # Snake will grow by adding a new head to the chain then popping the last segment,
    # unless the grow variable is set to True.
    def move_loc(self, grow):  # grow is a boolean denoting if the snake has eaten
        if self.next_snake.next_snake is not None:
            self.next_snake.move_loc(grow)
        elif not grow:
            self.next_snake = None

    def check_for_snake(self, y, x):
        if y == self.y_loc and x == self.x_loc:
            return True
        elif self.next_snake is not None:
            return self.next_snake.check_for_snake(y, x)
        return False

    def add_segment(self, y_loc, x_loc):  # For use in snake construction
        if self.next_snake is None:
            self.next_snake = SnakeStack(y_loc, x_loc)
        else:
            self.next_snake.add_segment(y_loc, x_loc)
