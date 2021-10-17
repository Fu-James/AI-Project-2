from queue import PriorityQueue
from gridworld import Cell, GridWorld, Status
import itertools
import copy
import time
from collections import deque

# PrioritizedItem is used to configure the priority queue
# such that it will only compare the priority, not the item
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PrioritizedItem():
    priority: int
    item: Cell = field(compare=False)


class InferenceAgentFourExtraRules():
    def __init__(self, maze: GridWorld, option: int = 0):
        self._maze = maze
        self._dim = maze.get_dim()
        self._goal = [self._dim-1, self._dim-1]
        self._confirmed_blocked = set()
        self._confirmed_empty = set()
        self._bump_into_blocked = 0
        self._cells_inferred = 0
        self.isInferenceEngine = False
        self._knowledge = GridWorld(self._dim, 0, False)
        for row, row_of_cell in enumerate(self._knowledge.gridworld):
            for col, cell in enumerate(row_of_cell):
                if [row, col] in [[0, 0], [0, self._dim-1],
                                  [self._dim-1, 0], [self._dim-1, self._dim-1]]:
                    cell.N = 3
                elif (row == 0 or row == self._dim - 1
                      or col == 0 or col == self._dim-1):
                    cell.N = 5
                else:
                    cell.N = 8
                cell.update_option(option)

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

    def Astar(self, start: Cell) -> list[Cell, str, int]:
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

            if [current.x, current.y] == self._goal:
                return current, 'solution', len(visited)

            current_gscore = current.get_gscore()
            neighbors = self._knowledge.get_4_neighbors(current)

            for neighbor in neighbors:
                if not neighbor.is_blocked() and neighbor.get_index() not in visited:
                    neighbor_copy = copy.copy(neighbor)
                    neighbor_copy.update_gscore(current_gscore + 1)
                    neighbor_copy.update_parent(current)
                    fringe.put(PrioritizedItem(
                        neighbor_copy.get_fscore(), neighbor_copy))

        return None, 'no_solution', 0

    def partial_sensing(self, current: Cell) -> None:
        current.isVisited = True
        neighbors = self._maze.get_8_neighbors(current)
        for neighbor in neighbors:
            if neighbor.is_blocked():
                current.C += 1

    def update_knowledge(self, current: Cell) -> None:
        neighbors = self._knowledge.get_8_neighbors(current)
        B_new = 0
        E_new = 0
        H_new = 0
        info_gained = 0
        hidden_indexs = set()
        for neighbor in neighbors:
            if neighbor.is_blocked():
                B_new += 1
                info_gained += 1
            elif neighbor.is_empty():
                E_new += 1
                info_gained += 1
            else:
                H_new += 1
                hidden_indexs.add((neighbor.x, neighbor.y))
        if info_gained > current.B + current.E:
            info_gained = True
        else:
            info_gained = False
        current.B = B_new
        current.E = E_new
        current.H = H_new
        if self.isInferenceEngine:
            # if (current.N - current.C) numbers of cells are empty
            # ((current.N - current.C) - current.E) are number of cells are hidden empty
            return hidden_indexs, info_gained, int((current.N - current.C) - current.E)
        return hidden_indexs, info_gained

    def update_assignments(self, count, assignments=[], domains=[Status.Empty, Status.Blocked]):
        if count == 0:
            self.knowledge_equations.append(assignments)
            return
        for domain in domains:
            hold = list(assignments)
            hold.append(domain.value)
            self.update_assignments(count-1, hold)

    def validate_assignment(self, constraint1, constraint2, options):
        index_1, sum_1 = constraint1
        index_2, sum_2 = constraint2

        combine_index = sorted(index_1.union(index_2))
        for key, value in options.items():
            combine_index.remove(key)

        self.knowledge_equations = []
        self.update_assignments(len(combine_index))

        flag = 0
        confirm_assignment = None
        for assignment in self.knowledge_equations:
            if flag > 1:
                break
            assign_index = {}
            assign_index.update(options)
            for index, status in enumerate(assignment):
                assign_index[combine_index[index]] = status

            counter_1 = counter_2 = 0
            for index in index_1:
                counter_1 += assign_index[index]
            for index in index_2:
                counter_2 += assign_index[index]

            if counter_1 == sum_1 and counter_2 == sum_2:
                flag += 1
                confirm_assignment = dict(assign_index)

        return flag == 1, flag == 0, confirm_assignment

    def constraint_engine(self):
        constraints = []
        for row in self._knowledge.gridworld:
            for cell in row:
                if cell.isVisited and not cell.is_unconfirmed():
                    hidden_indexs, info_gained, hidden_empty = self.update_knowledge(
                        cell)
                    if hidden_empty != 0:
                        constraints.append((hidden_indexs, hidden_empty))
        selecting_constraints = list(itertools.combinations(constraints, 2))
        for constraint in selecting_constraints:
            assignments = {}
            domains = [Status.Blocked, Status.Empty]
            potential_cells = sorted(constraint[0][0].union(constraint[1][0]))
            for index in potential_cells:
                exit_flag = False
                for domain in domains:
                    option = {}
                    option[index] = domain.value
                    additional_discovery, discovered, possible_assignment = self.validate_assignment(
                        constraint[0], constraint[-1], option)
                    if discovered:
                        if domain.value:
                            assignments[index] = Status.Blocked.value
                            #print(f'{index} --> Blocked')
                        else:
                            assignments[index] = Status.Empty.value
                            #print(f'{index} --> Empty')
                    elif additional_discovery:
                        if not domain.value:
                            assignments[index] = Status.Blocked.value
                            #print(f'{index} --> Blocked')
                        else:
                            assignments[index] = Status.Empty.value
                            #print(f'{index} --> Empty')
                        assignments.update(possible_assignment)
                        exit_flag = True
                if exit_flag:
                    break

            for key, value in assignments.items():
                knowledge_cell = self._knowledge.gridworld[key[0]][key[1]]
                actual_cell = self._maze.gridworld[key[0]][key[1]]
                # if actual_cell.get_status().value != value:
                #     print("Incorrect")
                if knowledge_cell.is_unconfirmed():
                    if Status(value) == Status.Empty:
                        knowledge_cell.update_status(Status.Empty)
                        self._confirmed_empty.add(knowledge_cell._index)
                        self.update_knowledge(knowledge_cell)
                    else:
                        knowledge_cell.update_status(Status.Blocked)
                        self._confirmed_blocked.add(knowledge_cell._index)
                        self.update_knowledge(knowledge_cell)

    def inference(self, current: Cell) -> list[Cell]:
        """
        Parameters:
        ----------
        current: The cell where inference is happening

        Returns:
        -------
        list[Cell]: A list of neighbors that changed status 
                        because of the inference
        """
        if not current.isVisited:
            return []
        changed_neighbors = []

        # If blocked neighbors count = blocked neighbors,
        #   all remaining hidden neighbors are unblocked
        neighbors = self._knowledge.get_8_neighbors(current)
        if current.C == current.B:
            for neighbor in neighbors:
                if neighbor.is_unconfirmed():
                    changed_neighbors.append(neighbor)
                    neighbor.update_status(Status.Empty)
                    self._cells_inferred += 1
            current.H = 0
            return changed_neighbors

        # If neighbors - blocked neighbors = empty neighbors,
        #   all remaining neighbors are blocked
        if current.N - current.C == current.E:
            for neighbor in neighbors:
                if neighbor.is_unconfirmed():
                    changed_neighbors.append(neighbor)
                    neighbor.update_status(Status.Blocked)
                    self._cells_inferred += 1
            current.H = 0
            return changed_neighbors
        return changed_neighbors

    def inference_neighbors(self, current: Cell, run_inference_engine: bool = True) -> None:
        """
        Parameters:
        ----------
        current: The cell who has it's status changed
        """
        # All neighbors of current should update their knowledge
        #   because the status of current is changed
        neighbors = self._knowledge.get_8_neighbors(current)
        for neighbor in neighbors:
            self.update_knowledge(neighbor)

        # If current is empty then we can apply inference rule on it
        # If some neighbors' status is changed because of the inference
        #   we have to recursive call this method for that neighbor
        if current.is_empty():
            changed_neighbors = self.inference(current)
            for changed_neighbor in changed_neighbors:
                self.inference_neighbors(changed_neighbor)

        if run_inference_engine:
            self.isInferenceEngine = True
            self.constraint_engine()

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
            knowledge_cell = self._knowledge.get_cell(cell.x, cell.y)
            if knowledge_cell.is_blocked():
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
            knowledge_cell = self._knowledge.get_cell(cell.x, cell.y)
            if self._maze.get_cell(cell.x, cell.y).is_blocked():
                knowledge_cell.update_status(Status.Blocked)
                knowledge_cell.isVisited = True
                self.inference_neighbors(knowledge_cell)
                return path[:count], 'blocked'

            knowledge_cell.update_status(Status.Empty)
            if not knowledge_cell.isVisited:
                self.partial_sensing(knowledge_cell)
                self.inference_neighbors(knowledge_cell)
            if self.is_block_ahead(path):
                return path[:count+1], 'blocked'
        return path, 'find_the_goal'

    def solve(self) -> list[list, str, float]:
        """       
        Returns:
        -------
        path: The path of the solution if there exists
        status_string: Whether the maze is solvable
        plan_time: The total time A* search took
        total_visited_trajectory_len: The trajectory length of visited cell
        """
        trajectory = []
        start = time.time()
        (end_cell, status_string,
         total_visited_trajectory_len) = self.Astar(self._knowledge.get_cell(0, 0))
        end = time.time()
        planning_time = (end - start)
        while True:
            if status_string == 'no_solution':
                return trajectory, 'unsolvable', 0, 0
            path = self.generate_path(end_cell)
            path, status_string = self.execute_path(path, trajectory)
            trajectory.extend(path)
            if status_string == 'find_the_goal':
                return (trajectory, 'find_the_goal',
                        planning_time, total_visited_trajectory_len)
            start = time.time()
            (end_cell, status_string,
             visited_trajectory_len) = self.Astar(path[-1])
            end = time.time()
            planning_time += (end - start)
            total_visited_trajectory_len += visited_trajectory_len
