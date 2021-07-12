import heapq
import constants
import uuid

class node:
    def __init__(self, coords, gameboard, g, h, f, parent=None) -> None:
        self.position = coords
        self.parent = parent
        self.g = g
        self.h = h
        self.f = f
        self.uuid = uuid.uuid4

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

    def __hash__(self):
        return hash((self.uuid))

    def __gt__(self, other):
        return self.h == other.h

class astar:
    def get_paths(self, start, target, gameboard):
        open_set = set()
        open_heapq = []
        closed_set = set()

        current = node(start, gameboard, 0, self.calculate_h(start, target), 0)
        open_set.add(current)
        open_heapq.append((0, current))

        path = None
        while open_set:
            current = heapq.heappop(open_heapq)[1]

            if current.position == target:
                path = self.get_paths_backtrack_helper(current, start)
                break
            open_set.remove(current)
            closed_set.add(current)
            
            for neighbor in current.neighbors:
                child_h = current.h + 1
                child_g = self.calculate_h(current.position, target)
                child = node(neighbor, gameboard, child_h, child_g, child_h + child_g, current)
                if child in closed_set:
                    continue

                if child not in open_set:
                    open_set.add(child)
                    heapq.heappush(open_heapq, (child.h, child))
            
        return path

    def get_paths_backtrack_helper(self, end_node, start_position):
        path = [end_node.position]
        while end_node.parent.position is not start_position:
            path.append(end_node.parent.position)
            end_node = end_node.parent
        
        path.reverse()
        
        return path
        
    def calculate_h(self, start, target):
        return abs(start[0] - target[0]) + abs(start[1] - target[1])