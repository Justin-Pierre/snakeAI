import numpy
import copy

import constants
import visualizer


class game_core:
    def __init__(self, visualize=False):
        self.gameboard = numpy.zeros(
            constants.GAME_DIMENSIONS, dtype=numpy.uint8)

        self.snake = copy.deepcopy(constants.SNAKE_START)
        for coord in constants.SNAKE_START:
            self.gameboard[coord] = 1

        self.new_apple()

        self.step_count = 0
        if visualize:
            self.window = visualizer.snake_visualizer(self.snake, self.apple)
        else:
            self.window = None
        return
    
    def increment_steps(self):
        self.step_count += 1

    def move(self):
        """
        All algorithms must implement this method.
        """
        pass

    def run(self):
        game_won = False
        while game_won is False:
            valid_moves = self.get_valid_moves()
            if not valid_moves:
                if self.window is not None:
                    self.window.deadloop()
                game_won = self.check_win()
                break
            
            self.move(valid_moves)
            self.increment_steps()

            if self.window is not None:
                self.window.draw_board(self.snake, self.apple)
        
        return game_won, self.step_count

    def new_apple(self):
        row, col = numpy.where(self.gameboard == 0)
        if len(row) == 0 and len(col) == 0:
            if not self.check_win():
                print("ERROR: No valid new apple positions, and game is not won.\n" + str(self.gameboard))
                exit(1)
            else:
                # Game is won, we can just return and avoid an error from numpy.random.choice()
                return

        self.apple = (numpy.random.choice(row), numpy.random.choice(col))
        if self.gameboard[self.apple] == 1:
            self.new_apple()

    def move_snake(self, new_pos):
        if new_pos in self.snake:
            print("ERROR: Tried to move into occupied space.")
            exit(1)
        else:
            self.gameboard[new_pos] = 1
            self.snake.insert(0, new_pos)
            if new_pos == self.apple:
                self.new_apple()
            else:
                self.gameboard[self.snake.pop()] = 0

    def get_valid_moves(self):
        head = self.snake[0]
        potential_moves = [(head[0]-1, head[1]), (head[0]+1, head[1]), (head[0], head[1]-1), (head[0], head[1]+1)]
        valid_moves = []
        for move in potential_moves:
            if (move[0] not in range(0,constants.GAME_DIMENSIONS[0])) or (move[1] not in range(0,constants.GAME_DIMENSIONS[1])):
                continue
            if self.gameboard[move] == 1:
                continue

            valid_moves.append(move)
        
        return valid_moves

    def check_win(self):
        if numpy.all(self.gameboard == 1):
            return True
        else:
            return False

    def add_tuple(self, tuple_1, tuple_2):
        return tuple(x+y for x, y in zip(tuple_1, tuple_2))
    
    def subtract_tuple(self, tuple_1, tuple_2):
        return tuple(x-y for x, y in zip(tuple_1, tuple_2))