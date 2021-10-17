from func_Astar import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from project2_agent12_function import *
import time

dim = 101
maxP = 0.33
huristic_option = 0
stepsize = 0.01
precesion_control = 100

seq_p= np.arange(0,maxP,stepsize)


#Q6 agent 1 start
seq_traj = []
seq_traj_spD = []
seq_spD_spF = []
seq_proc = []


seq_avg_time = []
seq_avg_traj = []
seq_total_traj = []
seq_avg_path = []
seq_avg_explored = []
seq_avg_rp = []
seq_avg_rp1=[]
seq_avg_rp2=[]
seq_avg_planning_time = []


for p0 in seq_p:
    sum_traj = 0
    sum_traj_spD = 0
    sum_spD_spF = 0
    sum_proc = 0
    count = 0
    sum_time = 0
    sum_spD = 0
    sum_explored = 0
    sum_rp = 0
    sum_rp1 = 0
    sum_rp2 = 0
    sum_planning_time = 0

    while count < precesion_control:
        #generate a maze with p0 and run repeated Astar
        #if solution, count +1, save result
        #if no solution, repeat
        initial_maze = generate_simpleMaze(dim, p0)
        #printMaze(initial_maze,'initial')
        ###---sp in full maze------###
        final_full, status_full, num2 = func_Astar2(Cell(0, 0, 0, dim, None), [dim - 1, dim - 1],
                                                   initial_maze, dim, 0)
        sp_full = []
        len_sp_full = 0
        if status_full == 'solution':
            sp_full = generate_path(final_full)
            len_sp_full = len(sp_full)

            ###---run repeated A*--------###
            start_time = time.process_time_ns()
            result, len_trajectory, discovered_maze, processed,explored, rp,rp1,rp2, planning_time = fun_repeated_Astar_p2(initial_maze, dim)
            end_time = time.process_time_ns()
            count = count + 1
            sum_traj = sum_traj + len_trajectory
            sum_proc = sum_proc + processed
            sum_time = sum_time + end_time - start_time
            sum_explored = sum_explored + explored
            sum_rp = sum_rp + rp
            sum_rp1 = sum_rp1 + rp1
            sum_rp2 = sum_rp2 + rp2
            sum_planning_time = sum_planning_time + planning_time
            ####---sp in discovered maze------###
            final_discoverd, status_disc, num1 = func_Astar2(Cell(0, 0, 0, dim, None), [dim - 1, dim - 1],
                                                            discovered_maze, dim, 0)
            sp_discovered = []
            len_sp_discovered = 0
            if status_disc == 'solution':
                sp_discovered = generate_path(final_discoverd)
            len_sp_discovered = len(sp_discovered)

            sum_spD = sum_spD + len_sp_discovered
            sum_spD_spF = sum_spD_spF + (len_sp_discovered / len_sp_full)
            sum_traj_spD = sum_traj_spD + (len_trajectory/len_sp_discovered)


    ## calculate average
    seq_avg_time.append(sum_time/count)
    seq_avg_traj.append(sum_traj/count)
    seq_avg_path.append(sum_spD/count)
    seq_total_traj.append(sum_traj)
    seq_avg_explored.append(sum_explored/count)
    seq_avg_rp.append(sum_rp/count)
    seq_avg_rp1.append(sum_rp1/count)
    seq_avg_rp2.append(sum_rp2/count)
    seq_avg_planning_time.append(sum_planning_time/count)
    print('agent 1, one round for p')
    print(p0)

    print('------sequence Agent 1 ------------')
    print('average trajectory')
    print(seq_avg_traj)
    print('average path')
    print(seq_avg_path)
    print('average time')
    print(seq_avg_time)
    print('total trajectory for 100 times')
    print(seq_total_traj)
    print('average visited/explored cell')
    print(seq_avg_explored)
    print('average number of repeate A*')
    print(seq_avg_rp)
    print('average number of repeate A* due to bump')
    print(seq_avg_rp1)
    print('average number of repeate A* due to see')
    print(seq_avg_rp2)
    print('average total planning time')
    print(seq_avg_planning_time)




#Q7 agent 2 start
seq_traj_Q7 = []
seq_traj_spD_Q7 = []
seq_spD_spF_Q7 = []
seq_proc_Q7 = []



seq_avg_time_Q7 = []
seq_avg_traj_Q7 = []
seq_avg_path_Q7 = []
seq_total_traj_Q7 = []
seq_avg_explored_Q7 = []
seq_avg_rp_Q7 = []
seq_avg_planning_time_Q7 = []


for p0 in seq_p:

    sum_traj = 0
    sum_traj_spD = 0
    sum_spD_spF = 0
    sum_proc = 0
    count = 0
    sum_time = 0
    sum_spD = 0
    sum_explored = 0
    sum_rp = 0
    sum_planning_time = 0

    while count < precesion_control:
        #generate a maze with p0 and run repeated Astar
        #if solution, count +1, save result
        #if no solution, repeat
        initial_maze = generate_simpleMaze(dim, p0)

        ###---sp in full maze------###
        final_full, status_full, num2 = func_Astar2(Cell(0, 0, 0, dim, None), [dim - 1, dim - 1],
                                                   initial_maze, dim, 0)
        sp_full = []
        len_sp_full = 0
        if status_full == 'solution':
            sp_full = generate_path(final_full)
            len_sp_full = len(sp_full)

            ###---run repeated A*--------###
            start_time = time.process_time_ns()
            result, len_trajectory, discovered_maze, processed, explored,rp,planning_time = fun_repeated_Astar_Q7_p2(initial_maze, dim)
            end_time = time.process_time_ns()
            count = count + 1
            sum_traj = sum_traj + len_trajectory
            sum_proc = sum_proc + processed
            sum_time = sum_time + end_time - start_time
            sum_explored = sum_explored + explored
            sum_rp = sum_rp + rp
            sum_planning_time = sum_planning_time + planning_time

            ####---sp in discovered maze------###
            final_discoverd, status_disc, num1 = func_Astar2(Cell(0, 0, 0, dim, None), [dim - 1, dim - 1],
                                                            discovered_maze, dim, 0)
            sp_discovered = []
            len_sp_discovered = 0
            if status_disc == 'solution':
                sp_discovered = generate_path(final_discoverd)
            len_sp_discovered = len(sp_discovered)

            sum_spD = sum_spD + len_sp_discovered
            sum_spD_spF = sum_spD_spF + (len_sp_discovered / len_sp_full)
            sum_traj_spD = sum_traj_spD + (len_trajectory/len_sp_discovered)


    ## calculate average
    seq_avg_time_Q7.append(sum_time / count)
    seq_avg_traj_Q7.append(sum_traj / count)
    seq_avg_path_Q7.append(sum_spD / count)
    seq_total_traj_Q7.append(sum_traj)
    seq_avg_explored_Q7.append(sum_explored/count)
    seq_avg_rp_Q7.append(sum_rp/count)
    seq_avg_planning_time_Q7.append(sum_planning_time/count)
    print('agent 2, one round for p')
    print(p0)


    print('------sequence Agent 2 ------------')
    print('average trajectory')
    print(seq_avg_traj_Q7)
    print('average path')
    print(seq_avg_path_Q7)
    print('average time')
    print(seq_avg_time_Q7)
    print('total trajectory for 100 times')
    print(seq_total_traj_Q7)
    print('average visited/explored cell')
    print(seq_avg_explored_Q7)
    print('average number of repeate A*')
    print(seq_avg_rp_Q7)
    print('average total planning time')
    print(seq_avg_planning_time_Q7)




















