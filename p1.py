from p1_support import load_level, show_level, save_level_costs
#from math import inf, sqrt
import math
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    unvisited = set()
    dist = {}
    prev = {}

    for v in graph['spaces']:
        dist[v] = math.inf
        prev[v] = None
        unvisited.add(v)

    for v in graph['waypoints']:
        dist[v] = math.inf
        prev[v] = None
        unvisited.add(v)

    adj_cells = adj(graph, initial_position)
    print(adj_cells)
    print(adj_cells[1])
    get_min_cost(adj_cells)
   # while len(unvisited) > 0:
    #    u =

    dist[initial_position] = 0


def get_min_cost(adj):
    j = math.inf

    for i in adj:
        if j > i[1]:
            j = i[1]
            k = i[0]

    return j,k


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    pass


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """

    if cell not in level['walls']:
        adj = [(cell[0]+1,cell[1]), (cell[0]-1,cell[1]), (cell[0],cell[1]+1), (cell[0],cell[1]-1), (cell[0]+1,cell[1]+1),
              (cell[0]-1,cell[1]-1), (cell[0]+1,cell[1]-1), (cell[0]-1,cell[1]+1)]

        true = []
        j = 0
        for i in adj:
            weight = 0
            if i in level['spaces']:
                if j < 3:
                    weight = (level['spaces'][cell] * 0.5) + (level['spaces'][adj[j]] * 0.5)
                else:
                    weight = (level['spaces'][cell] * math.sqrt(2)) + (level['spaces'][adj[j]] * math.sqrt(2))
                true.append((adj[j], weight))
            elif i in level['waypoints']:
                if j < 3:
                    weight = (level['spaces'][cell] * 0.5) + (1 * 0.5)
                else:
                    weight = (level['spaces'][cell] * math.sqrt(2)) + (1 * math.sqrt(2))
                true.append((adj[j], weight))

            j += 1

        if len(true) > 0:
            return true

def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    #navigation_edges(level,(14,9))

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    #if path:
    #    show_level(level, path)
    #else:
    #    print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'example.txt','a','e'

    #show_level(load_level(filename))

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    # cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
