from util import get_outgoing_edges

def topological_sort_1(edges, root):
    """
    Topologically sorts nodes in a DAG.

    This method iteratively builds a sorted list by starting with the root node,
    checking outgoing edges and then adding the neighbours to the sorted list.
    If the neighbours are already in the sorted list, their position is changed
    accordingly. This process is then repeated with the next node in the sorted
    list, until all nodes in the sorted list have been checked.

    This method does not work with cycles and will not include disconnected
    nodes.

    Parameters
    ----------
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the DAG.
    root : str
        The root node.

    Returns
    -------
    list of str
        A list of nodes in the DAG, topologically sorted from the root node.
    """
    # Start off with the root.
    sorted_nodes = [root]
    index = 0

    # While the index is less than the length of the sorted list, there is still
    # a node we can search from.
    while (index < len(sorted_nodes)):
        # Get the node at the current index.
        current_node = sorted_nodes[index]

        # For each outgoing edge, if the end node is not in the sorted list yet,
        # add it to the sorted list. If it already is in the sorted list, and it
        # appears before the current node, move it to the back of the sorted
        # list.
        for (u, v) in get_outgoing_edges(current_node, edges):
            if v not in sorted_nodes:
                sorted_nodes.append(v)
            elif sorted_nodes.index(v) < index:
                sorted_nodes.remove(v)
                # The index is now the node after the current one. The insert
                # operation places the object before the given index. Using the
                # index will therefore place the node directly after the current
                # node.
                sorted_nodes.insert(index, v)
                # Now fix the index so that it corresponds to the current node again.
                index -= 1

        # Move to the next node in the sorted list.
        index += 1

    return sorted_nodes

def topological_sort_2(nodes, edges):
    """
    Topologically sorts nodes in a directed graph.

    This method works by placing nodes with an in-degree of 0 in the sorted
    list. These nodes are then "removed" from the graph and the in-degree of
    their neighbours updated accordingly. The process then repeats until there
    are no more nodes with an in-degree of 0.
    
    This method works with cycles (will return an empty list) and disconnected
    nodes.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the directed graph.
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the
        directed graph.

    Returns
    -------
    list of str
        A list of nodes in the directed graph, topologically sorted.
    """
    sorted_nodes = []
    in_degrees = {}

    # Set the in-degree of all nodes to 0.
    for node in nodes:
        in_degrees[node] = 0
    # For each edge, increment the in-degree of the end node by 1.
    for (u,v) in edges:
        in_degrees[v] += 1

    keep_looking = True
    while keep_looking:
        # Find a node with an in-degree of 0.
        valid_nodes = [node for (node, in_degree) in in_degrees.items() if in_degree == 0]
        
        # If a node with an in-degree of 0 can be found, add it to the list of
        # sorted nodes, set its in-degree to -1 (to mark it as sorted) and
        # update the in-degree of its neighbours.
        if valid_nodes: 
            node = valid_nodes[0]    
            sorted_nodes.append(node)
            in_degrees[node] = -1
            for (node, v) in get_outgoing_edges(node, edges):
                in_degrees[v] -= 1
        # If we cannot find such a node, the algorithm terminates.
        else:
            keep_looking = False

    return sorted_nodes

if __name__ == "__main__":    
    #'''
    print ("\nTest 1")
    nodes = ["s", "b", "c", "x", "g", "z", "a", "h"]
    edges = [
        ("s","b"), ("s","c"),
        ("b","x"),
        ("c", "g"), ("c", "z"),
        ("x","a"), ("x","h")
    ]
    print (topological_sort_1(edges, "s"))
    print (topological_sort_2(nodes, edges))
    #'''

    #'''
    print ("\nTest 2 (this test has a cycle)")
    nodes = ["s", "u", "x", "v", "y"]
    edges = [
        ("s","u"), ("s","x"),
        ("u","x"), ("u","v"),
        ("x","u"), ("x","y"), ("x","v"),
        ("v","y"),
        ("y","v"), ("y","s")
    ]
    print ("N/A")
    print (topological_sort_2(nodes, edges))
    #'''

    #'''
    print ("\nTest 3")
    nodes = ["begin", "b", "a", "e", "g", "c", "d", "h", "p", "f", "q", "end"]
    edges = [
        ("begin","b"), ("begin","a"), ("begin","e"),
        ("b","c"),
        ("a","c"), ("a","g"),
        ("e","g"),
        ("g","c"), ("g","h"),
        ("c","d"), ("c","p"),
        ("d","p"), ("d","f"),
        ("h","p"), ("h","q"),
        ("p","end"), ("p","q"),
        ("f","end"),
        ("q","end")
    ]
    print (topological_sort_1(edges, "begin"))
    print (topological_sort_2(nodes, edges))
    #'''

    #'''
    print ("\nTest 4")
    nodes = ["s", "b", "a", "c", "d"]
    edges = [
        ("s","a"), ("s","b"), ("s","c"),
        ("b","a"), ("b","c"), ("b","d"),
        ("a","d"), ("c","d")
    ]
    print (topological_sort_1(edges, "s"))
    print (topological_sort_2(nodes, edges))
    #'''

    #'''
    print ("\nTest 5 (this test contains a node not reachable from the root)")
    nodes = ["f", "a", "d", "e", "b", "c"]
    edges = [
        ("f","a"), ("f","d"),
        ("a","b"), ("a","d"),
        ("e","a"), ("e","d"), ("e","c"),
        ("b","c"),
    ]
    print (topological_sort_1(edges, "f"))
    print (topological_sort_2(nodes, edges))
    #'''
    
    print("")
