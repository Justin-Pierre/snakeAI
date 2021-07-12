import game_core
import astar

class astar_hamiltonian(game_core.game_core):
    """
    A* based algorithm
    """

    def __init__(self, visualize=False):
        super().__init__(visualize)
        self.path = []

    def move(self, valid_moves):
        if not self.path:
            self.path = astar.astar().get_paths(self.snake[0], self.apple, self.gameboard)
            if not self.path:
                self.path = [valid_moves[0]]
        
        next_move = self.path.pop(0)
        if next_move not in valid_moves:
            print("ERROR: Invalid move calculated in 'astar_al'")

        self.move_snake(next_move)
    
    def find_move_towards(self, point, valid_moves):
        direction = self.subtract_tuple(point, self.snake[0])
        direction = (max(-1, min(1, direction[0])), max(-1, min(1, direction[1])))
        desired_move = self.add_tuple(direction, self.snake[0])

        if desired_move in valid_moves:
            return desired_move
        else:
            print("ERROR: Invalid move calculated in 'fixed'")
            if self.window is not None:
                self.window.deadloop()
            exit(1)