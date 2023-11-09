def get_outgoing_edges(node, edges):
    """
    Returns outgoing edges from a node in a graph.

    Parameters
    ----------
    node : str
        The node whose outgoing edges are to be returned.
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.

    Returns
    -------
    list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - outgoing from
        the node.
    """
    return [(u,v) for (u,v) in edges if u == node]

def prettify_edge_dict(dict):
    """
    Returns a user-friendly string showing the values associated with edges in a
    graph.

    Parameters
    ----------
    dict : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are some sort of numbers.

    Returns
    -------
    str
        A formatted string such that each line contains all the edges outgoing
        from a single node and their respective values. Edges with values of 0
        are not included.
    """
    string = ""

    previous_u = None    
    for ((u, v), value) in [((u,v), value) for ((u,v), value) in list(dict.items()) if value != 0]:
        # Add a newline if the base node changes.
        if previous_u != None and previous_u != u:
            string += "\n"
        string += str((u, v)) + ": " + str(value) + ", "
        previous_u = u

    string = string[:-2]    # Remove the last comma and space.
    return string

def get_path_edges(path_nodes):
    """
    Turns a path represented by a list of nodes into a path represented by a
    list of edges, where an edge is a pair of nodes (u, v).

    Parameters
    ----------
    path_nodes : list of str
        A list of nodes that lie on the path.

    Returns
    -------
    list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - that lie on
        the path.
    """
    path_edges = []
    for index in range(0, len(path_nodes) - 1):
        edge = (path_nodes[index], path_nodes[index + 1])
        path_edges.append(edge)
    return path_edges

def calculate_path_capacity(capacities, path_edges):
    """
    Calculates the capacity of a path in a flow graph.

    Parameters
    ----------
    capacities : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the capacities of the edges.
    path_edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - representing
        the path.

    Returns
    -------
    int
        The capacity of the path, i.e. the max min capacity along the path.

    """
    path_capacity = float("inf")
    for edge in path_edges:
        if capacities[edge] < path_capacity:
            path_capacity = capacities[edge]
    return path_capacity

def calculate_flow_value(flow, node):
    """
    Calculates the total net outgoing flow from a node in a flow graph.

    Parameters
    ----------
    flow : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - in a graph and values are the flow along the edges.
    node : str
        The node whose total net outgoing flow is to be calculated.

    Returns
    -------
    int
        The total net outgoing flow from the node.
    """
    flow_value = 0
    for outgoing_edge in [(u, v) for (u, v) in list(flow.keys()) if u == node]:
        flow_value += flow[outgoing_edge]
    for incoming_edge in [(u, v) for (u, v) in list(flow.keys()) if v == node]:
        flow_value -= flow[incoming_edge]
    return flow_value
