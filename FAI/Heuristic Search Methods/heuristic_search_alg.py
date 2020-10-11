import sys
sys.path.insert(1, '/Users/Hiro_hankamura/Desktop/HomeProjects/MAI-in-practice/FAI/Basic Search Algorithms')
from search_algorithms import detect_loop, check_max_size_queue


def hillClimbing1(goal, network, heuristicValueList):
    '''
    This algorithm performs the same way as depth-first algorithm BUT instead of left-to-right selection it first
    selects the child with the best (the smallest) heuristic value.
    '''

    # initialize the queue and the max size of the queue
    queue = [[0]]
    max_size_queue = sys.getsizeof(queue)

    # loop until the queue is empty
    while queue:

        # remove the path in the front of the queue
        front = queue.pop(0)

        # create list with SORTED children (ascending order by heuristic value) of the path that was in front of the queue
        children = network.return_connections(front[-1])

        childrenHeuristicValues = []
        for node in children:
            childrenHeuristicValues.append(heuristicValueList[node])
        sortedIndices = sorted(range(len(childrenHeuristicValues)), key=lambda k: childrenHeuristicValues[k])

        new_paths = [front + [children[index]] for index in sortedIndices]

        # remove new_paths with loops
        new_paths = [path for path in new_paths if not detect_loop(path)]

        # check if new paths reach the goal
        for path in new_paths:
            if path[-1] == goal: return path, max_size_queue

        # add new paths to the front of the queue
        queue = new_paths + queue
        max_size_queue = check_max_size_queue(max_size_queue, queue)

    return [], max_size_queue
