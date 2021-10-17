from func_Astar import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time

def check_discovered_maze(dim, initial_maze, discovered_maze, knowledged_maze):
    print('------check discovered maze-----')
    for i in range(dim):
        for j in range(dim):
            if initial_maze[i][j] == 1 and discovered_maze[i][j] == 0:
                print('error')
                return False
            if initial_maze[i][j] == 0 and knowledged_maze[i][j] == 1:
                print('error')
                return False
    return True


def generate_simpleMaze(dim, p):
    initial_maze = np.zeros([dim, dim])
    for row in range(dim):
        for col in range(dim):
            if np.random.uniform(0, 1) < p:
                initial_maze[row][col] = 1

    initial_maze[0][0] = 0
    initial_maze[dim - 1][dim - 1] = 0
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


def generate_path_re(current) -> list:

    path = []
    path.append(current) #first cell is goal (dim,dim), and path is put into list in reverse order
    while current.get_parent() is not None:
        current = current.get_parent()
        path.append(current)

    #reverse the list
    i = len(path)-1  #the last cell in the list is (0,0)
    path_re = []
    while i >= 0:
        path_re.append(path[i])
        i = i - 1
    return path_re


#This is used for Q6 agent1
def fun_repeated_Astar_p2(initial_maze, dim ):
    #print('start of one repeated A*')
    start_cell = Cell(0, 0, 0, dim, None)
    #knoledged_maze is the maze used in repeated A*
    #it assumes the undiscovered blocks are unblocked
    knowledged_maze = np.zeros([dim, dim])
    # discovered_maze is the maze used to find shortest path for Question 6,7
    # it assumes the undiscovered blocks are blocked
    discovered_maze = np.ones([dim, dim])
    processed = 0
    explored = 0
    count_rp=0
    count_rp1=0
    count_rp2=0
    total_planning_time = 0

    output_path = []

    while True:
        # planning path using A*
        #print('start A*, the start cell is')
        #print(start_cell.x)
        #print(start_cell.y)
        start_time = time.process_time_ns()
        goal_cell, status, processed = func_Astar2(start_cell, [dim - 1, dim - 1], knowledged_maze, dim, processed)
        end_time = time.process_time_ns()
        if status == 'no_solution':
            return 'no_solution', 0, discovered_maze, processed, explored, count_rp,count_rp1,count_rp2,0

        total_planning_time = total_planning_time + end_time - start_time

        # get the path planned by A*, start from start_cell, end at goal
        path = generate_path_re(goal_cell)
        # check and update knowledge
        isBlock = False
        i=0
        while i < len(path) and isBlock is False:
            current = path[i]
            explored = explored + 1
            output_path.append(current)
            #print('when explore + 1')
            #print(current.x)
            #print(current.y)
            # if one cell along the path is blocked, then replanning
            if initial_maze[current.x, current.y] == 1:
                knowledged_maze[current.x, current.y] = 1
                parent =  current.get_parent()
                start_cell = Cell(parent.x,parent.y,parent.get_gscore(),dim,None,0)
                isBlock = True
                count_rp = count_rp +1
                count_rp1 = count_rp1 + 1
            # if the current cell is not blocked, then update neighbour knowledge
            else:
                discovered_maze[current.x, current.y] = 0
                #####----start: only for Q6, not Q7---------###
                #print('start check children')
                children = current.get_children()
                for child in children:
                    if initial_maze[child[0], child[1]] == 1:
                        knowledged_maze[child[0], child[1]] = 1
                        if i + 1 < len(path):
                            next = path[i + 1]
                            if child[0] == next.x and child[1] == next.y:
                                start_cell = Cell(current.x,current.y,current.get_gscore(),dim,None,0)
                                isBlock = True
                                count_rp = count_rp + 1
                                count_rp2 = count_rp2 + 1
                                #print('children is blocked and on the planned path')
                                #print(next.x)
                                #print(next.y)
                    else:
                        discovered_maze[child[0], child[1]] = 0
                #print('end check children')
                #####----end: only for Q6, not Q7---------###
            #print('end check path')
            i = i + 1
            #print('end i+1')
        # if there is no block along the path, then it is a solution
        if isBlock is False:

            #print('end of one repeated A*')
            return 'solution', len(output_path), discovered_maze, processed, len(output_path), count_rp,count_rp1,count_rp2,total_planning_time
        #print('end check isBlock')

#This is used for Q7 agent2
def fun_repeated_Astar_Q7_p2(initial_maze, dim ):
    #print('start of one repeated A*')
    start_cell = Cell(0, 0, 0, dim, None)
    knowledged_maze = np.zeros([dim, dim])
    discovered_maze = np.ones([dim, dim])
    processed = 0
    explored = 0
    count_rp = 0
    total_planning_time = 0
    output_path = []

    while True:
        # planning path using A*
        start_time = time.process_time_ns()
        goal_cell, status, processed = func_Astar2(start_cell, [dim - 1, dim - 1], knowledged_maze, dim, processed)
        end_time = time.process_time_ns()
        if status == 'no_solution':
            return 'no_solution', 0, discovered_maze, processed, explored, count_rp, 0

        total_planning_time  = total_planning_time + end_time - start_time
        # get the path planned by A*,  start from start_cell, end at goal
        path = generate_path_re(goal_cell)

        # check and update knowledge
        isBlock = False
        i = 0
        while i<len(path) and isBlock is False:
            current = path[i]
            explored = explored +1
            output_path.append(current)
            # if one cell along the path is blocked, then replanning
            if initial_maze[current.x, current.y] == 1:
                knowledged_maze[current.x, current.y] = 1
                parent = current.get_parent()
                start_cell = Cell(parent.x, parent.y, parent.get_gscore(), dim, None, 0)
                isBlock = True
                count_rp = count_rp + 1
            else:
                discovered_maze[current.x, current.y] = 0
            i = i + 1
        # if there is no block along the path, then it is a solution
        if isBlock is False:
            #trajectory = generate_path(goal_cell)
            #print('end of one repeated A*')
            return 'solution', len(output_path), discovered_maze, processed, len(output_path), count_rp, total_planning_time














