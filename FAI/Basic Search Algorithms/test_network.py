from network import Network

network = Network(10, 2, seed=2, costs=[1,2,3], secure_path_to_goal = False)
print(network.cost_matrix)
print(network.probabilities)

# test return_connections function
conn_start = network.return_connections(0)
print("Connections to the start node: " + str(conn_start))

# test get_cost function
print("The cost to get from the start node to node " + str(conn_start[0]) + ' is ' + network.get_cost(0, conn_start[0]))
