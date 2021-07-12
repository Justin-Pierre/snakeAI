
from numpy import empty
from game_core import game_core

import game_core

class fixed(game_core.game_core):
    """
    Follows a constant, basic hamiltonian cycle. Inefficient, but guarenteed to work.
    """

    def __init__(self, visualize=False):
        super().__init__(visualize)

        self.move_targets = [(0, 0), (29, 0), (29, 1), (1, 1), (1, 2), (29, 2), (29, 3), (1, 3), (1, 4), (29, 4), (29, 5), (1, 5), (1, 6), (29, 6), (29, 7), (1, 7), (1, 8), (29, 8), (29, 9), (1, 9), (1, 10), (29, 10), (29, 11), (1, 11), (1, 12), (29, 12), (29, 13), (1, 13), (1, 14), (29, 14), (29, 15), (1, 15), (1, 16), (29, 16), (29, 17), (1, 17), (1, 18), (29, 18), (29, 19), (1, 19), (1, 20), (29, 20), (29, 21), (1, 21), (1, 22), (29, 22), (29, 23), (1, 23), (1, 24), (29, 24), (29, 25), (1, 25), (1, 26), (29, 26), (29, 27), (1, 27), (1, 28), (29, 28), (29, 29), (0, 29)]
        # Since the snake always starts at the same spot, we can start in the middle of the
        # fixed hamiltonian path.
        self.current_target_index = 31

    def move(self, valid_moves):
        move = self.find_move_towards(self.move_targets[self.current_target_index], valid_moves)
        if move == self.move_targets[self.current_target_index]:
            self.current_target_index += 1
            if self.current_target_index == len(self.move_targets):
                self.current_target_index = 0
        self.move_snake(move)
    
    def find_move_towards(self, point, valid_moves):
        direction = self.subtract_tuple(point, self.snake[0])
        direction = (max(-1, min(1, direction[0])), max(-1, min(1, direction[1])))
        desired_move = self.add_tuple(direction, self.snake[0])

        if desired_move in valid_moves:
            return desired_move
        else:
            print("ERROR: Invalid move calculated in basic_hamiltonian_cycle")
            if self.window is not None:
                self.window.deadloop()
            exit(1)
        