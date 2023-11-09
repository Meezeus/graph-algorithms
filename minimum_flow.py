from util import prettify_edge_dict, get_path_edges, calculate_path_capacity, calculate_flow_value
from maximum_flow import ford_fulkerson, find_augmenting_path_bfs, find_augmenting_path_dfs, find_augmenting_path_max, find_augmenting_path_min, pretty_print_ford_fulkerson

def construct_residual_graph_min_flow(edges, lower_bounds, upper_bounds, flow):
    """
    Constructs a residual graph.

    Parameters
    ----------
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the
        original graph.
    lower_bounds : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - in the original graph and values are the lower bounds on the flow
        along the edges.
    upper_bounds : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - in the original graph and values are the upper bounds on the flow
        along the edges.
    flow : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - in the original graph and values are the flow along the edges. 

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
        residual_capacities[(u, v)] = upper_bounds[(u, v)] - flow[(u, v)]
        residual_capacities[(v, u)] = flow[(u, v)] - lower_bounds[(u, v)]
    return (list(residual_capacities.keys()), residual_capacities)

def ford_fulkerson_min_flow(edges, lower_bounds, upper_bounds, source, sink, search_method, flow = None, debug = False):
    """
    A modified version of the Ford-Fulkerson method for use in minimum flow
    graphs. The only difference is the method used to construct the residual
    graph.

    Parameters
    ----------
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    lower_bounds : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the lower bounds on the flow along the edges.
    upper_bounds : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the upper bounds on the flow along the edges.
    source : str
        The source node.
    sink : str
        The sink node.
    search_method : (list of tuple of (str, str), dict of {tuple of (str, str) :
    int}, str, str) --> list of str
        A search method that, given the edges of a graph, their capacities, the
        source node and the sink node, finds an augmenting path in a residual
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
    (residual_edges, residual_capacities) = construct_residual_graph_min_flow(edges, lower_bounds, upper_bounds, flow)
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
            pretty_print_ford_fulkerson("Ford-Fulkerson Min Flow (" + search_method.__name__ + "), iteration " + str(counter),
                                        flow,
                                        calculate_flow_value(flow, source),
                                        augmenting_path_nodes,
                                        augmenting_path_capacity)
        
        # Build residual graph and find augmenting path.
        (residual_edges, residual_capacities) = construct_residual_graph_min_flow(edges, lower_bounds, upper_bounds, flow)
        augmenting_path_nodes = search_method(residual_edges, residual_capacities, source, sink)

    # Once an augmenting path cannot be found, return the flow.
    return (flow, calculate_flow_value(flow, source))

def minimum_flow(nodes, edges, lower_bounds, upper_bounds, source, sink, search_method, feasible_flow=None, debug=None):   
    """
    Attempts to find the minimum feasible flow in a flow graph.

    A feasible flow must satisfy three things: upper and lower bound constraints
    on edges, conservation of flow at nodes, and supply-demand of the nodes.

    For more information, see 25.1
    https://courses.engr.illinois.edu/cs498dl1/sp2015/notes/25-maxflowext.pdf

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the graph.
    edges : list of tuple of (str, str)
        A list of edges in the graph, represented as a pair of nodes (u, v).
    lower_bounds : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the lower bounds on the flow along the edges.
    upper_bounds : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the upper bounds on the flow along the edges.
    source : str
        The source node.
    sink : str
        The sink node.
    search_method : (list of tuple of (str, str), dict of {tuple of (str, str) :
    int}, str, str) --> list of str
        A search method that, given the edges of a graph, their capacities, the
        source node and the sink node, finds an augmenting path in a residual
        graph and returns the list of nodes on the path.
    feasible_flow : dict of {tuple of (str, str) : int}, default None, meaning
    no flow
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the flow along the edges. This is a feasible flow,
        but not necessarily the minimum feasible flow.
    debug : bool, default False
        Whether to print debug information or not.
    
    Returns
    -------
    min_flow : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the flow along the edges. This is the minimum
        feasible flow that could be found.
    min_flow_value : int
        The total value of the flow that was found.
    """
    # If a feasible flow was not given, it needs to be constructed. 
    if not feasible_flow:
        # Add a new source and a new sink.
        nodes_prime = nodes.copy()
        nodes_prime.append("s_prime")
        nodes_prime.append("t_prime")

        # Add new edges between s_prime and all nodes, between all nodes and t_prime, and between t and s.
        edges_prime = edges.copy()
        for node in nodes:
            edges_prime.append(("s_prime", node))
            edges_prime.append((node, "t_prime"))
        edges_prime.append((sink, source))

        # The capacities are as follows:
        # For edges (s_prime, node): sum of lower bounds of incoming edges
        # For edges (node, t_prime): sum of lower bounds of outgoing edges
        # For edges (node1, node2): upper bound of the edge minus lower bound of the edge
        # For edge (t, s): infinity
        capacities = {}
        for node in nodes:
            capacities[("s_prime", node)] = sum([lower_bounds[(u,v)] for (u,v) in edges if v == node])
            capacities[(node, "t_prime")] = sum([lower_bounds[(v,w)] for (v,w) in edges if v == node])
        for edge in edges:
            capacities[edge] = upper_bounds[edge] - lower_bounds[edge]
        capacities[(sink, source)] = float("inf")

        # Find the maximum flow from s_prime to t_prime.
        flow_prime = ford_fulkerson(edges_prime, capacities, "s_prime", "t_prime", search_method, debug=debug)[0]

        # Find the feasible flow by adding the lower bounds.
        feasible_flow = {}
        for edge in edges:
            feasible_flow[edge] = flow_prime[edge] + lower_bounds[edge] 

    # Send as much flow back from the sink to the source, while respecting edge lower bounds.
    (min_flow, min_flow_value) = ford_fulkerson_min_flow(edges, lower_bounds, upper_bounds, sink, source, search_method, flow=feasible_flow, debug=debug)

    # The min_flow_value is the outgoing flow from the sink. This will be
    # negative, so flip the sign to get the real minimum flow.
    return (min_flow, -min_flow_value)

def pretty_print_minimum_flow(title, flow, flow_value):
    """
    Prints the results of finding a minimum feasible flow in a user-friendly
    manner.

    Parameters
    ----------
    title : str
        The title of the problem to be printed.
    flow : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the flow along the edges. This is the minimum
        feasible flow that was found.
    flow_value : int
        The total value of the flow that was found.
    """
    print ("\n" + title)
    print ("----------------------------------------")
    print ("The minimum flow, with a value of " + str(flow_value) + ", is:\n" + prettify_edge_dict(flow))
    print("")

if __name__ == "__main__":    
    #''' Week 5 Slides 15-18. Min flow = 2.
    nodes = ["a", "b", "c", "d", "e", "f", "s", "g", "t"]
    lower_bounds = {
        ("a", "b"): 0, ("a", "d"): 2,
        ("b", "c"): 0, ("b", "d"): 5, ("b", "f"): 0,
        ("c", "f"): 0,
        ("d", "e"): 3, ("d", "s"): 0,
        ("e", "b"): 0, ("e", "f"): 5,
        ("f", "g"): 0, ("f", "t"): 0,
        ("s", "a"): 0, ("s", "g"): 0,
        ("g", "e"): 0, ("g", "t"): 0,
        ("t", "c"): 0
    }
    upper_bounds = {
        ("a", "b"): 5, ("a", "d"): 5,
        ("b", "c"): 3, ("b", "d"): 6, ("b", "f"): 4,
        ("c", "f"): 1,
        ("d", "e"): 4, ("d", "s"): 5,
        ("e", "b"): 2, ("e", "f"): 7,
        ("f", "g"): 8, ("f", "t"): 3,
        ("s", "a"): 8, ("s", "g"): 4,
        ("g", "e"): 3, ("g", "t"): 4,
        ("t", "c"): 2
    }
    edges = list(upper_bounds.keys())

    assert minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_bfs)[1] == minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_dfs)[1]
    assert minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_bfs)[1] == minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_max)[1]
    assert minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_bfs)[1] == minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_min)[1]

    pretty_print_minimum_flow("Minimum Flow (BFS)", *minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_bfs))
    pretty_print_minimum_flow("Minimum Flow (DFS)", *minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_dfs))
    pretty_print_minimum_flow("Minimum Flow (MAX)", *minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_max))
    pretty_print_minimum_flow("Minimum Flow (MIN)", *minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_min))
    #'''

    #''' Week 5 SGT Question 2. Min flow = 13.
    nodes = ["s", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "t"]
    lower_bounds = {
        ("s", "a"): 0, ("s", "c"): 0, ("s", "e"): 0, ("s", "g"): 0, ("s", "i"): 0,
        ("a", "b"): 5,
        ("b", "c"): 0, ("b", "e"): 0, ("b", "t"): 0,
        ("c", "d"): 6,
        ("d", "t"): 0,
        ("e", "f"): 5, ("e", "i"): 0,
        ("f", "c"): 0, ("f", "i"): 0, ("f", "t"): 0,
        ("g", "h"): 4,
        ("h", "i"): 0, ("h", "t"): 0,
        ("i", "j"): 7,
        ("j", "t"): 0,
    }
    upper_bounds = {
        ("s", "a"): float("inf"), ("s", "c"): float("inf"), ("s", "e"): float("inf"), ("s", "g"): float("inf"), ("s", "i"): float("inf"),
        ("a", "b"): float("inf"),
        ("b", "c"): float("inf"), ("b", "e"): float("inf"), ("b", "t"): float("inf"),
        ("c", "d"): float("inf"),
        ("d", "t"): float("inf"),
        ("e", "f"): float("inf"), ("e", "i"): float("inf"),
        ("f", "c"): float("inf"), ("f", "i"): float("inf"), ("f", "t"): float("inf"),
        ("g", "h"): float("inf"),
        ("h", "i"): float("inf"), ("h", "t"): float("inf"),
        ("i", "j"): float("inf"),
        ("j", "t"): float("inf"),
    }
    edges = list(upper_bounds.keys())
    flow = {
        ("s", "a"): 5, ("s", "c"): 6, ("s", "e"): 5, ("s", "g"): 4, ("s", "i"): 7,
        ("a", "b"): 5,
        ("b", "c"): 0, ("b", "e"): 0, ("b", "t"): 5,
        ("c", "d"): 6,
        ("d", "t"): 6,
        ("e", "f"): 5, ("e", "i"): 0,
        ("f", "c"): 0, ("f", "i"): 0, ("f", "t"): 5,
        ("g", "h"): 4,
        ("h", "i"): 0, ("h", "t"): 4,
        ("i", "j"): 7,
        ("j", "t"): 7,
    }

    assert minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_bfs)[1] == minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_dfs)[1]
    assert minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_bfs)[1] == minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_max)[1]
    assert minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_bfs)[1] == minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_min)[1]
    assert minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_bfs, feasible_flow=flow)[1] == minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_dfs, feasible_flow=flow)[1]
    assert minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_bfs, feasible_flow=flow)[1] == minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_max, feasible_flow=flow)[1]
    assert minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_bfs, feasible_flow=flow)[1] == minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_min, feasible_flow=flow)[1]

    pretty_print_minimum_flow("Minimum Flow (BFS)", *minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_bfs, feasible_flow=flow))
    pretty_print_minimum_flow("Minimum Flow (DFS)", *minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_dfs, feasible_flow=flow))
    pretty_print_minimum_flow("Minimum Flow (MAX)", *minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_max, feasible_flow=flow))
    pretty_print_minimum_flow("Minimum Flow (MIN)", *minimum_flow(nodes, edges, lower_bounds, upper_bounds, "s", "t", find_augmenting_path_min, feasible_flow=flow))
    #'''
