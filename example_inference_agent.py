from queue import PriorityQueue
from gridworld import Cell, GridWorld

import copy
from collections import deque

# PrioritizedItem is used to configure the priority queue
# such that it will only compare the priority, not the item
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem():
    priority: int
    item: Cell = field(compare=False)

class ExampleInferenceAgent():
    def __init__(self, maze: GridWorld, option: int = 0):
        self._maze = maze
        self._dim = maze.get_dim()
        self._bump_into_blocked = 0
        self._cells_inferred = 0
        self._goal = [self._dim-1, self._dim-1]
        self._knowledge =GridWorld(self._dim, 0, False)
        for row in range(self._dim):
            for col in range(self._dim):
                if [row, col] in [[0, 0], [0, self._dim-1], 
                                  [self._dim-1, 0], [self._dim-1, self._dim-1]]:
                    self._knowledge.gridworld[row][col].N = 3
                elif row == 0 or row == self._dim - 1 or col == 0 or col == self._dim-1:
                    self._knowledge.gridworld[row][col].N = 5
                else:
                    self._knowledge.gridworld[row][col].N = 8
                self._knowledge.gridworld[row][col].update_option(option)

    def generate_path(self, current: Cell) -> list[Cell]:
        """
        Parameters:
        ----------
        current: The final cell of the path

        Returns:
        -------
        path: A list containing ordered cell along the path
        """
        path = deque()
        while(current is not None):
            path.appendleft(current)
            current = current.get_parent()
        return list(path)
    
    def Astar(self, start: Cell, processed) -> list[Cell, str]:
        """
        Parameters:
        ----------
        start : Initial search point

        Returns:
        -------
        cell, status_string: Returns cell 
                                if goal node is found along with a status string.
        """
        fringe = PriorityQueue()
        fringe.put(PrioritizedItem(start.get_fscore(), 
                   self._knowledge.gridworld[start.x][start.y]))

        visited = set()

        while not fringe.empty():
            current = fringe.get().item
            if current.get_index() in visited:
                continue
            visited.add(current.get_index())
            processed += 1

            if [current.x, current.y] == self._goal:
                return current, 'solution', processed

            current_gscore = current.get_gscore()
            neighbors = self._knowledge.get_4_neighbors(current)

            for neighbor in neighbors:
                if not neighbor.is_blocked() and neighbor.get_index() not in visited:
                    neighbor_copy = copy.copy(neighbor)
                    neighbor_copy.update_gscore(current_gscore + 1)
                    neighbor_copy.update_parent(current)
                    fringe.put(PrioritizedItem(neighbor_copy.get_fscore(), neighbor_copy))

        return None, 'no_solution', processed

    def partial_sensing(self, current: Cell) -> None:
        current.isVisited = True
        neighbors = self._maze.get_8_neighbors(current)
        for neighbor in neighbors:
            if neighbor.is_blocked():
                current.C += 1

    def inference(self, current: Cell) -> bool:
        """
        Parameters:
        ----------
        current: The cell where inference is happening

        Returns:
        -------
        bool: True if sth new is inferenced; else False.
        """
        if not current.isVisited or current.H == 0:
            return False
        neighbors = self._knowledge.get_8_neighbors(current)
        B_new = 0
        E_new = 0
        H_new = 0
        for neighbor in neighbors:
            if neighbor.is_blocked():
                B_new += 1
            elif neighbor.is_empty():
                E_new += 1
            else:
                H_new += 1
        current.H = H_new
        current.B = B_new
        current.E = E_new

        # If blocked neighbors count = blocked neighbors,
        #   all remaining hidden neighbors are unblocked
        if current.C == current.B:
            for neighbor in neighbors:
                if not neighbor.is_blocked():
                    neighbor.update_status(0)
                    self._cells_inferred += 1
            current.H = 0
            return True
        # If neighbors - blocked neighbors = empty neighbors,
        #   all remaining neighbors are blocked
        if current.N - current.C == current.E:
            for neighbor in neighbors:
                if not neighbor.is_empty():
                    neighbor.update_status(1)
                    self._cells_inferred += 1
            current.H = 0
            return True
        return False
    
    def inference_all(self) -> bool:
        """
        Returns:
        -------
        bool: True if sth new is inferenced for any cells; else False.
        """
        new_knowledge = 0
        for row in self._knowledge.gridworld:
            for cell in row:
                if self.inference(cell):
                    new_knowledge += 1
        if new_knowledge == 0:
            return False
        else:
            return True
    
    def inference_path(self, trajectory: list[Cell]) -> bool:
        """
        Returns:
        -------
        bool: True if sth new is inferenced for any cells; else False.
        """
        new_knowledge = 0
        for cell in reversed(trajectory):
            if self.inference(cell):
                new_knowledge += 1
        if new_knowledge == 0:
            return False
        else:
            return True
        
    def is_block_ahead(self, path: list[Cell]) -> bool:
        for cell in path:
            if cell.is_blocked():
                return True
        return False


    def execute_path(self, path: list[Cell], trajectory: list[Cell]) -> list[list[Cell], str]:
        """
        Parameters:
        ----------
        path: A possible solution from the planning stage
        trajectory: All cells being traversed previously

        Returns:
        -------
        status_string: Whether agent walk to the end of the path
        cell: If blocked, return the traversed path before the blocked cell, 
                  else return the full path
        """
        for count, cell in enumerate(path):
            knowledge_cell = self._knowledge.gridworld[cell.x][cell.y]
            if self._maze.gridworld[cell.x][cell.y].is_blocked():
                knowledge_cell.update_status(1)
                self._bump_into_blocked += 1
                # while self.inference_all():
                #     pass
                while self.inference_path(trajectory):
                    pass
                return path[:count], 'blocked'

            knowledge_cell.update_status(0)
            if not knowledge_cell.isVisited:
                self.partial_sensing(knowledge_cell)
            # while self.inference_all():
            #     pass
            while self.inference_path(trajectory):
                pass
            if self.is_block_ahead(path):
                return knowledge_cell, 'blocked'
        return path, 'find_the_goal'

    def solve(self) -> list[list, str]:
        """       
        Returns:
        -------
        path: The path of the solution if there exists
        status_string: Whether the maze is solvable
        """
        processed = 0
        trajectory = []
        end_cell, status_string, processed = self.Astar(self._knowledge.gridworld[0][0], processed)
        while True:
            if status_string == 'no_solution':
                return trajectory, 'unsolvable', processed
            path = self.generate_path(end_cell)
            path, status_string = self.execute_path(path, trajectory)
            trajectory.extend(path)
            if status_string == 'find_the_goal':
                return trajectory, 'find_the_goal', processed
            end_cell, status_string, processed = self.Astar(path[-1], processed)

