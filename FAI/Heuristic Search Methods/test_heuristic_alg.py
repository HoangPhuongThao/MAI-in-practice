import random
import sys
import os
PATH, TAIL = os.path.split(os.path.abspath(os.getcwd()))
sys.path.insert(1, PATH + '/Basic Search Algorithms')
from network import Network
from heuristic_search_alg import hillClimbing1, beamSearch


def generateHeuristicValues(number_of_nodes):
    list = []
    for i in range(number_of_nodes):
        randomInt = random.randint(0,10)
        list.append(randomInt)
    return list


if __name__ == "__main__":
    amountOfNodes = 10
    branchingFactor = 2
    goal = amountOfNodes-1
    network = Network(amountOfNodes, branchingFactor, seed=0, secure_path_to_goal=True)
    heuristicValueList = generateHeuristicValues(network.n)
    print(network.cost_matrix)
    print(heuristicValueList)

    path_hc1, max_size_queue_hc1 = hillClimbing1(goal, network, heuristicValueList)
    print("Hill-climbing 1 Path found: ", path_hc1)
    print("Hill-climbing 1 max_size_queue: ", max_size_queue_hc1)

    path_bs, max_size_queue_bs = beamSearch(goal, network, heuristicValueList)
    print("Beam-search Path found: ", path_bs)
    print("Beam-search max_size_queue: ", max_size_queue_bs)



