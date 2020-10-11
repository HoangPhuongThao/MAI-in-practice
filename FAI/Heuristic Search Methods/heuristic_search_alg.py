import sys
sys.path.insert(1, '/Users/Hiro_hankamura/Desktop/HomeProjects/MAI-in-practice/FAI/Basic Search Algorithms')
from search_algorithms import detect_loop


def sortChildrenByHeuristicVal(children, heuristicValueList):
    # sort children in an ascending order by their heuristic value
    childrenHeuristicValues = []
    for node in children:
        childrenHeuristicValues.append(heuristicValueList[node])
    sortedIndices = sorted(range(len(childrenHeuristicValues)), key=lambda k: childrenHeuristicValues[k])

    return sortedIndices


def hillClimbing1(goal, network, heuristicValueList):
    '''
    This algorithm performs the same way as depth-first algorithm BUT instead of left-to-right selection it first
    selects the child with the best (the smallest) heuristic value.
    :param heuristicValueList: holds values prescribed to each node by a specific heuristic function
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
        sortedIndices = sortChildrenByHeuristicVal(children, heuristicValueList)

        new_paths = [front + [children[index]] for index in sortedIndices]

        # remove new_paths with loops
        new_paths = [path for path in new_paths if not detect_loop(path)]

        # check if new paths reach the goal
        for path in new_paths:
            if path[-1] == goal: return path, max_size_queue

        # add new paths to the front of the queue
        queue = new_paths + queue
        max_size_queue = max([max_size_queue, len(queue)])

    return [], max_size_queue


def beamSearch(goal, network, heuristicValueList, width=2):
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
        sortedIndices = sortChildrenByHeuristicVal(children, heuristicValueList)

        # add only width best paths to the queue
        queue = [new_paths[sortedIndices[i]] for i in range(width)]

        # check that the max_size_queue should be constant = width
        max_size_queue = max([max_size_queue, len(queue)])

        # check if new paths reach the goal
        for path in new_paths:
            if path[-1] == goal: return path, max_size_queue

    return [], max_size_queue

