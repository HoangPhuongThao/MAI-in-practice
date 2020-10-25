# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 18:12:41 2020

@author: didie
"""
import numpy as np
import random

class index_heuristic_network():
    '''
    '''
    def __init__(self,N, branching_factor, connection_ratio = 2,  seed = 0):

        
        if branching_factor >N:
            print("Branching factor cannot be more than number of nodes!")
            ValueError
        
        self.N = N
        self.connection_ratio = connection_ratio
        
        # set seed so the results are consistent
        np.random.seed(seed)
        random.seed(seed)
        
        # initiate the list of IndexDifferences between each node
        IndexDifferences = []
        for i in range(N - 1):
            IndexDifferences += list(range(1,N - i))
        
        alpha = np.log(connection_ratio) / (N - 2)
        probabilities = np.exp( - np.array(IndexDifferences) * alpha)
        n_connections =  probabilities.shape[0]
        
        TotalConnections = branching_factor * N / 2
        beta =  TotalConnections / probabilities.sum() 
        probabilities = probabilities * beta
        
        # tell the user if some probabilities are larger than zero
        if sum(probabilities > 1) > 0:
            print("connection_ratio too big or too small,\n thus some probabilieties are larger than zero")
        uniform_samples = np.random.rand(n_connections)

        connections = uniform_samples < probabilities
        
        upper_triangular_index = np.triu_indices(N, k = 1)
        
        # initialize cost matrix and fill lower triangular with costs
        cost_matrix = np.zeros((N, N))
        cost_matrix[upper_triangular_index] = connections
        
        # mirror the cost matrix
        cost_matrix = cost_matrix + cost_matrix.T
      
        # add a path to the goal by generating a sequence of at least 3 nodes (start -> A -> goal)
        # first parameter = nodes of the subpath between start and goal node
        # second parameter = the length of the subpath between start and goal node
        goal_path = random.sample(range(1, N - 1), random.randint(1, N - 2))
        goal_path = [0] + goal_path + [N - 1]
        
        # put the start of every connection is first part of tuple
        # put the end of every connection in second tuple        
        indexes = (goal_path[:-1], goal_path[1:])
        
        # use to tuple to find the cells where a connection needs to be added
        cost_matrix[indexes] = 1
        
        # reverse the indexes, added connection to the inverse cells to obtain a symmetric matrix
        cost_matrix[indexes[::-1]] = 1
            
        cost_matrix[cost_matrix == 0] = np.nan
                   
        self.cost_matrix = cost_matrix
    def check_connection(self, node0, node1):
        return self.cost_matrix[node0, node1] == 1
            
    def return_connections(self, node0):
        return [node1 for node1 in range(self.N) if self.check_connection(node0, node1)]
    
    def get_heuristic(self, node):
        return self.N + (1 - self.connection_ratio) * node
        
        