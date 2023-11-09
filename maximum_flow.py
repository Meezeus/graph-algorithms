from util import prettify_edge_dict, get_path_edges, calculate_path_capacity, calculate_flow_value

def construct_residual_graph(edges, capacities, flow):
    """
    Constructs a residual graph.

    Parameters
    ----------
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    capacities : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - in the original graph, and values are the original capacities of
        the edges.
    flow : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - in the original graph, and values are the flow along the edges. 

    Returns
    -------
    residual_edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the
        residual graph.
    residual_capacities : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - in the residual graph and values are the residual capacities of the
        edges.       
    """
    residual_capacities = {}
    for (u, v) in edges:
        residual_capacities[(u, v)] = capacities[(u, v)] - flow[(u, v)]
        residual_capacities[(v, u)] = flow[(u, v)]
    return (list(residual_capacities.keys()), residual_capacities)

def find_augmenting_path_bfs(edges, residual_capacities, source, sink):
    """
    Attempts to find an augmenting path in a residual graph, by performing BFS.

    Parameters
    ----------
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    residual_capacities : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are residual capacities of the edges.
    source : str
        The source node.
    sink : str
        The sink node.

    Returns
    ------- 
    list of str or None
        A list of nodes on the augmenting path, or None if no path was found.
    """
    closed_list_nodes = []    # Keeps track of which nodes have been discovered already by some path.
    open_list_paths = []    # Keeps track of the different active paths.

    open_list_paths.append([source])
    closed_list_nodes.append(source)

    while open_list_paths:
        current_path = open_list_paths.pop(0)
        current_node = current_path[-1]
        
        if current_node == sink:
            return current_path
        else:
            for new_node in [v for (u, v) in edges if (u == current_node and
                                                        residual_capacities[(u, v)] > 0 and
                                                        v not in closed_list_nodes)]:
                new_path = current_path[:]
                new_path.append(new_node)
                open_list_paths.append(new_path)
                closed_list_nodes.append(new_node)

def find_augmenting_path_dfs(edges, residual_capacities, source, sink):
    """
    Attempts to find an augmenting path in a residual graph, by performing DFS.

    Parameters
    ----------
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    residual_capacities : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are residual capacities of the edges.
    source : str
        The source node.
    sink : str
        The sink node.

    Returns
    ------- 
    list of str or None
        A list of nodes on the augmenting path, or None if no path was found.
    """
    closed_list_nodes = []  # Keeps track of nodes that are dead-ends.
    open_list_nodes = []    # Keeps track of the nodes on the current path.

    open_list_nodes.append(source)

    while open_list_nodes:
        current_node = open_list_nodes[-1]
        
        if current_node == sink:
            return open_list_nodes
        else:
            new_nodes = [v for (u, v) in edges if (u == current_node and
                                                    residual_capacities[(u, v)] > 0 and
                                                    v not in open_list_nodes and
                                                    v not in closed_list_nodes)]
            if new_nodes:
                open_list_nodes.append(new_nodes[0])
            else:
                open_list_nodes.pop()
                closed_list_nodes.append(current_node)

def find_augmenting_path_max(edges, residual_capacities, source, sink):
    """
    Attempts to find an augmenting path with the largest path capacity in a
    residual graph.

    Parameters
    ----------
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    residual_capacities : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are residual capacities of the edges.
    source : str
        The source node.
    sink : str
        The sink node.

    Returns
    ------- 
    list of str or None
        A list of nodes on the augmenting path, or None if no path was found.
    """
    all_paths = []      # All paths from the source to the sink.
    open_list_paths = []    # Keeps track of the different active paths.

    open_list_paths.append([source])

    while open_list_paths:
        current_path = open_list_paths.pop(0)
        current_node = current_path[-1]
        
        if current_node == sink:
            all_paths.append(current_path[:])
        else:
            for new_node in [v for (u, v) in edges if (u == current_node and
                                                        residual_capacities[(u, v)] > 0 and
                                                        v not in current_path)]:
                new_path = current_path[:]
                new_path.append(new_node)
                open_list_paths.append(new_path)
    
    max_path_capacity = 0
    max_path = None
    for path in all_paths:
        path_capacity = calculate_path_capacity(residual_capacities, get_path_edges(path))
        if path_capacity > max_path_capacity:
            max_path_capacity = path_capacity
            max_path = path

    return max_path

def find_augmenting_path_min(edges, residual_capacities, source, sink):
    """
    Attempts to find an augmenting path with the smallest path capacity in a
    residual graph.

    Parameters
    ----------
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    residual_capacities : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are residual capacities of the edges.
    source : str
        The source node.
    sink : str
        The sink node.

    Returns
    ------- 
    list of str or None
        A list of nodes on the augmenting path, or None if no path was found.
    """
    all_paths = []      # All paths from the source to the sink.
    open_list_paths = []    # Keeps track of the different active paths.

    open_list_paths.append([source])

    while open_list_paths:
        current_path = open_list_paths.pop(0)
        current_node = current_path[-1]
        
        if current_node == sink:
            all_paths.append(current_path[:])
        else:
            for new_node in [v for (u, v) in edges if (u == current_node and
                                                        residual_capacities[(u, v)] > 0 and
                                                        v not in current_path)]:
                new_path = current_path[:]
                new_path.append(new_node)
                open_list_paths.append(new_path)
    
    min_path_capacity = float("inf")
    min_path = None
    for path in all_paths:
        path_capacity = calculate_path_capacity(residual_capacities, get_path_edges(path))
        if path_capacity < min_path_capacity:
            min_path_capacity = path_capacity
            min_path = path

    return min_path

def ford_fulkerson(edges, capacities, source, sink, search_method, flow = None, debug = False):
    """
    Finds the maximum flow in a flow graph using the Ford-Fulkerson method.

    Parameters
    ----------
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    capacities : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are capacities of the edges.
    source : str
        The source node.
    sink : str
        The sink node.
    search_method : method of (list of tuple of (str, str), dict of {tuple of
    (str, str) : int}, str, str) --> list of str
        A search method that - given the edges of a graph, their capacities, the
        source node and the sink node - finds an augmenting path in a residual
        graph and returns the list of nodes on the path.
    flow : dict of {tuple of (str, str) : int}, default None, meaning no flow
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the flow along the edges. This is the initial flow.
    debug : bool, default False
        Whether to print debug information or not.
    
    Returns
    -------
    flow : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the flow along the edges. This is the maximum flow
        that could be found.
    flow_value : int
        The total value of the flow that was found.
    """
    # Initialise flow if none given.
    if not flow:
        flow = {}
        for edge in edges:
            flow[edge] = 0

    # Build residual graph and find augmenting path.
    (residual_edges, residual_capacities) = construct_residual_graph(edges, capacities, flow)
    augmenting_path_nodes = search_method(residual_edges, residual_capacities, source, sink)

    # Keep augmenting the flow until an augmenting path cannot be found.
    counter = 0
    while (augmenting_path_nodes):
        counter += 1

        # Get the augmenting path edges and the augmenting path capacity.
        augmenting_path_edges = get_path_edges(augmenting_path_nodes)
        augmenting_path_capacity = calculate_path_capacity(residual_capacities, augmenting_path_edges)

        # Augment the current flow with the augmenting path.
        for (u, v) in edges:
            if (u, v) in augmenting_path_edges:
                flow[(u, v)] += augmenting_path_capacity
            if (v, u) in augmenting_path_edges:
                flow[(u, v)] -= augmenting_path_capacity
        if debug:
            pretty_print_ford_fulkerson("Ford-Fulkerson (" + search_method.__name__ + "), iteration " + str(counter),
                                        flow,
                                        calculate_flow_value(flow, source),
                                        augmenting_path_nodes,
                                        augmenting_path_capacity)
        
        # Build residual graph and find augmenting path.
        (residual_edges, residual_capacities) = construct_residual_graph(edges, capacities, flow)
        augmenting_path_nodes = search_method(residual_edges, residual_capacities, source, sink)

    # Once an augmenting path cannot be found, return the flow.
    return (flow, calculate_flow_value(flow, source))

def pretty_print_ford_fulkerson(title, flow, flow_value, augmenting_path_nodes = [], augmenting_path_capacity = 0):
    """
    Prints the results of an iteration of the Ford-Fulkerson method in a
    user-friendly manner.

    Parameters
    ----------
    title : str
        The title of the problem to be printed.
    flow : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the flow along the edges. This is the maximum flow
        that was found this iteration.
    flow_value : int
        The total value of the flow that was found this iteration (after
        augmentation).
    augmenting_path_nodes : list of str, default [] meaning no augmenting path
    found
        A list of nodes that lie on the augmenting path that was found this
        iteration.
    augmenting_path_capacity : int, default 0 meaning no augmenting path found
        The capacity of the augmenting path that was found this iteration.
    """
    print ("\n" + title)
    print ("----------------------------------------")
    print ("The augmenting path, with a capacity of " + str(augmenting_path_capacity) + ", is " + str(augmenting_path_nodes))
    print ("The current flow, with a value of " + str(flow_value) + ", is:\n" + prettify_edge_dict(flow))
    print("")

if __name__ == "__main__":
    #''' Week 4 LGT Question 1. Max flow = 4.
    capacities = {
        ("s", "c1"): 1, ("s", "c2"): 1, ("s", "c3"): 1, ("s", "c4"): 1,
        ("c1", "r1"): 1, ("c1", "r2"): 1,
        ("c2", "r2"): 1, ("c2", "r3"): 1, ("c2", "r4"): 1,
        ("c3", "r4"): 1, ("c3", "r5"): 1,
        ("c4", "r4"): 1, ("c4", "r5"): 1, ("c4", "r6"): 1, ("c4", "r7"): 1,
        ("r1", "p1"): 1,
        ("r2", "p1"): 1,
        ("r3", "p2"): 1,
        ("r4", "p2"): 1,
        ("r5", "p3"): 1,
        ("r6", "p3"): 1,
        ("r7", "p3"): 1,
        ("p1", "t"): 1,
        ("p2", "t"): 2,
        ("p3", "t"): 2,
    }
    edges = list(capacities.keys())
    flow = {
        ("s", "c1"): 0, ("s", "c2"): 1, ("s", "c3"): 1, ("s", "c4"): 1,
        ("c1", "r1"): 0, ("c1", "r2"): 0,
        ("c2", "r2"): 1, ("c2", "r3"): 0, ("c2", "r4"): 0,
        ("c3", "r4"): 0, ("c3", "r5"): 1,
        ("c4", "r4"): 0, ("c4", "r5"): 0, ("c4", "r6"): 1, ("c4", "r7"): 0,
        ("r1", "p1"): 0,
        ("r2", "p1"): 1,
        ("r3", "p2"): 0,
        ("r4", "p2"): 0,
        ("r5", "p3"): 1,
        ("r6", "p3"): 1,
        ("r7", "p3"): 0,
        ("p1", "t"): 1,
        ("p2", "t"): 0,
        ("p3", "t"): 2,
    }

    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs, flow=flow.copy())[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_dfs, flow=flow.copy())[1]
    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs, flow=flow.copy())[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_max, flow=flow.copy())[1]
    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs, flow=flow.copy())[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_min, flow=flow.copy())[1]

    pretty_print_ford_fulkerson("Ford-Fulkerson (BFS)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs, flow=flow.copy()))
    pretty_print_ford_fulkerson("Ford-Fulkerson (DFS)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_dfs, flow=flow.copy()))
    pretty_print_ford_fulkerson("Ford-Fulkerson (MAX)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_max, flow=flow.copy()))
    pretty_print_ford_fulkerson("Ford-Fulkerson (MIN)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_min, flow=flow.copy()))
    #'''

    #''' Week 4 SGT Question 1, Week 5 LGT Question 1. Max flow = 10.
    capacities = {
        ("s", "a"): 8, ("s", "b"): 3,
        ("a", "p"): 7,
        ("b", "a"): 2, ("b", "c"): 2, ("b", "d"): 4,
        ("c", "d"): 1, ("c", "h"): 3,
        ("d", "t"): 5,
        ("h", "d"): 1, ("h", "t"): 3,
        ("p", "d"): 5, ("p", "t"): 3
    }
    edges = list(capacities.keys())

    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_dfs)[1]
    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_max)[1]
    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_min)[1]

    pretty_print_ford_fulkerson("Ford-Fulkerson (BFS)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs))
    pretty_print_ford_fulkerson("Ford-Fulkerson (DFS)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_dfs))
    pretty_print_ford_fulkerson("Ford-Fulkerson (MAX)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_max))
    pretty_print_ford_fulkerson("Ford-Fulkerson (MIN)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_min))
    #'''

    #''' Week 4 Quiz Question 1. Max flow = 7.
    capacities = {
        ("s", "a"): 5, ("s", "c"): 4,
        ("a", "b"): 4, ("a", "u"): 3,
        ("c", "u"): 1, ("c", "b"): 2,
        ("b", "t"): 3,
        ("u", "t"): 7
    }
    edges = list(capacities.keys())

    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_dfs)[1]
    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_max)[1]
    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_min)[1]

    pretty_print_ford_fulkerson("Ford-Fulkerson (BFS)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs))
    pretty_print_ford_fulkerson("Ford-Fulkerson (DFS)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_dfs))
    pretty_print_ford_fulkerson("Ford-Fulkerson (MAX)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_max))
    pretty_print_ford_fulkerson("Ford-Fulkerson (MIN)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_min))
    #'''

    #''' Week 5 SGT Question 1. Max flow = 6.
    capacities = {
        ("s", "t1"): 1, ("s", "t2"): 1, ("s", "t3"): 1, ("s", "t4"): 1, ("s", "t5"): 1, ("s", "t6"): 1,
        ("t1", "e1"): 1, ("t1", "e2"): 1, ("t1", "e3"): 1, ("t1", "e4"): 1,
        ("t2", "e2"): 1, ("t2", "e3"): 1, ("t2", "e4"): 1,
        ("t3", "e2"): 1, ("t3", "e5"): 1,
        ("t4", "e1"): 1, ("t4", "e5"): 1, ("t4", "e6"): 1,
        ("t5", "e2"): 1, ("t5", "e5"): 1,
        ("t6", "e5"): 1, ("t6", "e6"): 1,
        ("e1", "t"): 1,
        ("e2", "t"): 1,
        ("e3", "t"): 1,
        ("e4", "t"): 1,
        ("e5", "t"): 1,
        ("e6", "t"): 1,
    }
    edges = list(capacities.keys())

    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_dfs)[1]
    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_max)[1]
    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_min)[1]

    pretty_print_ford_fulkerson("Ford-Fulkerson (BFS)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs))
    pretty_print_ford_fulkerson("Ford-Fulkerson (DFS)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_dfs))
    pretty_print_ford_fulkerson("Ford-Fulkerson (MAX)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_max))
    pretty_print_ford_fulkerson("Ford-Fulkerson (MIN)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_min))
    #'''

    #''' Past Paper 2018 Question 11
    capacities = {
        ("s", "a"): 3, ("s", "b"): 3,
        ("a", "c"): 2, ("a", "d"): 2,
        ("b", "d"): 1, ("b", "e"): 2,
        ("c", "f"): 1,
        ("f", "d"): 2, ("f", "g"): 1,
        ("d", "g"): 2,
        ("e", "d"): 2, ("e","h"): 1,
        ("h", "g"): 2, ("h", "t"): 4,
        ("g", "t"): 2
    }
    edges = list(capacities.keys())

    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_dfs)[1]
    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_max)[1]
    assert ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs)[1] == ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_min)[1]

    pretty_print_ford_fulkerson("Ford-Fulkerson (BFS)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs))
    pretty_print_ford_fulkerson("Ford-Fulkerson (DFS)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_dfs))
    pretty_print_ford_fulkerson("Ford-Fulkerson (MAX)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_max))
    pretty_print_ford_fulkerson("Ford-Fulkerson (MIN)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_min))

    #'''

    #''' Test
    capacities = {
        ("s", "a"): 5, ("s", "e"): 10,
        ("a", "b"): 3, ("a", "c"): 4, ("a", "e"): 3, ("a", "h"): 3,
        ("b", "t"): 6,
        ("c", "b"): 4, ("c", "t"): 4,
        ("e", "c"): 9,
        ("h", "b"): 2, ("h", "k"): 6,
        ("k", "b"): 3, ("k", "t"): 5
    }
    edges = list(capacities.keys())

    pretty_print_ford_fulkerson("Ford-Fulkerson (BFS)", *ford_fulkerson(edges, capacities, "s", "t", find_augmenting_path_bfs, debug=True))    
    #'''
