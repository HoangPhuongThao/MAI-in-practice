# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 11:32:52 2020

@author: didie
"""
import random
import numpy as np
class network_of_nodes():
    
    '''
    Design a network of nodes by creating a matrix with the distance from
    each node to another.
    '''
    
    def __init__(self, amount_of_nodes, distances = np.arange(5), 
                 probabilities = [5, 2, 1, 1, 1]):
        '''
        In the distance matrix the start nodes are on the rows and the end
        nodes are on the columns. The distance from a node to itself must be
        zero, therefore, the diagonal must be zero. The matrix must also be
        mirrored in the diagonal so that the distance from node A to node B
        is the same as from node B to node A.
        '''

        self.n = amount_of_nodes
        
        # amount of generated distances should be equal to the lower 
        # triangular of the distance matrix
        amount_of_distances = int((amount_of_nodes - 1) * amount_of_nodes / 2)
        distances = random.choices(distances, probabilities, k = amount_of_distances)
        
        lower_triangular_index = np.tril_indices(amount_of_nodes, k=-1) 
        
        distance_matrix = np.zeros((amount_of_nodes, amount_of_nodes))
        distance_matrix[lower_triangular_index] = distances
        # mirror the distance matrix
        distance_matrix = distance_matrix + distance_matrix.T
        self.distance_matrix = distance_matrix
        
    def get_distance(self, node0, node1):
        return self.distance_matrix[node0, node1]
    
    def return_connections(self, node0):
        return [node1 for node1 in range(self.n) if self.get_distance(node0, node1) > 0]
        
