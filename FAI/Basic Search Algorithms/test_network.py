from network import Network

network = Network(10, 2, seed=2, costs=[1,2,3], secure_path_to_goal = False)
print(network.cost_matrix)
print(network.probabilities)
