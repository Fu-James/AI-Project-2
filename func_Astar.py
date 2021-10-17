from queue import PriorityQueue
from heuristics import heuristics

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

    def __str__(self) -> str:
        return "Cell({})\ng(n) = {}\nh(n) = {}\nf(n) = {}".format(self._index, self.get_gscore(), self.get_heuristic(), self._fscore)





# PrioritizedItem is used to configure the priority queue
# such that it will only compare the priority, not the item
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PrioritizedItem():
    priority: int
    item: Cell = field(compare=False)





#This is used for question 6 and 7
def func_Astar2(start: Cell, goal: list, maze, dim: int, processed) -> Cell:
    """
    Create a cell.
    Parameters:
    ----------
    start : Initial search point
    goal : x and y coordinate of the goal cell
    maze : Unexplored gridworld
    dim : Dimension of the gridworld as a int.

    Returns:
    -------
    cell, status_string: Returns cell if goal node is found along with a status string.
    """
    fringe = PriorityQueue()
    fringe.put(PrioritizedItem(start.get_fscore(), start))

    visited = set()
    #set is implemented as a hash table in Python
    #We can expect to lookup/insert/delete in O(1) average

    while not fringe.empty():
        current = fringe.get().item
        if current.get_index() in visited:
            continue
        visited.add(current.get_index())
        processed = processed + 1

        if [current.x, current.y] == goal:
            return current, 'solution', processed

        currentg = current.get_gscore()
        children = current.get_children()

        for child in children:
            #maze_child = maze.get_cell(child[0], child[1])#maze_child.get_flag() != 1
            #The three hueristics are all admissible,
            #The first item out of the fringe is optimal
            #So it is sufficient to check visited set before put new cell into the fringe
            if maze[child[0], child[1]] != 1 and (child[0] * dim + child[1] not in visited):
                c = Cell(child[0], child[1], (currentg + 1),
                         dim, parent=current)

                fringe.put(PrioritizedItem(
                    c.get_fscore(), c))
    return None, 'no_solution', processed




