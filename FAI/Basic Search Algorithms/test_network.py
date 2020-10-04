from network import Network
import search_algorithms as sa
from time import time

network = Network(400, 10, seed=10, costs=[1,2,3], secure_path_to_goal = True)
print(network.cost_matrix)
print(network.probabilities)

# test return_connections function
conn_start = network.return_connections(0)
print("Connections to the start node: " + str(conn_start))

# test get_cost function
print("The cost to get from the start node to node " + str(conn_start[0]) + ' is ' + str(network.get_cost(0, conn_start[0])))
print("depth")
start = time()
print(sa.depth_first(10 - 1, network))
print(time() - start)
print("Breadth")
start = time()
print(sa.breadth_first(10 - 1, network))
print(time() - start)
print("iterative")
start = time()
print(sa.iterative_deepening(10 - 1, network))
print(time() - start)
print("bi-directional")
start = time()
print(sa.bi_directional(10 - 1, network))
print(time() - start)
print("non-determenistic")
start = time()
print(sa.non_deterministic(10 - 1, network))
print(time() - start)