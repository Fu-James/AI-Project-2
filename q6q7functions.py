from func_Astar import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def generate_simpleMaze(dim, p):
    initial_maze = np.zeros([dim, dim])
    for row in range(dim):
        for col in range(dim):
            if np.random.uniform(0, 1) < p:
                initial_maze[row][col] = 1

    initial_maze[0][0] = 0
    initial_maze[dim - 1][dim - 1] = 0
    return initial_maze


def tiltMaze(dim, p):
    initial_maze = np.zeros([dim,dim])
    for row in range(dim):
        for col in range(row, dim):
            if np.random.uniform(0, 1) < p/2:
                initial_maze[row][col] = 1
        for col in range(0, row):
            if np.random.uniform(0, 1) < p:
                initial_maze[row][col] = 1
    return initial_maze


def printMaze(maze, title):
    cmap = mpl.colors.ListedColormap(['white', 'black', 'red'])
    bounds = [-0.5, 0.5, 1.5, 10]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    plt.imshow(maze,cmap = cmap, norm=norm)
    plt.title(title)
    plt.show()

def generate_path(current) -> list:
    """
    This function will help the agent to find the path between current and their parent cell.

    Returns:
    -------
    path: Returns a path between the current cell and it's parent until the hightes hierarchical parent is found.
    """
    path = []
    path.append(current)
    while current.get_parent() is not None:
        current = current.get_parent()
        path.append(current)
    return path



#This is used for Q6
def fun_repeated_Astar(initial_maze, dim ):

    start_cell = Cell(0, 0, 0, dim, None)
    #knoledged_maze is the maze used in repeated A*
    #it assumes the undiscovered blocks are unblocked
    knowledged_maze = np.zeros([dim, dim])
    # discovered_maze is the maze used to find shortest path for Question 6,7
    # it assumes the undiscovered blocks are blocked
    discovered_maze = np.ones([dim, dim])
    processed = 0

    while True:
        # planning path using A*
        goal_cell, status, processed = func_Astar2(start_cell, [dim - 1, dim - 1], knowledged_maze, dim, processed)
        if status == 'no_solution':
            return 'no_solution', 0, discovered_maze, processed
        # get the path planned by A*, reverse order
        path = generate_path(goal_cell)

        # check and update knowledge
        isBlock = False
        while path and isBlock is False:
            current = path.pop()
            # if one cell along the path is blocked, then replanning
            if initial_maze[current.x, current.y] == 1:
                knowledged_maze[current.x, current.y] = 1
                start_cell = current.get_parent()
                isBlock = True
            # if the current cell is not blocked, then update neighbour knowledge
            else:
                discovered_maze[current.x, current.y] = 0
                children = current.get_children()
                for child in children:
                    if initial_maze[child[0], child[1]] == 1:
                        knowledged_maze[child[0], child[1]] = 1
                    else:
                        discovered_maze[child[0], child[1]] = 0
        # if there is no block along the path, then it is a solution
        if isBlock is False:
            trajectory = generate_path(goal_cell)
            return 'solution', len(trajectory), discovered_maze, processed

#This is used for Q7
def fun_repeated_Astar_Q7(initial_maze, dim ):

    start_cell = Cell(0, 0, 0, dim, None)
    knowledged_maze = np.zeros([dim, dim])
    discovered_maze = np.ones([dim, dim])
    processed = 0

    while True:
        # planning path using A*
        goal_cell, status, processed = func_Astar2(start_cell, [dim - 1, dim - 1], knowledged_maze, dim, processed)
        if status == 'no_solution':
            return 'no_solution', 0, discovered_maze, processed
        # get the path planned by A*, reverse order
        path = generate_path(goal_cell)

        # check and update knowledge
        isBlock = False
        while path and isBlock is False:
            current = path.pop()
            # if one cell along the path is blocked, then replanning
            if initial_maze[current.x, current.y] == 1:
                knowledged_maze[current.x, current.y] = 1
                start_cell = current.get_parent()
                isBlock = True
            else:
                discovered_maze[current.x, current.y] = 0
        # if there is no block along the path, then it is a solution
        if isBlock is False:
            trajectory = generate_path(goal_cell)
            return 'solution', len(trajectory), discovered_maze, processed


#This is for test, not used for answer questions
def fun_repeated_Astar_test(initial_maze, dim ):

    start_cell = Cell(0, 0, 0, dim, None)
    knowledged_maze = np.zeros([dim, dim])
    discovered_maze = np.ones([dim, dim])
    processed = 0

    while True:
        # planning path using A*
        goal_cell, status, processed = func_Astar2(start_cell, [dim - 1, dim - 1], knowledged_maze, dim, processed)
        if status == 'no_solution':
            return 'no_solution', [], discovered_maze, processed, knowledged_maze
        # get the path planned by A*, reverse order
        path = generate_path(goal_cell)

        # check and update knowledge
        isBlock = False
        while path and isBlock is False:
            current = path.pop()
            # if one cell along the path is blocked, then replanning
            if initial_maze[current.x, current.y] == 1:
                knowledged_maze[current.x, current.y] = 1
                start_cell = current.get_parent()
                isBlock = True
            # if the current cell is not blocked, then update neighbour knowledge
            else:
                discovered_maze[current.x, current.y] = 0
                children = current.get_children()
                for child in children:
                    if initial_maze[child[0], child[1]] == 1:
                        knowledged_maze[child[0], child[1]] = 1
                    else:
                        discovered_maze[child[0], child[1]] = 0
        # if there is no block along the path, then it is a solution
        if isBlock is False:
            trajectory = generate_path(goal_cell)
            return 'solution', trajectory, discovered_maze, processed, knowledged_maze


#This is for test, not used for answer questions
def fun_repeated_Astar_tracking(initial_maze, dim ):

    start_cell = Cell(0, 0, 0, dim, None)
    knowledged_maze = np.zeros([dim, dim])
    discovered_maze = np.ones([dim, dim])
    processed = 0

    while True:
        print('-----------start of one loop-----------------')
        print(knowledged_maze)
        # planning path using A*
        print('-------starting point----')
        print(start_cell.x)
        print(start_cell.y)
        print(start_cell.get_gscore())
        print(start_cell.get_heuristic())
        goal_cell, status, processed = func_Astar2(start_cell, [dim - 1, dim - 1], knowledged_maze, dim, processed)
        print('-----------after run one A*-----------------')
        if status == 'no_solution':
            print('-----------no solution from A*-----------------')
            return 'no_solution', [], discovered_maze, processed, knowledged_maze
        # get the path planned by A*, reverse order
        path = generate_path(goal_cell)

        # check and update knowledge
        isBlock = False
        print('-------check planned path----------------')
        while path and isBlock is False:
            current = path.pop()
            # if one cell along the path is blocked, then replanning
            if initial_maze[current.x, current.y] == 1:
                print('-------planned path is blocked----------------')
                knowledged_maze[current.x, current.y] = 1
                start_cell = current.get_parent()
                isBlock = True
            # if the current cell is not blocked, then update neighbour knowledge
            else:
                children = current.get_children()
                for child in children:
                    if initial_maze[child[0], child[1]] == 1:
                        knowledged_maze[child[0], child[1]] = 1
                    else:
                        discovered_maze[child[0], child[1]] = 0
            print('---------------end of planned path-----------')
        # if there is no block along the path, then it is a solution
        if isBlock is False:
            print('-------return solution----------------')
            trajectory = generate_path(goal_cell)
            return 'solution', trajectory, discovered_maze, processed, knowledged_maze
        print('-----------end of one loop-----------------')


