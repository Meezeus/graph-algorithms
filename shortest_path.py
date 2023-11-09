import heapq as hq
from queue import Queue
from util import get_outgoing_edges, prettify_edge_dict
from check_tree_and_cycles import has_cycles
from topological_sort import topological_sort_2

def initialise(nodes, s, parents, distances):
    """
    Initialises a shortest path problem by setting the parents and distances
    dicts to their appropriate initial values.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the graph.
    s : str
        The source node.
    parents : dict of {str : str}
        A dictionary where keys are nodes and values are the parents of the
        nodes in the shortest-distance tree.
    distances : dict of {str : int}
        A dictionary where keys are nodes and values are the shortest distances
        from the source node to the key nodes.
    """
    parents[s] = None
    distances[s] = 0
    for node in [node for node in nodes if node != s]:
        parents[node] = None
        distances[node] = float("inf")

def relax(edge, weights, parents, distances):
    """
    Performs the relax operation on the given edge.

    Parameters
    ----------
    edge : tuple of (str, str)
        The edge - represented as a pair of nodes (u, v) - on which to perform
        the relax operation.
    weights : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the weights of the edges.
    parents : dict of {str : str}
        A dictionary where keys are nodes and values are the parents of the
        nodes in the shortest-distance tree.
    distances : dict of {str : int}
        A dictionary where keys are nodes and values are the shortest distances
        from the source node to the key nodes.
    """
    (u,v) = edge
    if (distances[v] > distances[u] + weights[(u,v)]):
        distances[v] = distances[u] + weights[(u,v)]
        parents[v] = u

def relax_bellman_ford_fifo(edge, weights, parents, distances, active):
    """
    Performs the Bellman-Ford FIFO relax operation on the given edge.

    Parameters
    ----------
    edge : tuple of (str, str)
        The edge - represented as a pair of nodes (u, v) - on which to perform
        the relax operation.
    weights : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the weights of the edges.
    parents : dict of {str : str}
        A dictionary where keys are nodes and values are the parents of the
        nodes in the shortest-distance tree.
    distances : dict of {str : int}
        A dictionary where keys are nodes and values are the shortest distances
        from the source node to the key nodes.
    active : queue.Queue
        A queue of nodes that are active.
    """
    (u,v) = edge
    if (distances[v] > distances[u] + weights[(u,v)]):
        distances[v] = distances[u] + weights[(u,v)]
        parents[v] = u
        if (v not in active.queue): active.put(v)

def relax_dijkstra(edge, weights, parents, distances, heap):
    """
    Performs the Dijkstra relax operation on the given edge.

    Parameters
    ----------
    edge : tuple of (str, str)
        The edge - represented as a pair of nodes (u, v) - on which to perform
        the relax operation.
    weights : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the weights of the edges.
    parents : dict of {str : str}
        A dictionary where keys are nodes and values are the parents of the
        nodes in the shortest-distance tree.
    distances : dict of {str : int}
        A dictionary where keys are nodes and values are the shortest distances
        from the source node to the key nodes.
    heap : list of tuple of (int, str), sorted ascending according to the first
    value of the tuple
        A min-heap (priority queue) containing tuples where the first value is
        the distance from the source node and the second value is the node to
        which the distance is measured.
    """
    (u,v) = edge
    if (distances[v] > distances[u] + weights[(u,v)]):
        heap.remove((distances[v], v))
        distances[v] = distances[u] + weights[(u,v)]
        parents[v] = u        
        heap.append((distances[v], v))
        hq.heapify(heap)

def relax_dijkstra_plus(edge, weights, weights_hat, parents, distances, heap, h_values):
    """
    Performs the Dijkstra+ relax operation on the given edge.

    Parameters
    ----------
    edge : tuple of (str, str)
        The edge - represented as a pair of nodes (u, v) - on which to perform
        the relax operation.
    weights : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the weights of the edges.
    weights_hat : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the re-weighted weights of the edges.
    parents : dict of {str : str}
        A dictionary where keys are nodes and values are the parents of the
        nodes in the shortest-distance tree.
    distances : dict of {str : int}
        A dictionary where keys are nodes and values are the shortest distances
        from the source node to the key nodes.
    heap : list of tuple of (int, str), sorted ascending according to the first
    value of the tuple
        A min-heap (priority queue) containing tuples where the first value is
        the distance from the source node and the second value is the node to
        which the distance is measured.
    h_values : dict of {str : int}
        A dictionary where keys are nodes and values are numbers assigned to the
        nodes by the re-weighting scheme.
    """
    (u,v) = edge

    if (u,v) not in weights_hat:
        weights_hat[(u,v)] = weights[(u,v)] + h_values[u] - h_values[v]

    if (distances[v] > distances[u] + weights_hat[(u,v)]):
        heap.remove((distances[v], v))
        distances[v] = distances[u] + weights_hat[(u,v)]
        parents[v] = u        
        heap.append((distances[v], v))
        hq.heapify(heap)

def bellman_ford(nodes, edges, weights, s, debug=False):
    """
    Finds the shortest distance from a source node to all other nodes in a graph
    using the Bellman-Ford algorithm.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the graph.
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    weights : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the weights of the edges.
    s : str
        The source node.
    debug : bool, default False
        Whether to print debug information or not.

    Returns
    -------
    nodes : list of str
        A list of all the nodes in the graph.
    parents : dict of {str : str} or None
        A dictionary where keys are nodes and values are the parents of the
        nodes in the shortest-distance tree. None if shortest distances could
        not be found.
    distances : dict of {str : int} or None
        A dictionary where keys are nodes and values are the shortest distances
        from the source node to the key nodes. None if shortest distances could
        not be found.
    """
    parents = {}
    distances = {}
    initialise(nodes, s, parents, distances)

    for i in range(len(nodes) - 1):
        for edge in edges:
            relax(edge, weights, parents, distances)
        if debug:
            pretty_print_single_source("Bellman-Ford, iteration " + str(i + 1), nodes, parents, distances)

    for edge in edges:
        (u,v) = edge
        if (distances[v] > distances[u] + weights[(u,v)]):
            return (nodes, None, None)

    return (nodes, parents, distances)

def bellman_ford_fifo(nodes, edges, weights, s, debug=False):
    """
    Finds the shortest distance from a source node to all other nodes in a graph
    using the Bellman-Ford algorithm. This version uses a FIFO queue.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the graph.
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    weights : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the weights of the edges.
    s : str
        The source node.
    debug : bool, default False
        Whether to print debug information or not.

    Returns
    -------
    nodes : list of str
        A list of all the nodes in the graph.
    parents : dict of {str : str} or None
        A dictionary where keys are nodes and values are the parents of the
        nodes in the shortest-distance tree. None if shortest distances could
        not be found.
    distances : dict of {str : int} or None
        A dictionary where keys are nodes and values are the shortest distances
        from the source node to the key nodes. None if shortest distances could
        not be found.
    """
    parents = {}
    distances = {}
    initialise(nodes, s, parents, distances)

    active = Queue()
    active.put(s)

    counter = 0
    while (not active.empty()):
        counter += 1
        u = active.get()

        for edge in get_outgoing_edges(u, edges):
            relax_bellman_ford_fifo(edge, weights, parents, distances, active)
        if debug:
            pretty_print_single_source("Bellman-Ford with FIFO, loop " + str(counter) + "\nNode removed from queue: " + u, nodes, parents, distances)

        # Convert the parents map to an array. The index of the array
        # corresponds to a node, the value to that node's parent.
        parents_array = [parents[node] for node in nodes]
        if (has_cycles(nodes, parents_array)):
            return (nodes, None, None)
    
    return (nodes, parents, distances)

def dijkstra(nodes, edges, weights, s, debug=False):
    """
    Finds the shortest distance from a source node to all other nodes in a graph
    using Dijkstra's algorithm.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the graph.
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    weights : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the weights of the edges.
    s : str
        The source node.
    debug : bool, default False
        Whether to print debug information or not.

    Returns
    -------
    nodes : list of str
        A list of all the nodes in the graph.
    parents : dict of {str : str}
        A dictionary where keys are nodes and values are the parents of the
        nodes in the shortest-distance tree.
    distances : dict of {str : int}
        A dictionary where keys are nodes and values are the shortest distances
        from the source node to the key nodes.
    """
    parents = {}
    distances = {}
    initialise(nodes, s, parents, distances)

    heap = []
    for node in nodes:
        if node == s: heap.append((0, s))
        else: heap.append((float("inf"), node))
    hq.heapify(heap)

    counter = 0
    while (heap):
        counter += 1
        node = hq.heappop(heap)[1]

        for edge in get_outgoing_edges(node, edges):
            relax_dijkstra(edge, weights, parents, distances, heap)
        if debug:
            pretty_print_single_source("Dijkstra, iteration " + str(counter) + "\nNode removed from queue: " + node, nodes, parents, distances)

    return (nodes, parents, distances)

def dag_shortest_path(nodes, edges, weights, s, debug=False):
    """
    Finds the shortest distance from a source node to all other nodes in a DAG.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the DAG.
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the DAG.
    weights : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the weights of the edges.
    s : str
        The source node.
    debug : bool, default False
        Whether to print debug information or not.

    Returns
    -------
    nodes : list of str
        A list of all the nodes in the DAG.
    parents : dict of {str : str}
        A dictionary where keys are nodes and values are the parents of the
        nodes in the shortest-distance tree.
    distances : dict of {str : int}
        A dictionary where keys are nodes and values are the shortest distances
        from the source node to the key nodes.
    """
    sorted_nodes = topological_sort_2(nodes, edges)
    parents = {}
    distances = {}
    initialise(sorted_nodes, s, parents, distances)

    for node in sorted_nodes:
        for edge in get_outgoing_edges(node, edges):
            relax(edge, weights, parents, distances)
        if debug:
            pretty_print_single_source("DAG Shortest Paths, node " + node, sorted_nodes, parents, distances)
    
    return (sorted_nodes, parents, distances)

def johnson(nodes, edges, weights, debug=False):
    """
    Finds the shortest distance between all pairs of nodes in a graph using
    Johnson's algorithm.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the graph.
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    weights : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the weights of the edges.
    debug : bool, default False
        Whether to print debug information or not.

    Returns
    -------
    nodes : list of str
        A list of all the nodes in the graph.
    parents : dict of {tuple of (str, str) : str}
        A dictionary where keys are a tuple (source_node, node) and values are
        the parents of the nodes in the shortest-distance tree where the source
        node is source_node.
    distances : dict of {tuple of (str, str) : int}
        A dictionary where keys are a tuple (source_node, node) and values are
        the shortest distances from the source_nodes to the nodes.
    """
    if debug:
        print("\nJohnson Debug:\n----------------------------------------")
    parents = {}
    distances = {}

    nodes_prime = nodes.copy()
    nodes_prime.append("s_prime")
    edges_prime = edges.copy()
    weights_prime = weights.copy()
    for node in nodes:
        edges_prime.append(("s_prime", node))
        weights_prime[("s_prime", node)] = 0

    (_, _, h_values) = bellman_ford(nodes_prime, edges_prime, weights_prime, "s_prime")
    if (not h_values):
        return None
    if debug:
        print("h_values: " + str(h_values))
    
    weights_hat = {}
    for (u, v) in edges:
        weights_hat[(u,v)] = weights[(u,v)] + h_values[u] - h_values[v]
    if debug:
        print("weights_hat:\n" + prettify_edge_dict(weights_hat))
    
    for source_node in nodes:
        (_, parents_prime, distances_prime) = dijkstra(nodes, edges, weights_hat, source_node)
        for node in nodes:
            parents[(source_node, node)] = parents_prime[node]
            distances[(source_node, node)] = distances_prime[node] - h_values[source_node] + h_values[node]
    
    if debug:
        print("")
    return (nodes, parents, distances)

def dijkstra_plus(nodes, edges, weights, h_values, source, destination, debug=False):
    """
    Finds the shortest distance from a source node to a destination node in a
    graph using a modified version of Dijkstra's algorithm.

    This modified version uses a re-weighting scheme to direct the search
    towards the destination node. The re-weighting scheme acts as a sort of
    heuristic (similar to A* search).

    For more information, see
    https://11011110.github.io/blog/2008/04/03/reweighting-graph-for.html

    The re-weighting scheme needs to satisfy the triangle inequality in order to
    guarantee positive edges.

    An example of a re-weighting scheme for geographical networks would be h(v)
    = -dist (v, d), where dist (v, d) is the straight-line distance from node v
    to the destination d (computed from the coordinates of v and d).

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the graph.
    edges : list of tuple of (str, str)
        A list of edges - represented as a pair of nodes (u, v) - in the graph.
    weights : dict of {tuple of (str, str) : int}
        A dictionary where keys are edges - represented as a pair of nodes (u,
        v) - and values are the weights of the edges.
    h_values : dict of {str : int}
        A dictionary where keys are nodes and values are numbers assigned to the
        nodes by the re-weighting scheme.
    source : str
        The source node.
    destination : str
        The destination node.
    debug : bool, default False
        Whether to print debug information or not.

    Returns
    -------
    nodes : list of str
        A list of all the nodes in the graph.
    parents : dict of {str : str} or None
        A dictionary where keys are nodes and values are the parents of the
        nodes in the shortest-distance tree. None if the shortest distance could
        not be found.
    distances : dict of {str : int} or None
        A dictionary where keys are nodes and values are the shortest distances
        from the source node to the key nodes. None if the shortest distance
        could not be found.
    """
    parents = {}
    distances = {}
    initialise(nodes, source, parents, distances)

    heap = []
    for node in nodes:
        if node == source: heap.append((0, source))
        else: heap.append((float("inf"), node))
    hq.heapify(heap)

    weights_hat = {} 

    counter = 0
    while (heap):
        counter += 1
        node = hq.heappop(heap)[1]

        if node == destination:
            for node in nodes:
                distances[node] = distances[node] - h_values[source] + h_values[node]
            return (nodes, parents, distances)

        for edge in get_outgoing_edges(node, edges):
            relax_dijkstra_plus(edge, weights, weights_hat, parents, distances, heap, h_values)
        if debug:
            pretty_print_single_source("Dijkstra+, iteration " + str(counter) + "\nNode removed from queue: " + node, nodes, parents, distances)

    return (nodes, None, None)

def pretty_print_single_source(title, nodes, parents, distances):
    """
    Prints the results of finding the shortest distances in a single source
    problem in a user-friendly manner.

    Parameters
    ----------
    title : str
        The title of the problem to be printed.
    nodes : list of str
        A list of all the nodes in the graph.
    parents : dict of {str : str}
        A dictionary where keys are nodes and values are the parents of the
        nodes in the shortest-distance tree.
    distances : dict of {str : int}
        A dictionary where keys are nodes and values are the shortest distances
        from the source node to the key nodes.
    """
    print ("\n" + title)
    print ("----------------------------------------")
    if (not parents or not distances):
        print ("Negative cycle discovered!")
    else: 
        for node in nodes:
            print ("Parent of " + node + " is " + str(parents[node]) +
                ", distance of " + node + " is " + str(distances[node]))
    print("")

def pretty_print_all_pairs(title, nodes, parents, distances):
    """
    Prints the results of finding the shortest distances in an all pairs problem
    in a user-friendly manner.

    Parameters
    ----------
    title : str
        The title of the problem to be printed.
    nodes : list of str
        A list of all the nodes in the graph.
    parents : dict of {tuple of (str, str) : str}
        A dictionary where keys are a tuple (source_node, node) and values are
        the parents of the nodes in the shortest-distance tree where the source
        node is source_node.
    distances : dict of {tuple of (str, str) : int}
        A dictionary where keys are a tuple (source_node, node) and values are
        the shortest distances from the source_nodes to the nodes.
    """
    print ("\n" + title)
    print ("----------------------------------------")
    if (not parents or not distances):
        print ("Negative cycle discovered!")
    else: 
        print("Parent Matrix:")

        # Print the empty space and vertical separator.
        print("{:>3}".format(""), end="")
        print("{:>4}".format("||"), end="")
        # Print the nodes in order.
        for node in nodes:
            print("{:>4}".format(node), end="")
        print("")

        # Print the horizontal separator.
        for i in range(len(nodes) + 2):
            print("{:=>4}".format("="), end="")
        print("")

        # Print the node, a vertical separator and the cell value.
        for source_node in nodes:
            print("{:>3}".format(source_node), end="")
            print("{:>4}".format("||"), end="")
            for node in nodes:
                print("{:>4}".format(parents[(source_node, node)] if parents[(source_node, node)] != None else "-"), end="")
            print("")

        print("\nDistance Matrix:")

        # Print the empty space and vertical separator.
        print("{:>3}".format(""), end="")
        print("{:>4}".format("||"), end="")
        # Print the nodes in order.
        for node in nodes:
            print("{:>4}".format(node), end="")
        print("")

        # Print the horizontal separator.
        for i in range(len(nodes) + 2):
            print("{:=>4}".format("="), end="")
        print("")

        # Print the node, a vertical separator and the cell value.
        for source_node in nodes:
            print("{:>3}".format(source_node), end="")
            print("{:>4}".format("||"), end="")
            for node in nodes:
                print("{:>4}".format(distances[(source_node, node)]), end="")
            print("")

    print("")

if __name__ == "__main__":
    #''' Week 1 LGT Questions 3 and 4, Week 2 LGT Question 1
    nodes = ["s", "u", "x", "v", "y"]
    weights = {
        ("s","u"): 10, ("s","x"): 5,
        ("u","x"): 2, ("u","v"): 1,
        ("x","u"): 3, ("x","y"): 2, ("x","v"): 9,
        ("v","y"): 4,
        ("y","v"): 6, ("y","s"): 7
    }
    edges = list(weights.keys())
    source = "s"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    assert bellman_ford(nodes, edges, weights, source)[2] == dijkstra(nodes, edges, weights, source)[2]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))
    pretty_print_single_source("Dijkstra", *dijkstra(nodes, edges, weights, source))
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''

    #''' Week 1 Quiz Question 1
    nodes = ["a", "b", "c", "e", "f", "h", "p", "q", "u", "s"]
    weights = {
        ("a", "b"): 1,
        ("c", "b"): 5,
        ("e", "c"): 4,
        ("f", "e"): 2, ("f", "h"): 1,
        ("h", "p"): 3,
        ("p", "q"): 2,
        ("u", "q"): 6, ("u", "a"): 3,
        ("s", "c"): 0, ("s", "h"): 0, ("s", "u"): 0
    }
    edges = list(weights.keys())
    source = "s"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    assert bellman_ford(nodes, edges, weights, source)[2] == dijkstra(nodes, edges, weights, source)[2]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))
    pretty_print_single_source("Dijkstra", *dijkstra(nodes, edges, weights, source))
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''

    #''' Week 1 Quiz Question 2
    nodes = ["c1", "c2", "c3", "c4"]
    weights = {
        ("c1", "c2"): -1, ("c1", "c3"): -4,
        ("c2", "c3"): -2, ("c2", "c4"): -4,              
        ("c3", "c2"): 2, ("c3", "c4"): -1
    }
    edges = list(weights.keys())
    source = "c1"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''

    #''' Week 2 Slides 19-20
    nodes = ["begin", "b", "a", "e", "g", "c", "d", "h", "p", "f", "q", "end"]
    weights = {
        ("begin","a"): -3, ("begin","b"): -4, ("begin","e"): -1,
        ("a","c"): -5, ("a","g"): -4,
        ("b","c"): -3,
        ("e","g"): -5,
        ("g","c"): -3, ("g","h"): -5,
        ("c","d"): -4, ("c","p"): -6,
        ("d","f"): -2, ("d","p"): -3,
        ("h","p"): -3, ("h","q"): -7,
        ("p","q"): -1, ("p","end"): -6,
        ("f","end"): -4,
        ("q","end"): -3
    }
    edges = list(weights.keys())
    source = "begin"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    assert bellman_ford(nodes, edges, weights, source)[2] == dag_shortest_path(nodes, edges, weights, source)[2]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))
    pretty_print_single_source("DAG Shortest Paths", *dag_shortest_path(nodes, edges, weights, source))
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''

    #''' Week 2 Quiz Question 1
    nodes = ["s", "u", "x", "v", "y"]
    weights = {
        ("s","y"): 3, ("s","x"): 10,
        ("x","u"): 1,
        ("u","v"): 3, ("u","x"): 3,
        ("v","y"): 4, ("v","x"): 1,
        ("y","u"): 7, ("y","v"): 4, ("y","x"): 7
    }
    edges = list(weights.keys())
    source = "s"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    assert bellman_ford(nodes, edges, weights, source)[2] == dijkstra(nodes, edges, weights, source)[2]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))
    pretty_print_single_source("Dijkstra", *dijkstra(nodes, edges, weights, source))
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''

    #''' Week 3 Slide 3
    nodes = ["A", "B", "C", "D", "E"]
    weights = {
        ("A","B"): 15, ("A","D"): 16,
        ("B","A"): 16, ("B","C"): 19, ("B","E"): 26,
        ("C","B"): 19, ("C","E"): 10,
        ("D","A"): 16,
        ("E","B"): 26, ("E","C"): 10, ("E","D"): 18,
    }
    edges = list(weights.keys())
    source = "A"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    assert bellman_ford(nodes, edges, weights, source)[2] == dijkstra(nodes, edges, weights, source)[2]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))   
    pretty_print_single_source("Dijkstra", *dijkstra(nodes, edges, weights, source))   
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''

    #''' Week 3 Slide 8
    nodes = ["1", "2", "3", "4", "5"]
    weights = {
        ("1","2"): 3, ("1","3"): -2, ("1","5"): -4,
        ("2","4"): 1, ("2","5"): 7,
        ("3","2"): 4,
        ("4","1"): 2, ("4","3"): -5,
        ("5","4"): 6
    }
    edges = list(weights.keys())
    source = "1"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))    
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''

    #''' Week 3 Quiz Question 1
    nodes = ["0", "1", "2", "3", "4", "5"]
    weights = {
        ("0","1"): 0, ("0","2"): 0, ("0","3"): 0, ("0","4"): 0, ("0","5"): 0,
        ("1","2"): 3, ("1","3"): -2, ("1","5"): -4,
        ("2","4"): 1, ("2","5"): 7,
        ("3","2"): 4,
        ("4","3"): -5, ("4","1"): 2,
        ("5","4"): 6
    }
    edges = list(weights.keys())
    source = "0"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))    
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''

    #''' Week 3 SGT Question 5
    nodes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "p", "q", "r"]
    weights = {
        ("a","b"): 9, ("a","l"): 7, ("a","q"): 10,
        ("b","a"): 9, ("b","k"): 7, ("b","q"): 5,
        ("c","f"): 4, ("c","j"): 3, ("c","p"): 5, ("c","r"): 9,
        ("d","g"): 6, ("d","h"): 4,
        ("e","f"): 6, ("e","r"): 6,
        ("f","c"): 4, ("f","e"): 6, ("f","j"): 3,
        ("g","d"): 6, ("g","k"): 4, ("g","p"): 6, ("g","r"): 5,
        ("h","d"): 4, ("h","r"): 3,
        ("i","l"): 2, ("i","p"): 3, ("i","q"): 4,
        ("j","c"): 3, ("j","f"): 3, ("j","l"): 9,
        ("k","b"): 7, ("k","g"): 4, ("k","q"): 7,
        ("l","a"): 7, ("l","i"): 2, ("l","j"): 9,
        ("p","c"): 5, ("p","i"): 3, ("p","g"): 6, ("p","q"): 3, ("p","r"): 7,
        ("q","a"): 10, ("q","b"): 5, ("q","i"): 4, ("q","k"): 7, ("q","p"): 3,
        ("r","c"): 9, ("r","e"): 6, ("r","g"): 5, ("r","h"): 3, ("r","p"): 7
    }
    edges = list(weights.keys())
    h_values = {
        "a": -21,
        "b": -13,
        "c": -15,
        "d": -0,
        "e": -12,
        "f": -17,
        "g": -6,
        "h": -4,
        "i": -14,
        "j": -18,
        "k": -9,
        "l": -16,
        "p": -11,
        "q": -13,
        "r": -6
    }   # Straight-line distances are negated in order to work as h_values.
    source = "p"
    destination = "d"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    assert bellman_ford(nodes, edges, weights, source)[2] == dijkstra(nodes, edges, weights, source)[2]
    assert bellman_ford(nodes, edges, weights, source)[2][destination] == dijkstra_plus(nodes, edges, weights, h_values, source, destination)[2][destination]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))
    pretty_print_single_source("Dijkstra", *dijkstra(nodes, edges, weights, source))
    pretty_print_single_source("Geographical Dijkstra", *dijkstra_plus(nodes, edges, weights, h_values, source, destination))    
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''  

    #''' Week 7 LGT Question 2 Original
    nodes = ["a", "b", "c", "e", "k", "p", "q", "u", "v"]
    weights = {
        ("a","b"): 2, ("a","u"): 4, ("a","v"): 3,
        ("b","c"): 3,
        ("c","a"): 2, ("c","e"): 8, ("c","k"): 2, ("c","v"): 1,
        ("e","k"): 5,
        ("k","q"): 1,
        ("p","e"): 3,
        ("q","p"): 1,
        ("u","b"): 3, ("u","q"): 3,
        ("v","k"): 1, ("v","q"): 2,
    }
    edges = list(weights.keys())
    source = "a"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    assert bellman_ford(nodes, edges, weights, source)[2] == dijkstra(nodes, edges, weights, source)[2]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))
    pretty_print_single_source("Dijkstra", *dijkstra(nodes, edges, weights, source))
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''

    #''' 7CCSMBIM Week 6 Part 3
    nodes = ["s", "t11", "t12", "t13", "t21", "t22", "t23", "t31", "t32", "t33", "t"]
    weights = {
        ("s","t11"): -0, ("s","t21"): -0, ("s","t31"): -0,
        ("t11","t12"): -5 ,("t11","t31"): -5,
        ("t12","t13"): -4,

        #("t12","t32"): -4,
        ("t12","t23"): -4,

        ("t13","t"): -2, ("t13","t33"): -2,
        ("t21","t22"): -2, ("t21","t13"): -2,
        ("t22","t23"): -3, 
        ("t23","t"): -7, 
        ("t31","t32"): -3, ("t31","t22"): -3,
        ("t32","t33"): -6,

        #("t32","t23"): -6,
        ("t32","t12"): -6,

        ("t33","t"): -1, 
    }
    edges = list(weights.keys())
    source = "s"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''
    
    #''' 7CCSMBIM Week 7 Part 1
    nodes = ["s", "t11", "t12", "t13", "t21", "t22", "t23", "t31", "t32", "t33", "t"]
    weights = {
        ("s","t11"): -0, ("s","t21"): -0, ("s","t31"): -0,
        ("t11","t12"): -3 ,("t11","t33"): -3,
        ("t12","t13"): -2, ("t12","t21"): -2,
        ("t13","t"): -3, ("t13","t23"): -3,
        ("t21","t22"): -4,
        ("t22","t23"): -2, 
        ("t23","t"): -3, 
        ("t31","t32"): -2, ("t31","t12"): -2,
        ("t32","t33"): -1, ("t32","t22"): -1,
        ("t33","t"): -2, ("t33","t22"): -2,
    }
    edges = list(weights.keys())
    source = "s"

    assert bellman_ford(nodes, edges, weights, source)[2] == bellman_ford_fifo(nodes, edges, weights, source)[2]
    distances = johnson(nodes, edges, weights)[2]
    for source_node in nodes:
        distances_prime = {}
        for node in nodes:
            distances_prime[node] = distances[(source_node, node)]
        assert bellman_ford(nodes, edges, weights, source_node)[2] ==  distances_prime

    pretty_print_single_source("Bellman Ford", *bellman_ford(nodes, edges, weights, source))
    pretty_print_single_source("Bellman Ford with FIFO", *bellman_ford_fifo(nodes, edges, weights, source))
    pretty_print_all_pairs("Johnson", *johnson(nodes, edges, weights))
    #'''
