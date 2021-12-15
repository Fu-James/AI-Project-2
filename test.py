from example_inference_agent import *
import matplotlib.pyplot as plt
import copy
import time

def group_cell(c1, c2, c3, c4) -> list:
    c_list = []
    c_list.append(c1)
    c_list.append(c2)
    c_list.append(c3)
    c_list.append(c4)
    return c_list

def reverse_list(n) -> list:
    start = time.time()
    l = []
    for i in range(n):
        l.append(i)
    return l.reverse()

def deque_list(n) -> list:
    l = deque()
    for i in range(n):
        l.appendleft(i)
    return list(l)


if __name__ == '__main__':
    # cell_1 = Cell(10, None, 0, 0)
    # cell_2 = Cell(10, None, 1, 1)
    # cell_3 = Cell(10, None, 2, 2)
    # cell_4 = Cell(10, None, 3, 3)
    # cell_list = group_cell(cell_1, cell_2, cell_3, cell_4)
    # cell_1_copy1 = copy.copy(cell_1)
    # cell_1_copy2 = copy.copy(cell_1)
    # cell_1_copy1.update_status(1)
    # cell_1_copy2.update_parent(cell_2)
    # print(cell_1.get_status())
    # print(cell_1_copy1.get_status())
    # print(cell_1_copy2.get_status())
    # print(cell_1_copy2.get_parent())
    # print(cell_1_copy1.get_parent())

    # cell = Cell(10, None, 1, 1)
    # print(cell.get_status().value)
    for _ in range(10):
        maze = GridWorld(101, 0.3, True)
        plt.figure(num="Maze", figsize=(8, 8), tight_layout=True)
        plt.imshow(maze.get_grid_ascii())
        agent = ExampleInferenceAgent(maze)
        path, status_string, _, _ = agent.solve()
        if status_string == 'unsolvable':
            print('unsolvable')
        else:
            solution1 = copy.deepcopy(maze)
            for cell in path:
                solution1.gridworld[cell.x][cell.y].update_status(2)
        # path_astar, status_string = agent.solve_with_only_knowledge()
        # solution2 = copy.deepcopy(maze)
        # for cell in path_astar:
        #     solution2.gridworld[cell.x][cell.y].update_status(2)
        # plt.figure(num="Solved Maze", figsize=(8, 8), tight_layout=True)
        # plt.imshow(solution1.get_grid_ascii())
        # plt.figure(num="Solved Maze with A*", figsize=(8, 8), tight_layout=True)
        # plt.imshow(solution2.get_grid_ascii())
        # plt.show()

    # n = 10000
    # start1 = time.time_ns()
    # list1 = reverse_list(n)
    # end1 = time.time_ns()
    # start2 = time.time_ns()
    # list2 = reverse_list(n)
    # end2 = time.time_ns()
    # print('list 1 took {} time'.format(end1 - start1))
    # print('list 2 took {} time'.format(end2 - start2))

