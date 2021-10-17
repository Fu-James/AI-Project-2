from inference_agent_four_rules import InferenceAgentFourExtraRules
from example_inference_agent import ExampleInferenceAgent
import matplotlib.pyplot as plt
from gridworld import GridWorld
from q6q7plots import *
import numpy as np
import time

def time_vs_density_3_vs_4(dim, collection_time_agent_3, collection_time_agent_4):
    font_style = {'family': 'serif', 'color': 'black', 'size': 12}
    title = "Time vs Density"
    plt.figure(num=title, tight_layout=True)
    plt.title(title, fontdict=font_style)

    plt.xlabel("Density", fontdict=font_style)
    plt.ylabel("Time (nanoseconds)", fontdict=font_style)

    plt.plot(density, collection_time_agent_3, label="Agent 3")
    plt.plot(density, collection_time_agent_4, label="Agent 4")

    plt.legend()
    plt.grid()
    filename = f"images/{dim}_x_{dim}_AvgTime_3_vs_4_{iteration}.png"
    plt.savefig(filename)
    plt.close()


def processed_cells_3_vs_4(dim, processed_cells_agent_3, processed_cells_agent_4):
    font_style = {'family': 'serif', 'color': 'black', 'size': 12}
    title = "Processed Cells vs Density"
    plt.figure(num=title, tight_layout=True)
    plt.title(title, fontdict=font_style)

    plt.xlabel("Density", fontdict=font_style)
    plt.ylabel("Number of Cells", fontdict=font_style)

    plt.plot(density, processed_cells_agent_3, label="Agent 3")
    plt.plot(density, processed_cells_agent_4, label="Agent 4")

    plt.legend()
    plt.grid()
    filename = f"images/{dim}_x_{dim}_ProcessCells_3_vs_4_{iteration}.png"
    plt.savefig(filename)
    plt.close()


def processed_cells_vs_all(dim, processed_cells_agent_1, processed_cells_agent_2, processed_cells_agent_3, processed_cells_agent_4):
    font_style = {'family': 'serif', 'color': 'black', 'size': 12}
    title = "Processed Cells vs Density"
    plt.figure(num=title, tight_layout=True)
    plt.title(title, fontdict=font_style)

    plt.xlabel("Density", fontdict=font_style)
    plt.ylabel("Number of Cells", fontdict=font_style)

    plt.plot(density, processed_cells_agent_1, label="Agent 1")
    plt.plot(density, processed_cells_agent_2, label="Agent 2")
    plt.plot(density, processed_cells_agent_3, label="Agent 3")
    plt.plot(density, processed_cells_agent_4, label="Agent 4")

    plt.legend()
    plt.grid()
    filename = f"images/{dim}_x_{dim}_ProcessCells_vs_ALL_{iteration}.png"
    plt.savefig(filename)
    plt.close()
    processed_cells_3_vs_4(dim, processed_cells_agent_3,
                           processed_cells_agent_4)


def average_trajectory_3_vs_4(dim, iteration, average_trajectory_len_agent_3, average_trajectory_len_agent_4):
    font_style = {'family': 'serif', 'color': 'black', 'size': 12}
    title = "Average Trajectory"
    plt.figure(num=title, tight_layout=True)
    plt.title(title, fontdict=font_style)

    plt.xlabel("Density", fontdict=font_style)
    plt.ylabel("Length in Number of Steps", fontdict=font_style)

    plt.plot(density, average_trajectory_len_agent_3, label="Agent 3")
    plt.plot(density, average_trajectory_len_agent_4, label="Agent 4")

    plt.legend()
    plt.grid()
    filename = f"images/{dim}_x_{dim}_AvgTraj_3_vs_4_{iteration}.png"
    plt.savefig(filename)
    plt.close()


def average_trajectory_vs_all(dimensions, density, iteration, huristic_option, stepsize):
    for i, dim in enumerate(dimensions):
        average_trajectory_len_agent_1 = list()
        average_trajectory_len_agent_2 = list()
        average_trajectory_len_agent_3 = list()
        processed_cells_agent_3 = list()
        collection_time_agent_3 = list()
        average_trajectory_len_agent_4 = list()
        processed_cells_agent_4 = list()
        collection_time_agent_4 = list()
        for j, p in enumerate(density):
            sum_trajectory_agent_3 = 0
            sum_proc_cells_agent_3 = 0
            avg_time_agent_3 = 0
            sum_trajectory_agent_4 = 0
            sum_proc_cells_agent_4 = 0
            avg_time_agent_4 = 0
            count_agent_3 = 0
            count_agent_4 = 0
            for i in range(iteration):
                maze = GridWorld(dim, p, True)

                # #Agent 1 UPDATE
                # agent  = InferenceAgentFourExtraRules(maze)
                # trajectory_agent_1, status = agent.solve()
                # if status != 'unsolvable':
                #     sum_trajectory_agent_1 += len(trajectory_agent_1)
                #     count_agent_1 += 1

                # #Agent 2 UPDATE
                # agent  = InferenceAgentFourExtraRules(maze)
                # trajectory_agent_2, status = agent.solve()
                # if status != 'unsolvable':
                #     sum_trajectory_agent_2 += len(trajectory_agent_2)
                #     count_agent_2 += 1

                # ******************************************
                # Agent 3
                # ******************************************
                start_time = time.process_time_ns()
                agent = ExampleInferenceAgent(maze)
                trajectory_agent_3, status, proc_cells_agent_3 = agent.solve()
                end_time = time.process_time_ns()
                if status != 'unsolvable':
                    sum_trajectory_agent_3 += len(trajectory_agent_3)
                    sum_proc_cells_agent_3 += proc_cells_agent_3
                    avg_time_agent_3 += (end_time - start_time)
                    count_agent_3 += 1
                print(f'for {dim} and {p} Agent 3')

                # ******************************************
                # Agent 4 
                # ******************************************
                start_time = time.process_time_ns()
                agent = InferenceAgentFourExtraRules(maze)
                trajectory_agent_4, status, proc_cells_agent_4 = agent.solve()
                end_time = time.process_time_ns()
                if status != 'unsolvable':
                    sum_trajectory_agent_4 += len(trajectory_agent_4)
                    sum_proc_cells_agent_4 += proc_cells_agent_4
                    avg_time_agent_4 += (end_time - start_time)
                    count_agent_4 += 1
                print(f'for {dim} and {p} Agent 4')

            average_trajectory_len_agent_3.append(
                sum_trajectory_agent_3/count_agent_3)
            processed_cells_agent_3.append(
                sum_proc_cells_agent_3/count_agent_3)
            collection_time_agent_3.append(avg_time_agent_3/count_agent_3)

            average_trajectory_len_agent_4.append(
                sum_trajectory_agent_4/count_agent_4)
            processed_cells_agent_4.append(
                sum_proc_cells_agent_4/count_agent_4)
            collection_time_agent_4.append(avg_time_agent_4/count_agent_4)

        font_style = {'family': 'serif', 'color': 'black', 'size': 12}
        title = "Average Trajectory"
        plt.figure(num=title, tight_layout=True)
        plt.title(title, fontdict=font_style)

        plt.xlabel("Density", fontdict=font_style)
        plt.ylabel("Length in Number of Steps", fontdict=font_style)

        average_trajectory_len_agent_1, processed_cells_agent_1 = getQ7Graph(
            dim, p, huristic_option, stepsize, iteration, density)
        average_trajectory_len_agent_2, processed_cells_agent_2 = getQ6Graph(
            dim, p, huristic_option, stepsize, iteration, density)
        plt.plot(density, average_trajectory_len_agent_1, label="Agent 1")
        plt.plot(density, average_trajectory_len_agent_2, label="Agent 2")

        plt.plot(density, average_trajectory_len_agent_3, label="Agent 3")
        plt.plot(density, average_trajectory_len_agent_4, label="Agent 4")

        plt.legend()
        plt.grid()
        filename = f"images/{dim}_x_{dim}_AvgTraj_vs_ALL_{iteration}.png"
        plt.savefig(filename)
        plt.close()
        average_trajectory_3_vs_4(
            dim, iteration, average_trajectory_len_agent_3, average_trajectory_len_agent_4)
        processed_cells_vs_all(dim, processed_cells_agent_1, processed_cells_agent_2,
                               processed_cells_agent_3, processed_cells_agent_4)
        time_vs_density_3_vs_4(dim, collection_time_agent_3,
                               collection_time_agent_4)


if __name__ == '__main__':
    # dimensions = [25, 100]
    # huristic_option = 0
    # stepsize = 0.02
    # density = np.arange(0.0, 0.28, stepsize)
    # iteration = 100
    dimensions = [15, 25, 35, 50]
    huristic_option = 0
    stepsize = 0.02
    density = np.arange(0.0, 0.28, stepsize)
    iteration = 100
    
    average_trajectory_vs_all(
        dimensions, density, iteration, huristic_option, stepsize)
