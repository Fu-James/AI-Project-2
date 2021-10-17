from func_Astar import *
from q6q7functions import *
import numpy as np

#Compas direction
def getQ6Graph(dim, maxP, huristic_option, stepsize, precesion_control, seq_p):
    #Q6
    seq_traj = []
    seq_traj_spD = []
    seq_spD_spF = []
    seq_proc = []


    #Q6
    for p0 in seq_p:
        sum_traj = 0
        sum_traj_spD = 0
        sum_spD_spF = 0
        sum_proc = 0
        count = 0

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
                result, len_trajectory, discovered_maze, processed = fun_repeated_Astar(initial_maze, dim)
                count = count + 1
                sum_traj = sum_traj + len_trajectory
                sum_proc = sum_proc + processed

                ####---sp in discovered maze------###
                final_discoverd, status_disc, num1 = func_Astar2(Cell(0, 0, 0, dim, None), [dim - 1, dim - 1],
                                                                discovered_maze, dim, 0)
                sp_discovered = []
                len_sp_discovered = 0
                if status_disc == 'solution':
                    sp_discovered = generate_path(final_discoverd)
                len_sp_discovered = len(sp_discovered)


                sum_spD_spF = sum_spD_spF + (len_sp_discovered / len_sp_full)
                sum_traj_spD = sum_traj_spD + (len_trajectory/len_sp_discovered)



        ## calculate average
        seq_traj.append(sum_traj/count)
        seq_traj_spD.append(sum_traj_spD/count)
        seq_spD_spF.append(sum_spD_spF/count)
        seq_proc.append(sum_proc/count)

    # print('------sequence Q6------------')
    # print(seq_p)
    # print(seq_traj)
    # print(seq_traj_spD)
    # print(seq_spD_spF)
    # print(seq_proc)


    # ##plot
    # fig, axs = plt.subplots(2,2,figsize=(12,10))
    # axs[0,0].plot(seq_p , seq_traj, color='red')
    # axs[0,0].set_title('average trajectroy')

    # axs[0,1].plot(seq_p , seq_traj_spD, color='red')
    # axs[0,1].set_title('daverage (trajectory/sp in discovered map)')

    # axs[1,0].plot(seq_p , seq_spD_spF, color='red')
    # axs[1,0].set_title('average (sp in discovered map/sp in full map)')

    # axs[1,1].plot(seq_p , seq_proc, color='red')
    # axs[1,1].set_title('average number of processed cell')

    # #fig.show()
    return seq_traj, seq_proc


#direction of attempted motion as the field of view
def getQ7Graph(dim, maxP, huristic_option, stepsize, precesion_control, seq_p):        
    #Q7
    seq_traj_Q7 = []
    seq_traj_spD_Q7 = []
    seq_spD_spF_Q7 = []
    seq_proc_Q7 = []

    #Q7
    for p0 in seq_p:

        sum_traj = 0
        sum_traj_spD = 0
        sum_spD_spF = 0
        sum_proc = 0
        count = 0

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
                result, len_trajectory, discovered_maze, processed = fun_repeated_Astar_Q7(initial_maze, dim)
                count = count + 1
                sum_traj = sum_traj + len_trajectory
                sum_proc = sum_proc + processed

                ####---sp in discovered maze------###
                final_discoverd, status_disc, num1 = func_Astar2(Cell(0, 0, 0, dim, None), [dim - 1, dim - 1],
                                                                discovered_maze, dim, 0)
                sp_discovered = []
                len_sp_discovered = 0
                if status_disc == 'solution':
                    sp_discovered = generate_path(final_discoverd)
                len_sp_discovered = len(sp_discovered)

                sum_spD_spF = sum_spD_spF + (len_sp_discovered / len_sp_full)
                sum_traj_spD = sum_traj_spD + (len_trajectory/len_sp_discovered)


        ## calculate average
        seq_traj_Q7.append(sum_traj/count)
        seq_traj_spD_Q7.append(sum_traj_spD/count)
        seq_spD_spF_Q7.append(sum_spD_spF/count)
        seq_proc_Q7.append(sum_proc/count)


    # print('------sequence Q7------------')
    # print(seq_traj_Q7)
    # print(seq_traj_spD_Q7)
    # print(seq_spD_spF_Q7)
    # print(seq_proc_Q7)

    # ##plot
    # axs[0,0].plot(seq_p , seq_traj_Q7, color='blue')
    # axs[0,1].plot(seq_p , seq_traj_spD_Q7, color='blue')
    # axs[1,0].plot(seq_p , seq_spD_spF_Q7, color='blue')
    # axs[1,1].plot(seq_p , seq_proc_Q7, color='blue')

    # fig.show()
    # plt.show()
    return seq_traj_Q7, seq_proc_Q7