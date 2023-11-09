# Graph Algorithms

This is a collection of various graph algorithms, implemented in
[Python](https://www.python.org/), that I wrote for one of my modules at
university. This was not required, but I thought it would help with my
understanding - plus I could use it to double check my work! The files and their
contents are as follows:

* *util.py*
  * Contains various auxiliary functions for graphs, such as: getting the
    outgoing edges of a node; formatting {edge : value} dictionaries for
    user-friendly printing; turning a path represented as a list of nodes into a
    path represented by a list of edges; calculating the flow capacity of a
    path; and calculating the total net outgoing flow from a node.

* *check_tree_and_cycles.py*
  * Contains code for checking if a graph is a tree and for checking if a graph
    contains cycles. 

* *topological_sort.py*
  * Contains two different methods for topologically sorting nodes in a graph.

* *shortest_path.py*
  * Contains methods for finding the shortest path between nodes in a graph.
    Includes the Bellman-Ford algorithm, the Bellman-Ford algorithm with FIFO
    queue, Dijkstra's algorithm, an algorithm for finding shortest paths in
    DAGs, Johnson's algorithm and a modified version of Dijkstra's algorithm
    that uses a re-weighting scheme to direct the search (similar to A* search).

* *maximum_flow.py*
  * Contains code for solving the maximum flow problem using the Ford-Fulkerson
    method. Includes code for building residual graphs and various methods for
    finding augmenting paths in residual graphs.

* *feasible_flow.py*
  * Contains code for solving the feasible flow problem.

* *minimum_cost_flow.py*
  * Contains code for solving the minimum cost feasible flow problem. This
    includes code for building residual graphs.

* *minimum_flow.py*
  * Contains code for solving the minimum feasible flow problem. This includes
    code for building residual graphs and a modified version of the
    Ford-Fulkerson algorithm.

All methods are well-documented and most of the files also contain some tests
for the methods - questions from slides/tutorials/past papers etc. These can be
used as example use cases.

For more information about the algorithms implemented (including their
constraints and limitations), I recommend the [CLRS
textbook](https://en.wikipedia.org/wiki/Introduction_to_Algorithms).
