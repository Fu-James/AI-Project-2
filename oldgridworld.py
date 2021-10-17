from heuristics import heuristics
from array import *
import random


class Cell():
    """
    Create a cell.
    Parameters:
    ----------
    x : x-coordinate of the cell
    y : y-coordinate of the cell
    gscore : Length of the shortest path discovered from the initial search point to cell.
    dim : Dimension of the gridworld as a int.
    parent : Parent cell if exists else None
    flag : 
        0 indicates unblocked.
        1 indicates blocked.

    Returns:
    -------
    cell: A object which mainly holds four values.
    g(n), h(n), f(n) and a pointer to parent.
    """
    def __init__(self, x: int, y: int, gscore: int, dim: int, parent=None, flag: int = 0) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self._dim = dim
        self._index = self.x * self._dim + self.y
        self.update_gscore(gscore)
        self.update_parent(parent)
        self._flag = flag
        self._no_of_neighbors = 0
        self._no_of_blocked_neighbors = 0

    def get_heuristic(self) -> float:
        return self._hscore

    def get_gscore(self) -> int:
        return self._gscore

    def get_fscore(self) -> float:
        return self._fscore

    def get_children(self) -> list:
        """
        Create a cell.
        Parameters:
        ----------
        x : x-coordinate of the cell
        y : y-coordinate of the cell
        gscore : Length of the shortest path discovered from the initial search point to cell.
        dim : Dimension of the gridworld as a int.
        parent : Parent cell if exists else None
        flag : 
            0 indicates unblocked.
            1 indicates blocked.

        Returns:
        -------
        children: A list which contains all valid possible neighbours
        """
        children = []
        # Up
        if self.x - 1 >= 0:
            children.append([self.x - 1, self.y])
        # Right
        if self.y + 1 < self._dim:
            children.append([self.x, self.y + 1])
        # Down
        if self.x + 1 < self._dim:
            children.append([self.x + 1, self.y])
        # Left
        if self.y - 1 >= 0:
            children.append([self.x, self.y - 1])
        return children

    def get_parent(self):
        return self._parent

    def get_index(self) -> int:
        return self._index

    def get_flag(self) -> int:
        return self._flag

    def get_no_of_neighbors(self) -> int:
        return self._no_of_neighbors
    
    def get_no_of_blocked_neighbors(self) -> int:
        return self._no_of_blocked_neighbors

    def update_parent(self, parent) -> None:
        self._parent = parent

    def update_flag(self, flag: int) -> None:
        self._flag = flag

    def update_gscore(self, gscore: int) -> None:
        self._gscore = gscore
        self.__update_heuristics()
        self.__update_f()

    def __update_heuristics(self, option: int = 0) -> None:
        self._hscore = heuristics(
            A=[self._dim - 1, self._dim - 1], B=[self.x, self.y], option=option)

    def __update_f(self) -> None:
        self._fscore = self.get_gscore() + self.get_heuristic()

    def update_no_of_neighbors(self, no_of_neighbors) -> None:
        self._no_of_neighbors = no_of_neighbors
    
    def update_no_of_blocked_neighbors(self, no_of_blocked_neighbors) -> None:
        self._no_of_blocked_neighbors = no_of_blocked_neighbors

    def __str__(self) -> str:
        return "Cell({})\ng(n) = {}\nh(n) = {}\nf(n) = {}".format(self._index, self.get_gscore(), self.get_heuristic(), self._fscore)


class Gridworld():
    """
    Create a gridworld with the given dimension and probabilty.
    Parameters:
    ----------
    dim : Dimension of the gridworld as a int.
    p : Probability that each cell would be blocked as a float. (0 < p < 1).

    Returns:
    -------
    gridworld: Gridworld as a 2-D cell array. Dimension is (dim) * (dim).
    Upper left corner(Start) and lower right corner(End) are always unblocked.
    """

    def __init__(self, dim: int, p: float) -> None:
        super().__init__()
        self._dim = dim
        self._density = p
        if self.__valid_input():
            self.gridworld = [[Cell(row, col, 0, self._dim, flag=0) for col in range(
                self._dim)] for row in range(self._dim)]

            for row in range(self._dim):
                for col in range(self._dim):
                    if random.uniform(0, 1) < self._density:
                        self.gridworld[row][col] = Cell(
                            row, col, 0, self._dim, flag=1)

            self.gridworld[0][0] = Cell(0, 0, 0, self._dim, flag=0)
            self.gridworld[self._dim-1][self._dim -
                                        1] = Cell(self._dim-1, self._dim-1, 0, self._dim, flag=0)

    def __valid_input(self):
        """
        Raises an exception if the input is not valid.
        Valid parameter should be a int dim and a float p, which 0 < p < 1.
        Parameters:
        ----------
        dim : Dimension of the gridworld as a int.
        p : Probability that each cell would be blocked as a float. (0 < p < 1).

        Returns:
        -------
        valid_input : True
        """
        if not isinstance(self._dim, int):
            raise TypeError("Argument dim expected to be a int")
        if not isinstance(self._density, float):
            raise TypeError("Argument p expected to be a float")
        if not self._dim > 0:
            raise ValueError("Argument dim should be greater than 0")
        if not 0 <= self._density <= 1:
            raise ValueError(
                "Argument p should be greater than 0 and smaller than 1")
        return True

    def get_cell(self, x: int, y: int) -> Cell:
        return self.gridworld[x][y]

    def get_grid_ascii(self) -> [[int]]:
        return [[self.gridworld[row][col].get_flag() for col in range(self._dim)] for row in range(self._dim)]

    def update_cell(self, cell: Cell, x: int, y: int) -> None:
        self.gridworld[x][y] = cell

    def __str__(self) -> str:
        gridworld = ""
        for row in self.gridworld:
            gridworld += "  ".join([str(cell.get_flag())
                                   for cell in row]) + "\n"
        return gridworldg