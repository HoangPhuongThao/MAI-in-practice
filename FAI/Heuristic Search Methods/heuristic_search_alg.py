from numpy import inf
import sys

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

def sortChildrenByHeuristicVal(network, children):
    # sort children in an ascending order by their heuristic value
    childrenHeuristicValues = [network.get_heuristic(child) for child in children]
    sortedIndices = sorted(range(len(childrenHeuristicValues)), key=lambda k: childrenHeuristicValues[k])

    return sortedIndices


def hillClimbing1(goal, network):
    '''
    This algorithm performs the same way as depth-first algorithm BUT instead of left-to-right selection it first
    selects the child with the best (the smallest) heuristic value.
    :return: the found path from start node to goal node and the max size memory we used
    '''

    # initialize the queue and the max size of the queue
    queue = [[0]]
    max_size_queue = 1

    # loop until the queue is empty
    while queue:

        # remove the path in the front of the queue
        front = queue.pop(0)

        # create list with SORTED children (ascending order by heuristic value) of the path that was in front of the queue
        children = network.return_connections(front[-1])
        sortedIndices = sortChildrenByHeuristicVal(network, children)

        new_paths = [front + [children[index]] for index in sortedIndices]

        # remove new_paths with loops
        new_paths = [path for path in new_paths if not detect_loop(path)]

        # check if new paths reach the goal
        for path in new_paths:
            if path[-1] == goal: return path, max_size_queue

        # add new paths to the front of the queue
        queue = new_paths + queue
        max_size_queue = check_max_size_queue(max_size_queue, queue)

    print("No path found")
    return [], max_size_queue


def beamSearch(goal, network, width=2):
    '''
    This algorithm performs a breadth-first search narrowed by a WIDTH parameter, i.e. we only keep the WIDTH best
    children (according to their heuristic values) at each level. We also optimize by ignoring leafs that are not the
    goal node.
    :param width: by default = 2
    '''

    # initialize the queue and the max size of the queue
    queue = [[0]]
    max_size_queue = 1

    # loop until the queue is empty
    while queue:
        children = []
        new_paths = []

        # removing all paths from the queue, creating new paths to all children
        while queue:
            # remove the path in the front of the queue
            front = queue.pop(0)

            # add new children of the path
            childrenOfPath = network.return_connections(front[-1])

            # remove a child if it's a leaf and not a goal node
            for node in childrenOfPath:
                if (network.return_connections(node) == []) and (node != goal):
                    childrenOfPath.remove(node)
                else:
                    # create new path
                    children.append(node)
                    new_paths.append(front + [node])

        # remove new_paths with loops
        pathsWithLoops = [path for path in new_paths if detect_loop(path)]
        for path in pathsWithLoops:
            del children[new_paths.index(path)]
            new_paths.remove(path)

        # sort children in an ascending order by their heuristic value (i.e. sorting new_paths according to heuristic)
        sortedIndices = sortChildrenByHeuristicVal(network, children)

        # add only width best paths to the queue
        queue = [new_paths[sortedIndices[i]] for i in range(min(width, len(new_paths)))]

        max_size_queue = check_max_size_queue(max_size_queue, queue)

        # check if new paths reach the goal
        for path in new_paths:
            if path[-1] == goal: return path, max_size_queue

    print("No path found")
    return [], max_size_queue

def HillClimbing2(goal, network):
    '''
     = Beam search algorithm with width=1
    '''
    
    # initialize the queue and the max size of the queue
    queue = [0]
    max_size_queue = 1

    # loop until the queue is empty
    while queue:        
        
        # create list with children of the path in the queue
        new_paths = [queue + [node] for node in network.return_connections(queue[-1])]        
        
        # remove new_paths with loops
        new_paths = [path for path in new_paths if not detect_loop(path)]
        
        if not new_paths: 
            print("No path found")
            return [], sys.getsizeof(queue)
        
        min_heuristic_value = inf
        
        # store the path with the lowest heuristic
        for path in new_paths:
            if network.get_heuristic(path[-1]) < min_heuristic_value:
                queue = path
                min_heuristic_value = network.get_heuristic(path[-1])        

        if queue[-1] == goal: return queue, sys.getsizeof(queue)
            
    return [], max_size_queue

def Greedy(goal, network):
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
        
        # calculate the heursitic of each path
        heuristic_values = [network.get_heuristic(path[-1]) for path in queue]
        
        # save a list with sorted heuristics of each path
        heuristic_values_sorted = heuristic_values.copy()
        heuristic_values_sorted.sort()
        
        # use index of sorted heuristics list to sort the queue
        queue = [queue[heuristic_values.index(heuristic)] for heuristic in heuristic_values_sorted]
                
        max_size_queue = check_max_size_queue(max_size_queue, queue)
    
    return [], max_size_queue
