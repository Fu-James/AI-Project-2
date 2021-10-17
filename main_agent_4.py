from inference_agent_four_rules import InferenceAgentFourExtraRules
from example_inference_agent import ExampleInferenceAgent
from gridworld import GridWorld, Status
import matplotlib.pyplot as plt
import copy


def print_plt_grid(grid: GridWorld, title):
    plt.figure(figsize=(5, 5))
    plt.title(title)
    plt.imshow([[grid.gridworld[row][col].get_status(
    ).value for col in range(dim)] for row in range(dim)])


def solve_agent(maze, agent, title):
    trajectory, status, processed_cells = agent.solve()
    temp_maze = copy.deepcopy(maze)
    if status != 'unsolvable':
        print("Solution Found")
        for i in range(dim):
            for j in range(dim):
                for ind, v in enumerate(trajectory):
                    if v.x == i and v.y == j:
                        temp_maze.gridworld[i][j].update_status(Status.Walked)
                        agent._knowledge.gridworld[i][j].update_status(
                            Status.Walked)
        # temp_maze.print_grid()
    else:
        print('No Solution!')
    print_plt_grid(temp_maze, title)


if __name__ == '__main__':
    dim = 15
    density = 0.15
    maze = GridWorld(dim, density, True)

    agent = ExampleInferenceAgent(maze)
    solve_agent(maze, agent, "Agent 3")

    agent = InferenceAgentFourExtraRules(maze)
    solve_agent(maze, agent, "Agent 4")

    plt.show()
