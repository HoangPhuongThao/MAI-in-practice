import random
import sys
import os
PATH, TAIL = os.path.split(os.path.abspath(os.getcwd()))
sys.path.insert(1, PATH + '/Basic Search Algorithms')
from network import Network
from heuristic_search_alg import hillClimbing1


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

    path, max_size_queue = hillClimbing1(goal, network, heuristicValueList)
    print("Path found: ", path)
    print("max_size_queue: ", max_size_queue)
    print(os.path.abspath(os.getcwd()))



