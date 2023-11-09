def get_parent(node, nodes, parents):
    """
    Given a tree in the form of nodes and parents, returns the parent of a given
    node.

    Parameters
    ----------
    node : str
        The node whose parent is to be returned.
    nodes : list of str
        A list of all the nodes in the tree.
    parents : list of str
        A list of nodes in the tree such that parents[i] contains the parent of
        the i-th node in nodes.

    Returns
    -------
    str
        The parent of the given node.
    """
    index = nodes.index(node)
    return parents[index]

def is_tree(nodes, parents, root, debug=False):
    """
    Checks if a graph where every node has at most one parent is a tree.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the alleged tree.
    parents : list of str
        A list of all the nodes in the alleged tree such that parents[i]
        contains the parent of the i-th node in nodes.
    root : str
        The root node of the alleged tree.
    debug : bool, default False
        Whether to print debug information or not.

    Returns
    -------
    bool
        True if the graph is indeed a tree, false otherwise.
    """
    # If the root node has a parent, the graph is not a tree (or the root is not
    # the real root).
    if (get_parent(root, nodes, parents)): return False
    
    # For each node, see if the root can be reached by going backwards and
    # following the parents of nodes. Closed list is used to check for cycles.
    for i in range(len(nodes)):
        closed_list = []
        start_node = nodes[i]
        if debug:
            print ("\nStarting Node: " + start_node)  
        
        # Move backwards to the parent of the current node, until the current
        # node is the root or until it is part of a cycle.              
        current_node = start_node
        while (current_node != root and current_node not in closed_list):
            closed_list.append(current_node)
            if debug:
                print ("Closed list: " + str(closed_list))

            current_node = get_parent(current_node, nodes, parents)
            # If the current node does not have a parent, then it's not a tree,
            # since the root was not reached.
            if (not current_node):
                return False            
            if debug:
                print ("Current node: " + current_node)

        # If at the end the current node is not the root, then the while loop quit
        # because the current node is part of a cycle and therefore the graph is not
        # a tree.             
        if (current_node != root):
            return False

    # If the root can be reached from all nodes, the graph is a tree.
    return True

def has_cycles(nodes, parents, debug=False):   
    """
    Checks if a graph where every node has at most one parent contains a cycle.

    Parameters
    ----------
    nodes : list of str
        A list of all the nodes in the graph.
    parents : list of str
        A list of nodes such that parents[i] contains the parent of the i-th
        node in nodes.
    debug : bool, default False
        Whether to print debug information or not.

    Returns
    -------
    bool
        True if the graph contains a cycle, false otherwise.
    """ 
    # Set the label of every node to None.
    checked = []
    for i in range(len(nodes)):
        checked.append(None)

    # Iterate over all nodes.
    for start_node_index in range(len(nodes)):                
        start_node = nodes[start_node_index]
        if debug:
            print("\nStarting Node: " + start_node)

        # Move backwards to the parent of the current node, until the current
        # node is None (i.e. the previous node had no parent) or until the
        # current node already has a label.
        current_node = start_node
        current_node_index = start_node_index
        while (current_node != None and not checked[current_node_index]):
            # Set the label of the current node as the name of the start node.
            checked[current_node_index] = start_node
            if debug:
                print("Checked: " + str(checked)) 

            # Set the current node as the parent of the current node.
            current_node = get_parent(current_node, nodes, parents)
            # If a parent was found, update the current node index.
            if (current_node):
                if debug:
                    print("Current node: " + current_node)
                current_node_index = nodes.index(current_node)   

        # At this point either the current node is None (i.e. the last node had
        # no parent) or the current node is not None, but already had a label
        # when it was encountered. In the latter case, if the label is the name
        # of the start node, then a cycle exists.
        if (current_node != None and checked[current_node_index] == start_node):
            return True

    # If no cycles were found, then
    return False

if __name__ == "__main__":
    #''' Week 1 LGT Question 5
    print ("\nTest 1: this graph is a tree (and therefore has no cycles).")
    nodes = ["a", "b", "c", "g", "h", "s", "x", "z"]
    parents = ["x", "s", "s", "c", "x", None, "b", "c"]

    if is_tree(nodes, parents, "s"):
        print("The graph is a tree!")
    else:
        print("The graph is not a tree!")

    if has_cycles(nodes, parents):
        print("The graph contains a cycle!")
    else:
        print("The graph does not contain a cycle!")
    #'''

    #''' Week 1 LGT Question 5
    print ("\nTest 2: this graph is not a tree (has cycles).")
    nodes = ["a", "b", "c", "g", "h", "s", "x", "z"]
    parents = ["x", "h", "s", "c", "x", None, "b", "c"]

    if is_tree(nodes, parents, "s"):
        print("The graph is a tree!")
    else:
        print("The graph is not a tree!")

    if has_cycles(nodes, parents):
        print("The graph contains a cycle!")
    else:
        print("The graph does not contain a cycle!")
    #'''

    #''' Custom
    print ("\nTest 3: this graph is not a tree (doesn't have cycles, but is not connected).")
    nodes = ["a", "b", "c", "d"]
    parents = [None, "a", None, "c"]

    if is_tree(nodes, parents, "a"):
        print("The graph is a tree!")
    else:
        print("The graph is not a tree!")

    if has_cycles(nodes, parents):
        print("The graph contains a cycle!")
    else:
        print("The graph does not contain a cycle!")
    #'''

    print("")
