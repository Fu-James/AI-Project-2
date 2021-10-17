import random
import enum
from heuristics import heuristics


class Status(enum.Enum):
    Empty = 0
    Blocked = 1
    Unconfirmed = 2


class Cell():
    def __init__(self, dim: int, parent, x: int = 0, y: int = 0, N: int = 0, 
                 isVisited: bool = False, status: Status = Status.Unconfirmed, 
                 C: int = 0, B: int = 0, E: int = 0, H: int = 8, gscore: int = 0, 
                 option: int = 0) -> None:
        self.x = x
        self.y = y
        self.dim = dim
        self._index = self.x * self.dim + self.y
        self.gscore = gscore
        self.update_option(option)
        self.update_parent(parent)
        # The number of neighbors cell x has.
        self.N = N
        # Whether or not cell x has been visited.
        self.isVisited = isVisited
        # Whether or not cell x has been confirmed as empty or blocked, or is currently unconfirmed.
        self._status = status
        # The number of neighbors of x that are sensed to be blocked.
        self.C = C
        # The number of neighbors of x that have been confirmed to be blocked.
        self.B = B
        # The number of neighbors of x that have been confirmed to be empty.
        self.E = E
        # The number of neighbors of x that are still hidden or unconfirmed either way
        self.H = H

    def update_parent(self, parent) -> None:
        self._parent = parent

    def update_option(self, option: int):
        self.option = option
        self.update_hscore()

    def update_gscore(self, gscore: int) -> None:
        self.gscore = gscore
        self.update_fscore()
    
    def get_gscore(self) -> float:
        return self.gscore

    def update_hscore(self) -> None:
        self.hscore = heuristics(
            A=[self.dim - 1, self.dim - 1], B=[self.x, self.y], option=self.option)
        self.update_fscore()

    def update_fscore(self) -> None:
        self.fscore = self.gscore + self.hscore

    def get_fscore(self) -> float:
        return self.fscore

    def get_index(self) -> int:
        return self._index
    
    def get_parent(self):
        return self._parent        

    def get_4_children(self) -> list:
        children = []
        # N
        if self.x - 1 >= 0:
            children.append([self.x - 1, self.y])
        # E
        if self.y + 1 < self.dim:
            children.append([self.x, self.y + 1])
        # S
        if self.x + 1 < self.dim:
            children.append([self.x + 1, self.y])
        # W
        if self.y - 1 >= 0:
            children.append([self.x, self.y - 1])
        return children

    def get_8_children(self):
        # N, S, E, W
        children = self.get_4_children()
        # NW
        if self.x - 1 >= 0 and self.y-1 >= 0:
            children.append([self.x-1, self.y-1])
        # NE
        if self.x - 1 >= 0 and self.y+1 < self.dim:
            children.append([self.x-1, self.y+1])
        # SW
        if self.x + 1 < self.dim and self.y-1 >= 0:
            children.append([self.x+1, self.y-1])
        # SE
        if self.x+1 < self.dim and self.y+1 < self.dim:
            children.append([self.x+1, self.y+1])
        return children

    def update_status(self, s: int):
        self._status = Status(s)

    def get_status(self) -> Status:
        return self._status

    def is_blocked(self) -> bool:
        return self._status is Status.Blocked

    def is_empty(self) -> bool:
        return self._status is Status.Empty
    
    def is_unconfirmed(self) -> bool:
        return self._status is Status.Unconfirmed


class GridWorld():
    def __init__(self, dim: int, density: float, is_maze: bool) -> None:
        self._dim = dim
        self._density = density
        self._is_maze = is_maze
        if self._is_maze:
            self.create_maze()
        else:
            self.create_knowledge()

    def create_maze(self):
        maze = [[None for i in range(self._dim)] for i in range(self._dim)]
        for row in range(self._dim):
            for col in range(self._dim):
                maze[row][col] = Cell(self._dim, None, row, col, status=Status.Empty)
                if random.uniform(0, 1) < self._density:
                    maze[row][col].update_status(Status.Blocked)

        maze[0][0] = Cell(self._dim, None, 0, 0, 3, False, Status.Empty)
        maze[self._dim-1][self._dim-1] = Cell(self._dim, None, self._dim-1,
                                            self._dim-1, 3, False, Status.Empty)

        self.gridworld = maze

    def create_knowledge(self):
        knowledge = [[Cell(self._dim, None, x, y) for y in range(self._dim)]
                     for x in range(self._dim)]
        self.gridworld = knowledge

    def get_N(self, row: int, col: int) -> int:
        if ([row, col] in [[0, 0], [0, self.dim-1], 
                          [self.dim-1, 0], [self.dim-1, self.dim-1]]):
            return 3
        elif row == 0 or row == self.dim - 1 or col == 0 or col == self.dim-1:
            return 5
        else:
            return 8
    
    def get_dim(self) -> int:
        return self._dim
    
    def get_cell(self, x: int, y: int) -> Cell:
        if not 0 <= x < self._dim:
            raise ValueError("Index x should be in the interval [0, dim)")
        if not 0 <= y < self._dim:
            raise ValueError("Index y should be in the interval [0, dim)")
        return self.gridworld[x][y]

    def get_4_neighbors(self, current: Cell) -> list[Cell]:
        neighbors = []
        # N
        if current.x - 1 >= 0:
            neighbors.append(self.gridworld[current.x-1][current.y])
        # E
        if current.y + 1 < self._dim:
            neighbors.append(self.gridworld[current.x][current.y+1])
        # S
        if current.x + 1 < self._dim:
            neighbors.append(self.gridworld[current.x+1][current.y])
        # W
        if current.y - 1 >= 0:
            neighbors.append(self.gridworld[current.x][current.y-1])   
        return neighbors
    
    def get_8_neighbors(self, current: Cell) -> list[Cell]:
        # N, S, E, W
        neighbors = self.get_4_neighbors(current)
        # NW
        if current.x - 1 >= 0 and current.y - 1 >= 0:
            neighbors.append(self.gridworld[current.x-1][current.y-1])
        # NE
        if current.x - 1 >= 0 and current.y + 1 < self._dim:
            neighbors.append(self.gridworld[current.x-1][current.y+1])
        # SW
        if current.x + 1 < self._dim and current.y - 1 >= 0:
            neighbors.append(self.gridworld[current.x+1][current.y-1])
        # SE
        if current.x + 1 < self._dim and current.y + 1 < self._dim:
            neighbors.append(self.gridworld[current.x+1][current.y+1])
        return neighbors  

    def print_grid(self) -> str:
        maze = ""
        for row in self.gridworld:
            maze += "  ".join([str(cell.get_status().value)
                                for cell in row]) + "\n"
        if self._is_maze:
            print("Option:{} Maze".format(
            str(self.gridworld[0][0].option), self._is_maze))
        else:
            print("Option:{} Knowledge".format(
            str(self.gridworld[0][0].option), self._is_maze))
        print(maze)

    def get_grid_ascii(self) -> list[list[int]]:
        return [[cell.get_status().value for cell in row] for row in self.gridworld]
