from example_inference_agent import ExampleInferenceAgent
from gridworld import GridWorld
import numpy as np
import time
import csv

def simulation(dim: int, start_density: float, end_density: float,
               density_increment: float, run_per_density: int):
    count = 0
    density_list = []
    avg_path_len = []
    avg_visited_trajectory_len = []
    avg_plan_time = []
    avg_solve_time = []
    avg_solve_with_astar_time = []
    avg_solve_with_astar_path = []
    for density in np.arange(start_density, end_density, density_increment):
        solve_count = 0
        path_len_sum = 0
        visited_trajectory_len_sum = 0
        plan_time_sum = 0
        solve_time_sum = 0

        solve_with_astar_count = 0
        solve_with_astar_path_sum = 0
        solve_with_astar_time_sum = 0


        for i in range(run_per_density):
            maze = GridWorld(dim, density, True)
            agent = ExampleInferenceAgent(maze)

            start = time.time()
            (path, status_string, 
             plan_time, visited_trajectory_len) = agent.solve()
            end = time.time()

            if(status_string == 'find_the_goal'):
                solve_count += 1
                path_len_sum += len(path)
                visited_trajectory_len_sum += visited_trajectory_len
                plan_time_sum += plan_time
                solve_time_sum += (end - start)

            start = time.time()
            path, status_string = agent.solve_in_discovered_gridworld()
            end = time.time()
            if(status_string == 'find_the_goal'):
                solve_with_astar_count += 1
                solve_with_astar_path_sum += len(path)
                solve_with_astar_time_sum += (end - start)
                
        density_list.append(density)
        avg_path_len.append(path_len_sum / solve_count)
        avg_visited_trajectory_len.append(visited_trajectory_len_sum / solve_count)
        avg_plan_time.append(plan_time_sum / solve_count)
        avg_solve_time.append(solve_time_sum / solve_count)
        
        avg_solve_with_astar_path.append(solve_with_astar_path_sum / solve_with_astar_count)
        avg_solve_with_astar_time.append(solve_with_astar_time_sum / solve_with_astar_count)
    
    return (density_list, avg_path_len, avg_visited_trajectory_len, avg_plan_time, 
            avg_solve_time, avg_solve_with_astar_path, avg_solve_with_astar_time)

def main():
    dim = 101
    start_density = 0
    end_density = 0.33
    density_increment = 0.1
    run_per_density = 100
    (density_list, avg_path_len, avg_visited_trajectory_len, 
     avg_plan_time, avg_solve_time, avg_solve_with_astar_path, 
     avg_solve_with_astar_time) = simulation(dim, start_density, end_density, 
                                             density_increment, run_per_density)
    with open('countries.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(density_list)
        writer.writerow(avg_path_len)
        writer.writerow(avg_visited_trajectory_len)
        writer.writerow(avg_plan_time)
        writer.writerow(avg_solve_time)
        writer.writerow(avg_solve_with_astar_path)
        writer.writerow(avg_solve_with_astar_time)

if __name__ == '__main__':
    main()
