# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 14:38:23 2020

@author: didie
"""
from network import network_of_nodes 
import time, sys


def detect_loop(path):
    return len(path) > len(set(path))

def depth_first(goal, network):
    
    queue = [[0]]
    max_size_queue = 1

    while queue:
        front = queue[0]
        queue.pop(0)
        new_paths = [front + [node] for node in network.return_connections(front[-1])]
        for path in new_paths: 
            if path[-1] == goal: return path, max_size_queue
        new_paths = [path for path in new_paths if not detect_loop(path)]
        queue = new_paths + queue
        queue_size = sys.getsizeof(queue)
        
        if queue_size > max_size_queue: 
           max_size_queue = queue_size 
    
    return [], max_size_queue

def breadth_first(goal, network):
    
    queue = [[0]]
    max_size_queue = 1
    while queue:
        front = queue[0]
        queue.pop(0)
        new_paths = [front + [node] for node in network.return_connections(front[-1])]
        for path in new_paths: 
            if path[-1] == goal: return path, max_size_queue
        new_paths = [path for path in new_paths if not detect_loop(path)]
        queue = queue + new_paths 
        queue_size = sys.getsizeof(queue)
        
        if queue_size > max_size_queue: 
           max_size_queue = queue_size 
    
    return [], max_size_queue

def non_determenistic(goal, network):
    
    queue = [[0]]
    max_size_queue = 1
    while queue:
        front = queue[0]
        queue.pop(0)
        new_paths = [front + [node] for node in network.return_connections(front[-1])]
        for path in new_paths: 
            if path[-1] == goal: return path, max_size_queue
        new_paths = [path for path in new_paths if not detect_loop(path)]
        queue = queue + new_paths 
        queue_size = sys.getsizeof(queue)
        
        if queue_size > max_size_queue: 
           max_size_queue = queue_size 
    
    return [], max_size_queue

def iterative_deepening(goal, network, depth = 3):
    
    max_size_queue = 1
    
    while depth < goal:
        queue = [[0]]
        while queue:
            front = queue[0]
            queue.pop(0)
            if len(front) > depth: 
                continue            
            new_paths = [front + [node] for node in network.return_connections(front[-1])]
            for path in new_paths: 
                if path[-1] == goal: return path, max_size_queue
            new_paths = [path for path in new_paths if not detect_loop(path)]
            queue = new_paths + queue
            queue_size = sys.getsizeof(queue)
            
            if queue_size > max_size_queue: 
               max_size_queue = queue_size 
               
        depth += 1
    
    return [], max_size_queue

def bi_directional(goal, network):
    
    queue1 = [[0]]
    queue2 = [[goal]]
    max_size_queue = 1
    while queue:
        front1 = queue1[0]
        front2 = queue2[0]
        
        queue1.pop(0)
        queue2.pop(0)
        
        new_paths1 = [front1 + [node] for node in network.return_connections(front1[-1])]
        new_paths2 = [front2 + [node] for node in network.return_connections(front2[-1])]
                    
        new_paths1 = [path for path in new_paths1 if not detect_loop(path)]
        new_paths2 = [path for path in new_paths2 if not detect_loop(path)]
        
        queue1 += new_paths1
        queue2 += new_paths2
        
        queue_size = sys.getsizeof(queue1) + sys.getsizeof(queue2)
        
        if queue_size > max_size_queue: 
           max_size_queue = queue_size 
    
    return [], max_size_queue
#%%
nodes = 1000
goal = nodes - 1 
network = network_of_nodes(nodes, probabilities = [1000, 1,1,1,1])
start = time.time()
print(depth_first(goal, network))
print(time.time() - start)
start = time.time()
print(breadth_first(goal, network))
print(time.time() - start)
start = time.time()
print(iterative_deepening(goal, network))
print(time.time() - start)