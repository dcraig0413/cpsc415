'''
CPSC 415 -- Homework #2
David Craig, University of Mary Washington, fall 2021
'''

from atlas import Atlas
import numpy as np
import logging
import sys
import math


def find_best_path(atlas):
    '''Finds the best path from src to dest, based on costs from atlas.
    Returns a tuple of two elements. The first is a list of city numbers,
    starting with 0 and ending with atlas.num_cities-1, that gives the
    optimal path between those two cities. The second is the total cost
    of that path.'''

    # fill 2 arrays with inf, size equal to number of cities
    path_costs = (np.zeros(atlas.get_num_cities())) + math.inf
    crow_path_costs = path_costs.copy()

    # set first element of both arrays to 0 before looping
    path_costs[0] = 0
    crow_path_costs[0] = atlas.get_crow_flies_dist(0,atlas.get_num_cities()-1)

    #array of all false values to keep track of when a city is hit
    visited = np.zeros(atlas.get_num_cities())
    path = set()

    while True:
        current_shortest_path = math.inf
        current_shortest_path_index = -1

        #for every path possible
        for i in range(len(crow_path_costs)):
            #keep track of the path with the lowest cost
            if crow_path_costs[i] < current_shortest_path and visited[i] == 0:
                current_shortest_path = crow_path_costs[i]
                current_shortest_path_index = i
        #if there is no path to goal, return a None tuple
        if current_shortest_path_index == -1:
            return None, None

        #once goal node has been reached, use shortest path index to return that path
        elif current_shortest_path_index == atlas.get_num_cities()-1:
            return list(path), path_costs[current_shortest_path_index]

        #for all neighboring cities that a city has a path to
        for i in range(len(atlas._adj_mat[current_shortest_path_index])):
            #if neighbor hasn't been visited
            if atlas._adj_mat[current_shortest_path_index][i] != 0 and not visited[i]:
                #update distance from here to next neighboring city
                if path_costs[current_shortest_path_index] + atlas._adj_mat[current_shortest_path_index][i] < path_costs[i]:
                    path_costs[i] = path_costs[current_shortest_path_index] + atlas._adj_mat[current_shortest_path_index][i]
                    crow_path_costs[i] = path_costs[i] + atlas.get_crow_flies_dist(0,atlas.get_num_cities()-1)
                    atlas.get_road_dist(current_shortest_path_index,atlas.get_num_cities()-1)
                    path.add(i)
                visited[current_shortest_path_index] = 1


if __name__ == '__main__':

    if len(sys.argv) not in [2,3]:
        print("Usage: gps.py numCities|atlasFile [debugLevel].")
        sys.exit(1)

    if len(sys.argv) > 2:
        if sys.argv[2] not in ['DEBUG','INFO','WARNING','ERROR']:
            print('Debug level must be one of: DEBUG, INFO, WARNING, ERROR.')
            sys.exit(2)
        logging.getLogger().setLevel(sys.argv[2])
    else:
        logging.getLogger().setLevel('INFO')

    try:
        num_cities = int(sys.argv[1])
        logging.info('Building random atlas with {} cities...'.format(
            num_cities))
        usa = Atlas(num_cities)
        logging.info('...built.')
    except:
        logging.info('Loading atlas from file {}...'.format(sys.argv[1]))
        usa = Atlas.from_filename(sys.argv[1])
        logging.info('...loaded.')

    path, cost = find_best_path(usa)
    if path != None:
        print('Best path from {} to {} costs {}: {}.'.format(0,
            usa.get_num_cities()-1, cost, path))
    else:
        print("No path found!")
    print('You expanded {} nodes: {}'.format(len(usa._nodes_expanded),
        usa._nodes_expanded))

