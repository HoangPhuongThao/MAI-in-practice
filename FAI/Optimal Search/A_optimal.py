import sys
import os
import numpy as np
PATH, TAIL = os.path.split(os.path.abspath(os.getcwd()))
sys.path.insert(1, PATH + '/Heuristic Search Methods')
from network_heuristic import index_heuristic_network
from heuristic_search_alg import detect_loop, check_max_size_queue


def delete_redundant_paths(queue, accumulated_cost_paths):
    sorted_indices = sorted(range(len(accumulated_cost_paths)), key=lambda k: accumulated_cost_paths[k], reverse=True)
    new_queue = queue.copy()
    deleted_indices = []
    for i in sorted_indices:
        path = queue[i]
        endpoint_path = path[-1]
        acc_cost_path = accumulated_cost_paths[i]
        for path2 in new_queue:
            if path2 != path and endpoint_path in path2:
                # print(path, path2)
                path2_index = queue.index(path2)
                acc_cost_path2 = accumulated_cost_paths[path2_index]
                # print(acc_cost_path, acc_cost_path2)
                if acc_cost_path > acc_cost_path2:
                    new_queue.remove(path)
                    deleted_indices.append(i)

    return new_queue, deleted_indices


def A_optimal(goal, network, node_cost):
    '''
    A combination of these algorithms: Uniform Best First, Branch and Bound, Estimate Extended Uniform Cost,
                                       Redundant Path Deletion
    :return: optimal path
    '''

    # initialize a queue, a max size of the queue and a cost and a function f of a path in the queue
    queue = [[0]]
    max_size_queue = sys.getsizeof(queue)
    accumulated_cost_paths = [0]
    f = [0]

    while queue and (goal not in queue[0]):
        # remove the first path in the queue and create new paths to all its children
        front = queue.pop(0)
        cost_front = accumulated_cost_paths.pop(0)
        f.pop(0)
        children = network.return_connections(front[-1])
        new_paths = [front + [child] for child in children]

        # remove new_paths with loops
        deleted_path_indices = [i for i in range(len(new_paths)) if detect_loop(new_paths[i])]
        new_paths = [path for path in new_paths if not detect_loop(path)]
        for i in deleted_path_indices:
            del children[i]

        # f = accumulated_cost(path) + heuristic(endpoint_path)
        accumulated_cost_new_paths = [cost_front + node_cost[child] for child in children]
        accumulated_cost_paths += accumulated_cost_new_paths
        children_heuristic_values = [network.get_heuristic(child) for child in children]
        f += [a + b for a, b in zip(accumulated_cost_new_paths, children_heuristic_values)]

        # add new paths to the queue
        queue += new_paths

        # sort the entire queue by f (ascending order)
        sorted_indices = sorted(range(len(f)), key=lambda k: f[k])
        f.sort()
        queue = [queue[k] for k in sorted_indices]
        accumulated_cost_paths = [accumulated_cost_paths[k] for k in sorted_indices]

        # IF QUEUE contains path P terminating in I, With cost P, and path Q containing I,
        # with cost Q AND cost P > cost Q; THEN delete P;
        queue, deleted_indices = delete_redundant_paths(queue, accumulated_cost_paths)
        for index in deleted_indices:
            del accumulated_cost_paths[index]
            del f[index]
        max_size_queue = check_max_size_queue(max_size_queue, queue)

    return queue.pop(0), max_size_queue


if __name__ == "__main__":
    amountOfNodes = 10
    branchingFactor = 2
    goal = amountOfNodes-1
    network = index_heuristic_network(amountOfNodes, branchingFactor, seed=0)
    print(network.cost_matrix)

    cost = np.random.randint(1,11,amountOfNodes)
    print("Cost vector: ", cost)

    # test delete_redundant_paths function
    # acc_cost = [10, 9, 8]
    # P = [0,1,3,4,5,2]
    # Q = [0,2,6,3,8,9]
    # S = [0,4,9,7]
    # queue = [P, Q, S]
    # queue = delete_redundant_paths(queue, acc_cost)
    # print(queue)

    optimal_path, max_size_queue = A_optimal(goal, network, cost)
    print("Optimal Path found: ", optimal_path)
    print("Max_size_queue: ", max_size_queue)
