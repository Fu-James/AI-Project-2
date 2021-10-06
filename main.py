from gridworld import GridWorld
import copy

def update_grid_heuristics(option: int, g: GridWorld) -> GridWorld:
    g_copy = copy.deepcopy(g)
    for row in range(len(g_copy.knowledge)):
        for col in range(len(g_copy.knowledge)):
            g_copy.knowledge[row][col].update_option(option)
            g_copy.gridworld[row][col].update_option(option)
    return g_copy


if __name__ == '__main__':
    dim = 5
    density = 0.15
    grid = GridWorld(dim, density)
    grid.print_grid()
    grid.print_grid("knowledge")
