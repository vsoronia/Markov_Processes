import numpy as np
from collections import deque


def isCyclicUtil(v, visited, recStack, graph, cycle):
    visited[v] = True
    recStack[v] = True

    for neighbour in reversed(graph[v]):
        if visited[neighbour] == False:
            cycle.append(neighbour)
            if isCyclicUtil(neighbour, visited, recStack, graph, cycle) == True:
                return True

            cycle.pop()

        elif recStack[neighbour] == True:
            cycle.append(neighbour)
            return True

    recStack[v] = False

    if not graph[v]:
        # Empty node, append it to the cycle
        cycle.append(v)
        return True

    return False


def isCyclic(graph):
    visited = {node: False for node in graph}
    recStack = {node: False for node in graph}
    cycles = []

    for node in graph:
        nodes = deque(graph.keys())
        for next_node in nodes:
            graph[next_node] = deque(graph[next_node])
            graph[next_node].rotate(-1)

            if visited[node] == False:
                cycle = [next_node]
                if isCyclicUtil(next_node, visited, recStack, graph, cycle):
                    cycles.append(cycle)

            graph[next_node] = list(graph[next_node])
            visited = {node: False for node in graph}
            recStack = {node: False for node in graph}

    return cycles


def eliminateDuplicateCycles(cycles):
    # Find cycles that contain the same value in the last two positions
    duplicate_cycles = []
    for cycle in cycles:
        if cycle[-1] == cycle[-2]:
            duplicate_cycles.append(cycle)

    # Find elements in duplicate cycles
    elements_to_eliminate = set()
    for cycle in duplicate_cycles:
        elements_to_eliminate.update(cycle)

    # Eliminate elements from cycles
    updated_cycles = []
    for cycle in cycles:
        if not any(element in elements_to_eliminate for element in cycle):
            updated_cycles.append(cycle)

    return updated_cycles


def eliminateCyclesByUnreachableStart(cycles, graph):
    # Find states from which the starting state is unreachable
    states_to_eliminate = set()
    for cycle in cycles:
        start_state = cycle[0]
        end_state = cycle[-1]
        if not isReachable(graph, end_state, start_state):
            states_to_eliminate.add(start_state)

    # Eliminate cycles that start from unreachable states
    final_cycles = []
    for cycle in cycles:
        if cycle[0] not in states_to_eliminate:
            final_cycles.append(cycle)

    return final_cycles


def isReachable(graph, start_state, target_state):
    visited = set()
    stack = [start_state]

    while stack:
        current_state = stack.pop()
        visited.add(current_state)

        if current_state == target_state:
            return True

        for neighbour in graph[current_state]:
            if neighbour not in visited:
                stack.append(neighbour)

    return False


def findRecurrentClasses(cycles):
    recurrent_classes = []

    for cycle in cycles:
        found_class = False
        for recurrent_class in recurrent_classes:
            if recurrent_class.intersection(cycle):
                recurrent_class.update(cycle)
                found_class = True
                break

        if not found_class:
            recurrent_classes.append(set(cycle))

    return recurrent_classes


def create_nodes(matrix):
    num_states = matrix.shape[0]
    nodes = {}

    for i in range(num_states):
        state = str(i)
        connections = []
        for j in range(num_states):
            if matrix[i, j] > 0:
                connections.append(str(j))
        nodes[state] = connections

    return nodes


def checkMarkov(matrix):
    for i in range(0, len(matrix)):
        sm = 0
        for j in range(0, len(matrix[i])):
            sm = sm + matrix[i][j]
        if sm != 1:
            return False
    return True


M = np.array([[0,   0,  1/2, 1/4, 1/4,  0,   0],
              [0,   0,   0,   0,   0,  1,   0],
              [0,   0,   0,   0,   0,  1/3, 2/3],
              [0,   0,   0,   0,   0,  1/2, 1/2],
              [0,   0,   0,   0,   0,  3/4, 1/4],
              [0,   1,   0,   0,   0,   0,   0],
              [1/4, 3/4,  0,   0,   0,   0,   0]])


if checkMarkov(M):
    print("Is a transition matrix of a Markov Chain.")
    # Consider diagonal (=1) elements as recurrent states
    recurrent_states = [str(i) for i, value in enumerate(np.diagonal(M)) if value == 1]
    np.fill_diagonal(M, 0)

    graph = create_nodes(M)

    cycles = isCyclic(graph)
    updated_cycles = eliminateDuplicateCycles(cycles)
    updated_cycles = eliminateCyclesByUnreachableStart(updated_cycles, graph)
    recurrent_classes = findRecurrentClasses(updated_cycles)
    if recurrent_classes:
        print("Recurrent classes:")
    else:
        print("There are not recurrent classes")
    for i, recurrent_class in enumerate(recurrent_classes):
        print('Recurrent Class', i + 1, ':', sorted(recurrent_class))
        recurrent_states.extend(recurrent_class)

    transient_states = set(graph.keys()) - set(recurrent_states)
    print("\nStates:")
    print("Transient states:", sorted(transient_states))
    print("Recurrent states:", sorted(recurrent_states))

else:
    print("The matrix is not a valid Markov matrix.")