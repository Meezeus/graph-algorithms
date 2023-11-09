from util import prettify_edge_dict
from maximum_flow import ford_fulkerson, find_augmenting_path_bfs, find_augmenting_path_dfs, find_augmenting_path_max, find_augmenting_path_min

def feasible_flow(nodes, edges, capacities, supply, search_method, flow = None, debug = False):
    """
    Attempts to find a feasible flow in a flow graph.

    A feasible flow must satisfy three things: capacity constraints on edges,
    conservation of flow at nodes, and supply-demand of the nodes.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the graph.
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph
    capacities : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are capacities of the edges.
    supply : list of int
        A list of numbers such that supply[i] is the supply of the i-th node of
        nodes. Negative numbers represent demand.
    search_method : (list of tuple of (str, str), dict of {tuple of (str, str) :
    int}, str, str) --> list of str
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
    feasible : bool
        True if a feasible flow was found that satisfies all conditions, false
        otherwise.
    flow : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the flow along the edges. This is the best flow that
        could be found.
    flow_value : int
        The total value of the flow that was found.
    """
    # Construct G_prime by adding edges from the new source node s_prime to all
    # supply nodes, and from all demand nodes to the new sink node t_prime. The
    # capacity of each such edge is the supply/demand at the node.
    edges_prime = edges.copy()
    capacities_prime = capacities.copy()
    for node in nodes:
        if supply[node] > 0:
            edges_prime.append(("s_prime", node))
            capacities_prime[("s_prime", node)] = supply[node]
        elif supply[node] < 0:
            edges_prime.append((node, "t_prime"))
            capacities_prime[(node, "t_prime")] = -supply[node]

    # Find the maximum flow from s_prime to t_prime.
    (flow_prime, flow_value) = ford_fulkerson(edges_prime, capacities_prime, "s_prime", "t_prime", search_method, flow, debug)

    # Turn flow_prime to flow by removing the added edges.
    flow = {}
    for edge in edges:
        flow[edge] = flow_prime[edge]

    # Check that the flow is feasible, by checking that the net outgoing flow
    # from each node is equal to the supply value at that node.
    for node in nodes:
        net_outgoing_flow = sum([flow[(v,w)] for (v,w) in edges if v == node]) - sum([flow[(u,v)] for (u,v) in edges if v == node])        
        if net_outgoing_flow != supply[node]:
            return (False, flow, flow_value)

    return (True, flow, flow_value)

def pretty_print_feasible_flow(title, feasible, flow, flow_value):
    """
    Prints the results of finding a feasible flow in a user-friendly manner.

    Parameters
    ----------
    title : str
        The title of the problem to be printed.
    feasible : bool
        True if a feasible flow was found that satisfies all conditions, false
        otherwise.
    flow : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the flow along the edges. This is the best flow that
        could be found.
    flow_value : int
        The total value of the flow that was found.
    """
    print ("\n" + title)
    print ("----------------------------------------")
    if feasible:
        print ("A feasible flow that satisfies all supplies and demands DOES exist!")
        print ("The feasible flow, with a value of " + str(flow_value) + ", is:\n" + prettify_edge_dict(flow))
    else:
        print ("A feasible flow that satisfies all supplies and demands DOES NOT exist!")
        print ("The max flow, with a value of " + str(flow_value) + ", is:\n" + prettify_edge_dict(flow))
    print("")

if __name__ == "__main__":
    #''' Week 4 LGT Question 2. Feasible flow exists.
    supply = {
        "a": 10,
        "b": 0,
        "c": 0,
        "d": -8,
        "e": 3,
        "f": 0,
        "g": 0,
        "h": -5
    }
    nodes = list(supply.keys())
    capacities = {
        ("a", "b"): 6, ("a", "c"): 7, ("a", "f"): 2,
        ("b", "c"): 8, ("b", "g"): 7,
        ("c", "d"): 6,
        ("e", "b"): 2, ("e", "f"): 1,
        ("f", "c"): 4, ("f", "h"): 4,
        ("g", "d"): 2, ("g", "h"): 3
    }
    edges = list(capacities.keys())

    assert feasible_flow(nodes, edges, capacities, supply, find_augmenting_path_bfs)[0] == feasible_flow(nodes, edges, capacities, supply, find_augmenting_path_dfs)[0]
    assert feasible_flow(nodes, edges, capacities, supply, find_augmenting_path_bfs)[0] == feasible_flow(nodes, edges, capacities, supply, find_augmenting_path_max)[0]
    assert feasible_flow(nodes, edges, capacities, supply, find_augmenting_path_bfs)[0] == feasible_flow(nodes, edges, capacities, supply, find_augmenting_path_min)[0]

    pretty_print_feasible_flow("Feasible Flow (BFS)", *feasible_flow(nodes, edges, capacities, supply, find_augmenting_path_bfs))
    pretty_print_feasible_flow("Feasible Flow (DFS)", *feasible_flow(nodes, edges, capacities, supply, find_augmenting_path_dfs))
    pretty_print_feasible_flow("Feasible Flow (MAX)", *feasible_flow(nodes, edges, capacities, supply, find_augmenting_path_max))
    pretty_print_feasible_flow("Feasible Flow (MIN)", *feasible_flow(nodes, edges, capacities, supply, find_augmenting_path_min))
    #'''
