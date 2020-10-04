# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 11:44:09 2020

@author: didie & thao
"""
import pandas as pd
import numpy as np
from time import time
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from network import Network
from search_algorithms import depth_first, breadth_first, iterative_deepening
#%%

# initialize dataframe with results
test_results = pd.DataFrame([], columns = ["algorithm","no_of_nodes_network","branching_factor", "average_speed", "average_memory_usage", "average_length_goal_path"])

# select value for the amount of nodes and probabilities of the connectivity
network_nodes = [250, 500, 750, 1000]
branching_factors = [2, 3, 5, 10]

amount_of_test_runs = 10
algorithms = {"depth_first": depth_first, "breadth_first": breadth_first,
            "iterative_deepening": iterative_deepening}

for algorithm_name, algorithm in algorithms.items():
    for nodes in network_nodes:
        for branching_factor in branching_factors:
            # calculate goal node
            goal = nodes - 1
            
            # initialize test variables
            speed = np.zeros(amount_of_test_runs)
            memory_usage = np.zeros(amount_of_test_runs)
            length_goal_path = np.zeros(amount_of_test_runs)

            print("\n", algorithm_name, nodes, branching_factor)
            
            for i in tqdm(range(amount_of_test_runs)):
                network = Network(nodes, branching_factor, seed = i)
                start = time()
                goal_path, memory_usage[i] = algorithm(goal, network)
                speed[i]= time() - start
                length_goal_path[i] = len(goal_path)
            
            # add averaged test values to the data frame
            test_results.loc[len(test_results)] = [algorithm_name,nodes,branching_factor,
                                                   speed.mean(), memory_usage.mean(),
                                                   length_goal_path.mean()]

#%%

combos = [["algorithm","no_of_nodes_network"],["algorithm","branching_factor"]]
variables = ["average_speed", "average_memory_usage", "average_length_goal_path"]

for combo in combos:
    data = test_results.groupby(by = combo).mean()
    for variable in variables:
        data_var = data[[variable]].unstack(level = 0)
        data_var.columns = data_var.columns.droplevel()    
        plt.figure()
        sns.heatmap(data_var, cmap = "Reds").set_title(variable)
        plt.savefig('Evaluation/' + variable + '_' + combo[1] + '.png')
