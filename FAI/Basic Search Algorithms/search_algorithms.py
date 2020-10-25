# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 14:38:23 2020

@author: didie & thao
"""
import sys, random


def detect_loop(path):
    # check if path only contains unique values by comparing the length of the
    # path with the path of the unique values of the path
    return len(path) > len(set(path))


def check_max_size_queue(max_size_queue, queue):
    # update memory
    queue_size = sys.getsizeof(queue)
    
    # edit max size of the queue if the size of the queue increased
    if queue_size > max_size_queue: 
       max_size_queue = queue_size 
       
    return max_size_queue
    

def depth_first(goal, network):
    '''
    
    A basic search algorithm, where the queue starts with the start node as the
    only path in the queue. Next for each iteration the first path is removed
    and all of the children of this path are created. Further, all the new paths
    that contain loops are removed. Then the new paths are added to the front of 
    the queue. The algorithm stops as soon as there is a connection to the goal node.
    The function returns the path to the goal and the largest size the queue was
    during the iterations (i.e. the memory).

    '''
    
    # initialize the queue and the max size of the queue
    queue = [[0]]
    max_size_queue = sys.getsizeof(queue)

    # loop until the queue is empty
    while queue:
        
        # remove the path in the front of the queue
        front = queue.pop(0)
        
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
        
        # remove the path in the front of the queue
        front = queue.pop(0)
        
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

def bi_directional(goal, network):
    
    def return_intersection(list1, list2):
        '''
        
        calculate the unique items in both lists. Then calculate the complement 
        by first substracting the first set of unique values of the other. This 
        will return the values in list1 that are not present in list2. If list1
        and list2 contain any intersecting values than the complement will 
        have less values than list1. If you subtract the complement from list 1
        you obtain the values that were removed from list1 while calculating
        the complement, thus the intersecting values.
        '''
        unique_list1 = set(list1)
        complement = (unique_list1 - set(list2))
        return list(unique_list1 - complement)

    # initialize the queue and the max size of the queue
    queue1 = [[0]]
    queue2 = [[goal]]
    max_size_queue = 1

    # loop until the queue is empty
    while queue1 and queue2:
        
        # remove the path in the front of the queue
        front1 = queue1.pop(0)
        front2 = queue2.pop(0)
        
        # create list with children of the path that was in front of the queue
        new_paths1 = [front1 + [node] for node in network.return_connections(front1[-1])]
        new_paths2 = [front2 + [node] for node in network.return_connections(front2[-1])]
        
        # remove new_paths with loops
        new_paths1 = [path for path in new_paths1 if not detect_loop(path)]
        new_paths2 = [path for path in new_paths2 if not detect_loop(path)]
        
        # add new paths to the back of the queue
        queue1 += new_paths1
        queue2 += new_paths2
        
        # concatenate all paths of the queue
        nodes_queue1 = []
        nodes_queue2 = []
        for path in queue1: nodes_queue1 += path
        for path in queue2: nodes_queue2 += path
        
        # calculate if there are any intersecting nodes between the queues
        intersections = return_intersection(nodes_queue1, nodes_queue2)
        
        # if there exist an intersecting value
        if intersections:
            # select the first intersecting node
            intersection = intersections[0]
            
            # look for a path containing the intersection and cut off the nodes
            # after the intersecting node
            for path1 in queue1:
                if intersection in path1: 
                    path1 = path1[:path1.index(intersection)]
                    break
                
            for path2 in queue2:
                if intersection in path2: 
                    path2 = path2[:(path2.index(intersection)+1)]
                    break
            # join the two lists at the intersection by reversing the list that
            # started at the goal node to obtain goal path
            return path1 + path2[::-1], max_size_queue
        
        queue_size = sys.getsizeof(queue1) + sys.getsizeof(queue2)
        
        # edit max size of the queue if the size of the queue increased
        if queue_size > max_size_queue: 
           max_size_queue = queue_size 
    
    return [], max_size_queue

def non_deterministic(goal, network):
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
        
        # remove the path in the front of the queue
        front = queue.pop(0)
        
        # create list with children of the path that was in front of the queue
        new_paths = [front + [node] for node in network.return_connections(front[-1])]
        
        
        # remove new_paths with loops
        new_paths = [path for path in new_paths if not detect_loop(path)]
        
        # check if new paths reach the goal 
        for path in new_paths: 
            if path[-1] == goal: return path, max_size_queue
        
        # add new paths at random places in the queue
        for path in new_paths:
            # generate a random index to add the path
            insert_index = random.randint(0, len(queue))
            
            # add path at random place
            queue = queue[:insert_index] + [path] + queue[insert_index:]
            
        max_size_queue = check_max_size_queue(max_size_queue, queue) 
    
    return [], max_size_queue

