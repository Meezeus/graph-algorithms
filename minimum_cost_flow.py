from util import prettify_edge_dict, calculate_path_capacity
from shortest_path import bellman_ford

def construct_residual_graph(nodes, edges, capacities, costs, supply, flow):
    """
    Constructs a residual graph.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the original graph.
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the
        original graph.
    capacities : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - in the original graph and values are the original capacities of the
        edges.
    costs : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) in the original graph and values are the costs of the edges.
    supply : list of int
        A list of numbers such that supply[i] is the original supply of the i-th
        node of nodes. Negative numbers represent demand.
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
    residual_costs : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - in the residual graph and values are the cost of the edges.
    residual_supply : list of int
        A list of numbers such that supply[i] is the residual supply of the i-th
        node of nodes. Negative numbers represent demand.
    """
    residual_capacities = {}
    residual_costs = {}
    residual_supply = {}

    for (u, v) in edges:
        residual_capacities[(u, v)] = capacities[(u, v)] - flow[(u, v)]
        residual_capacities[(v, u)] = flow[(u, v)]
        residual_costs[(u, v)] = costs[(u, v)]
        residual_costs[(v, u)] = -costs[(u, v)]

    residual_edges = [edge for edge in list(residual_capacities.keys()) if residual_capacities[edge] > 0]

    for node in nodes:
        residual_supply[node] = supply[node] + sum([flow[(u,v)] for (u,v) in edges if v == node]) - sum([flow[(v,w)] for (v,w) in edges if v == node])

    return (residual_edges, residual_capacities, residual_costs, residual_supply)

def minimum_cost_flow(nodes, edges, capacities, costs, supply, debug=False):
    """
    Attempts to find the minimum cost feasible flow that satisfies all demand.

    A feasible flow must satisfy three things: capacity constraints on edges,
    conservation of flow at nodes, and supply-demand of the nodes.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the graph.
    edges : list of tuple of (str, str)
        A list of edges represented as a pair of nodes (u, v).
    capacities : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the capacities of the edges.
    costs : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the costs of the edges.
    supply : list of int
        A list of numbers such that supply[i] is the supply of the i-th node of
        nodes. Negative numbers represent demand.
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
    flow_cost : int
        The total cost of the flow that was found.
    """
    # Initialise flow.
    flow = {}
    for edge in edges:
        flow[edge] = 0

    # Construct the residual graph.
    (residual_edges, residual_capacities, residual_costs, residual_supply) = construct_residual_graph(nodes, edges, capacities, costs, supply, flow)

    # Keep trying to send flow from supply nodes to demand nodes along the lowest-cost path.
    counter = 0
    residual_supply_nodes = [node for node in nodes if residual_supply[node] > 0]
    while residual_supply_nodes:
        counter += 1
        if debug:
            print ("\nMinimum Cost Flow Debug (iteration " + str(counter) + ")\n----------------------------------------")

        supply_node = residual_supply_nodes[0]

        # Compute a shortest-path (i.e. min cost) tree in the residual graph from the current supply node.
        (nodes, parents, distances) = bellman_ford(nodes, residual_edges, residual_costs, supply_node)

        # Find a residual demand node in the tree.
        residual_demand_nodes = [node for node in nodes if residual_supply[node] < 0 and parents[node]]
        # If a residual demand node was found, send flow to it.
        if residual_demand_nodes:
            # Find the path from the supply node to the demand node.
            demand_node = residual_demand_nodes[0]
            augmenting_path_edges = []
            current_node = demand_node
            parent = parents[current_node]
            while (parent):
                augmenting_path_edges.append((parent, current_node))
                current_node = parent
                parent = parents[current_node]
            augmenting_path_edges.reverse()
            
            # Find the capacity of that path, and augment the flow.
            augmenting_path_capacity = min(residual_supply[supply_node], -residual_supply[demand_node], calculate_path_capacity(residual_capacities, augmenting_path_edges))
            for (u, v) in edges:
                if (u, v) in augmenting_path_edges:
                    flow[(u, v)] += augmenting_path_capacity
                if (v, u) in augmenting_path_edges:
                    flow[(u, v)] -= augmenting_path_capacity

            if debug:
                print ("Sent " + str(augmenting_path_capacity) + " units of flow from " + str(supply_node) + " to " + str(demand_node) + " along the path " + str(augmenting_path_edges))
                print("The current flow is:\n" + prettify_edge_dict(flow))

            # Construct the new residual graph.
            (residual_edges, residual_capacities, residual_costs, residual_supply) = construct_residual_graph(nodes, edges, capacities, costs, supply, flow)

            # If the residual supply of the current supply node is 0, remove it from the list.
            if residual_supply[supply_node] == 0:
                residual_supply_nodes.remove(supply_node)

        # If no residual demand node found in the tree, remove the current supply node from the list.
        else:
            residual_supply_nodes.remove(supply_node)

    # Check if the flow found is feasible.
    feasible = True
    for node in nodes:
        net_outgoing_flow = sum([flow[(v,w)] for (v,w) in edges if v == node]) - sum([flow[(u,v)] for (u,v) in edges if v == node])        
        if net_outgoing_flow != supply[node]:
            feasible = False

    # Find the value of the flow.
    flow_value = 0
    for node in [node for node in nodes if supply[node] > 0]:
        flow_value += sum([flow[(v,w)] for (v,w) in edges if v == node]) - sum([flow[(u,v)] for (u,v) in edges if v == node])

    # Find the cost of the flow.
    flow_cost = 0
    for edge in edges:
        flow_cost += flow[edge] * costs[edge]

    return (feasible, flow, flow_value, flow_cost)

def pretty_print_minimum_cost_flow(title, feasible, flow, flow_value, flow_cost):
    """
    Prints the results of finding a minimum cost feasible flow in a
    user-friendly manner.

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
    flow_cost : int
        The total cost of the flow that was found.
    """
    print ("\n" + title)
    print ("----------------------------------------")
    if feasible:
        print("A feasible flow that satisfies all supplies and demands DOES exist!")
        print("The minimum cost feasible flow with a value of " + str(flow_value) + " and a cost of " + str(flow_cost) + " is:\n" + prettify_edge_dict(flow))
    else:
        print("A feasible flow that satisfies all supplies and demands DOES NOT exist!")
        print("The minimum cost best flow with a value of " + str(flow_value) + " and a cost of " + str(flow_cost) + " is:\n" + prettify_edge_dict(flow))
    print("")

if __name__ == "__main__":
    #''' Week 7 Slide 9. Feasible flow of value 12 and cost 60.
    supply = {
        "a": 5,
        "b": 7,
        "c": 0,
        "i": -9,
        "p": -3
    }
    nodes = list(supply.keys())
    capacities = {
        ("a", "c"): 4, ("a", "i"): 5,
        ("b", "c"): 8, ("b", "p"): 4,        
        ("c", "i"): 9, ("c", "p"): 3
    }
    costs = {
        ("a", "c"): 1, ("a", "i"): 3,
        ("b", "c"): 4, ("b", "p"): 3,        
        ("c", "i"): 5, ("c", "p"): 0
    }
    edges = list(capacities.keys())

    pretty_print_minimum_cost_flow("Minimum Cost Flow", *minimum_cost_flow(nodes, edges, capacities, costs, supply))
    #'''

    #''' Week 7 LGT Question 2c. Feasible flow of value 13 and cost 84.
    supply = {
        "c": 5,
        "a": 8,
        "b": 0,
        "e": -4,
        "k": -6,
        "p": 0,
        "q": -3,
        "u": 0,
        "v": 0
    }
    nodes = list(supply.keys())
    capacities = {
        ("a", "b"): 2, ("a", "u"): 5, ("a", "v"): 4,
        ("b", "c"): 2,        
        ("c", "a"): 3, ("c", "e"): 3, ("c", "k"): 1, ("c", "v"): 4,
        ("e", "k"): 1,
        ("k", "q"): 8,
        ("p", "e"): 4,
        ("q", "p"): 4,
        ("u", "b"): 6, ("u", "q"): 4,
        ("v", "k"): 4, ("v", "q"): 4,
    }
    costs = {
        ("a", "b"): 2, ("a", "u"): 4, ("a", "v"): 3,
        ("b", "c"): 3,        
        ("c", "a"): 2, ("c", "e"): 8, ("c", "k"): 2, ("c", "v"): 1,
        ("e", "k"): 5,
        ("k", "q"): 1,
        ("p", "e"): 3,
        ("q", "p"): 1,
        ("u", "b"): 3, ("u", "q"): 3,
        ("v", "k"): 1, ("v", "q"): 2,
    }
    edges = list(capacities.keys())

    pretty_print_minimum_cost_flow("Minimum Cost Flow", *minimum_cost_flow(nodes, edges, capacities, costs, supply))
    #'''
