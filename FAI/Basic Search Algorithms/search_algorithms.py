# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 14:38:23 2020

@author: didie
"""
import sys

def detect_loop(path):
    # check if path only contains unique values by comparing the length of the
    # path with the path of the unique values of the path
    return len(path) > len(set(path))

def check_max_size_queue(max_size_queue, queue):
    
    queue_size = sys.getsizeof(queue)
    
    # edit max size of the queue if the size of the queue increased
    if queue_size > max_size_queue: 
       max_size_queue = queue_size 
       
    return max_size_queue
    

def depth_first(goal, network):
    '''
    
    A basic search algorithm, where the queue starts with the start node as the
    only path in the queue. Next for each itereation the first path in removed 
    and all of the children of this path are created. Further, all the new paths
    that contain loops are removed. Then the new paths are added to the front of 
    the queue. The network stop as soon as there is a connection to the goal node.
    The function returns the path to the goal and largest size the queue was 
    during the iterations.

    '''
    
    # initialize the queue and the max size of the queue
    queue = [[0]]
    max_size_queue = sys.getsizeof(queue)

    # loop until the queue is empty
    while queue:
        front = queue[0]
        
        # remove the path in the front of the queue
        queue.pop(0)
        
        # create list with children of the path that was in front of the queue
        new_paths = [front + [node] for node in network.return_connections(front[-1])]
        
        
        # remove new_paths with loops
        new_paths = [path for path in new_paths if not detect_loop(path)]
        
        # check if new paths reach the goal 
        for path in new_paths: 
            if path[-1] == goal: return path, max_size_queue
        
        # add new paths to the front of the queue
        queue = new_paths + queue
        max_size_queue = check_max_size_queue(max_size_queue, queue)
    
    return [], max_size_queue

def breadth_first(goal, network):
    '''
    
    A basic search algorithm, where the queue starts with the start node as the
    only path in the queue. Next for each itereation the first path in removed 
    and all of the children of this path are created. Further, all the new paths
    that contain loops are removed. Then the new paths are added to the back of 
    the queue. The network stop as soon as there is a connection to the goal node.
    The function returns the path to the goal and largest size the queue was 
    during the iterations.

    '''
    
    # initialize the queue and the max size of the queue
    queue = [[0]]
    max_size_queue = 1

    # loop until the queue is empty
    while queue:
        front = queue[0]
        
        # remove the path in the front of the queue
        queue.pop(0)
        
        # create list with children of the path that was in front of the queue
        new_paths = [front + [node] for node in network.return_connections(front[-1])]
        
        
        # remove new_paths with loops
        new_paths = [path for path in new_paths if not detect_loop(path)]
        
        # check if new paths reach the goal 
        for path in new_paths: 
            if path[-1] == goal: return path, max_size_queue
        
        # add new paths to the back of the queue
        queue = queue + new_paths
        max_size_queue = check_max_size_queue(max_size_queue, queue) 
    
    return [], max_size_queue

def iterative_deepening(goal, network, depth = 3):
    
    '''
    
    Restrict a depth-first search to a fixed depth and if no path is found,
    increase the depth and restart the search.

    '''
    # initialize largest size of the queue
    max_size_queue = 1
    
    # loop until the depth is equal the maximum size of a path
    while depth < goal:
        
        # initialize queue with only the start node
        queue = [[0]]
        
        # loop until the queue is empty
        while queue:
            front = queue[0]
            
            # remove first path in queue
            queue.pop(0)
            
            # create list with children of the path that was in front of the queue 
            new_paths = [front + [node] for node in network.return_connections(front[-1])]
            
            # check if new_paths reach the goal 
            for path in new_paths: 
                if path[-1] == goal: return path, max_size_queue
            
            # only add new paths to the queue if they are shorter than given depth
            if len(front) < depth:
                
                # remove paths with loops
                new_paths = [path for path in new_paths if not detect_loop(path)]
                
                # add new paths to the front of the queue
                queue = new_paths + queue
                max_size_queue = check_max_size_queue(max_size_queue, queue)
                   
        # increase depth if no solution was found       
        depth += 1
    
    return [], max_size_queue

