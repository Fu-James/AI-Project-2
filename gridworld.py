import random
import enum
from heuristics import heuristics


class Status(enum.Enum):
    Empty = 0
    Blocked = 1
    Unconfirmed = 2


class Cell():
    def __init__(self, dim: int, parent, x: int = 0, y: int = 0, N: int = 0, isVisited: bool = False, status: Status = Status.Unconfirmed, C: int = 0, B: int = 0, E: int = 0, H: int = 0, gscore: int = 0, option: int = 0) -> None:
        self.x = x
        self.y = y
        self.dim = dim
        self.index = self.x * self.dim + self.y
        self.gscore = gscore
        self.update_option(option)
        self.update_gscore(gscore)
        self.update_parent(parent)
        # The number of neighbors cell x has.
        self.N = N
        # Whether or not cell x has been visited.
        self.isVisited = isVisited
        # Whether or not cell x has been confirmed as empty or blocked, or is currently unconfirmed.
        self.status = status
        # The number of neighbors of x that are sensed to be blocked.
        self.C = C
        # The number of neighbors of x that have been confirmed to be blocked.
        self.B = B
        # The number of neighbors of x that have been confirmed to be empty.
        self.E = E
        # The number of neighbors of x that are still hidden or unconfirmed either way
        self.H = H

    def update_parent(self, parent) -> None:
        self.parent = parent

    def update_option(self, option: int):
        self.option = option
        self.update_heuristics()

    def update_gscore(self, gscore: int) -> None:
        self.gscore = gscore
        self.update_f()

    def update_heuristics(self) -> None:
        self.hscore = heuristics(
            A=[self.dim - 1, self.dim - 1], B=[self.x, self.y], option=self.option)
        self.update_f()

    def update_f(self) -> None:
        self.fscore = self.gscore + self.hscore

    def get_index(self) -> int:
        return self.index
    
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


class GridWorld():
    def __init__(self, dim: int, density: float) -> None:
        self.dim = dim
        self.density = density
        self.knowledge = [[Cell(dim, None, x, y) for y in range(self.dim)] for x in range(self.dim)]
        self.knowledge[0][0] = Cell(
            self.dim, None, 0, 0, 3, False, Status.Empty)
        self.create_grid()

    def create_grid(self):
        gridworld = [[None for i in range(self.dim)] for i in range(self.dim)]
        for row in range(self.dim):
            for col in range(self.dim):
                neighbhors = self.get_N(row, col)
                gridworld[row][col] = Cell(
                    self.dim, None, row, col, neighbhors, False, Status.Empty)
                if random.uniform(0, 1) < self.density:
                    gridworld[row][col].status = Status.Blocked

        gridworld[0][0] = Cell(self.dim, None, 0, 0, 3, False, Status.Empty)
        gridworld[self.dim-1][self.dim -
                              1] = Cell(self.dim, None, self.dim-1, self.dim-1, 3, False, Status.Empty)

        for row in range(self.dim):
            for col in range(self.dim):
                current = gridworld[row][col]
                if current.status == Status.Blocked:
                    for child in current.get_8_children():
                        current_neighbor = gridworld[child[0]][child[1]]
                        current_neighbor.C += 1
                        current_neighbor.B += 1
                        current_neighbor.E = current_neighbor.N - current_neighbor.C

        self.gridworld = gridworld

    def get_N(self, row: int, col: int) -> int:
        if [row, col] in [[0, 0], [0, self.dim-1], [self.dim-1, 0], [self.dim-1, self.dim-1]]:
            return 3
        elif row == 0 or row == self.dim - 1 or col == 0 or col == self.dim-1:
            return 5
        else:
            return 8

    def print_grid(self, option: str = "") -> str:
        maze = ""
        if option == "knowledge":
            for row in self.knowledge:
                maze += "  ".join([str(cell.status.value)
                                  for cell in row]) + "\n"
            print("Option:{} Knowledge Gridworld".format(
                str(self.knowledge[0][0].option)))
            print(maze)
        else:
            for row in self.gridworld:
                maze += "  ".join([str(cell.status.value)
                                  for cell in row]) + "\n"
            print("Option:{} Gridworld".format(
                str(self.gridworld[0][0].option)))
            print(maze)
