# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 11:32:52 2020

@author: didie
"""
import random
import numpy as np
class Network():
    
    '''
    Design a network of nodes by creating a matrix with the cost from
    each node to another.
    '''
    
    def __init__(self, amount_of_nodes, branching_factor, seed = 0, costs = [1],
                 cost_probabilities = [], secure_path_to_goal = True):
        
        '''
        In the cost matrix the start nodes are on the rows and the end
        nodes are on the columns. The cost from a node to itself must be
        NA, therefore, the diagonal must be NA. The matrix must also be
        symmetric, so that the cost from node A to node B is the same as from 
        node B to node A. Each network contains at least one path from the 
        start to the end node.
        '''

        self.n = amount_of_nodes
        
        if branching_factor > amount_of_nodes:
            print("branching factor cannot be more than number of nodes")
            ValueError
        
        random.seed(seed)
        
        # amount of generated costs should be equal to the lower 
        # triangular of the cost matrix
        amount_of_costs = int((amount_of_nodes - 1) * amount_of_nodes / 2)
        
        amount_of_connections = branching_factor * amount_of_nodes / 2
        
        # probability of having a connection multiplied by 10000 and rounded
        probability_connection = int(amount_of_connections / amount_of_costs * 10000)
        
        # if probability per cost is not defined assume that the probability is equal
        if not cost_probabilities:
            
            # equal probability of a connection for each cost
            prabability_each_cost = probability_connection / len(costs)
            
            probabilities = [10000 - probability_connection] + [prabability_each_cost] * len(costs)
        else:
            if len(costs) != len(cost_probabilities):
                print("list of costs is not equal to list of cost probabilities")
                ValueError
            # standardize the probabilities to be equal to 1 and multiply with
            # probability of a connection
            cost_probabilities *= probability_connection / sum(cost_probabilities)
            probabilities = [1000 - probability_connection] + cost_probabilities       
        
        # generate the cost of all the connections
        node_costs = random.choices([np.nan] + costs, probabilities, k = amount_of_costs)
        
        lower_triangular_index = np.tril_indices(amount_of_nodes, k=-1)
        
        # initialize cost matrix and fill lower triangular with costs
        cost_matrix = np.zeros((amount_of_nodes, amount_of_nodes))
        cost_matrix[np.diag_indices(amount_of_nodes)] = np.nan
        cost_matrix[lower_triangular_index] = node_costs
        
        # mirror the cost matrix
        cost_matrix = cost_matrix + cost_matrix.T
        
        if secure_path_to_goal:
            # add a path to the goal by generating a sequence of at least 5 nodes
            goal_path = random.sample(range(1, amount_of_nodes - 1), 
                                      random.randint(3, amount_of_nodes))        
            goal_path = [0] + goal_path + [amount_of_nodes - 1]
            
            # generate costs for each step of the goal path
            costs_path = random.choices(costs, k = len(goal_path) - 1)
            
            # fill cost matrix with the costs of the goal path
            for i in range(len(goal_path)-1):
                cost_matrix[goal_path[i], goal_path[i + 1]] = costs_path[i]
                cost_matrix[goal_path[i + 1], goal_path[i]] = costs_path[i]
                   
        self.cost_matrix = cost_matrix
        
    def get_cost(self, node0, node1):
        return self.cost_matrix[node0, node1]
    
    def return_connections(self, node0):
        return [node1 for node1 in range(self.n) if self.get_cost(node0, node1) > 0]
        
