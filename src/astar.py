import constants

class node:
    def __init__(self, coords, gameboard, g, h, f, parent=None) -> None:
        self.position = coords
        self.parent = parent
        self.g = g
        self.h = h
        self.f = f

        self.neighbors = []

        potential_neighbors = [(coords[0]-1, coords[1]), (coords[0]+1, coords[1]), (coords[0], coords[1]-1), (coords[0], coords[1]+1)]
        for neighbor in potential_neighbors:
            if (neighbor[0] not in range(0,constants.GAME_DIMENSIONS[0])) or (neighbor[1] not in range(0,constants.GAME_DIMENSIONS[1])):
                continue
            if gameboard[neighbor] == 1:
                continue

            self.neighbors.append(neighbor)
        
    def __eq__(self, other):
        return self.position == other.position

class astar:
    def get_paths(self, start, target, gameboard):
        open_list = [node(start, gameboard, 0, self.calculate_h(start, target), 0)]
        closed_list = []

        path = None
        while open_list:
            open_list.sort(key=lambda x: x.g)
            current = open_list.pop(0)
            closed_list.append(current)

            if current.position == target:
                path = self.get_paths_backtrack_helper(current, start)
                break
            
            for neighbor in current.neighbors:
                child_h = current.h + 1
                child_g = self.calculate_h(current.position, target)
                child = node(neighbor, gameboard, child_h, child_g, child_h + child_g, current)
                if child in closed_list:
                    continue

                if child in open_list:
                    if child.g > open_list[open_list.index(child)].g:
                        continue
                
                open_list.append(child)
            
        return path

    def get_paths_backtrack_helper(self, end_node, start_position):
        path = [end_node.position]
        while end_node.parent.position is not start_position:
            path.insert(0, end_node.parent.position)
            end_node = end_node.parent
        
        return path
        
    def calculate_h(self, start, target):
        return abs(start[0] - target[0]) + abs(start[1] - target[1])