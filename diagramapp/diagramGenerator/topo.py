from copy import deepcopy

from dag import DiagramDag, get_adjacency_list


def nodes_without_incoming_edge(nodes: set[str], edges: set[tuple[str, str]]):
    return set(nodes).difference(set(map(lambda edge: edge[1], edges)))

def node_has_incoming_edge(node: str, edges: set[tuple[str, str]]):
    return len(get_edges(node, edges, True)) > 0

def get_edges(node: str, edges: set[tuple[str, str]], incoming = False):
    matches = list()
    for edge in edges:
        if edge[1 if incoming else 0] == node:
            matches.append(edge)
    return matches

def get_incoming_neighbour_positions(node: str, ordered_nodes: list[str], edges: set[tuple[str, str]])->list[int]:
    incoming_neighbours = set(map(lambda edge: edge[0], get_edges(node, edges, True)))
    positions = list()
    if len(incoming_neighbours) <= 0:
        return positions

    for i, n in enumerate(ordered_nodes):
        if n in incoming_neighbours:
            positions.append(i)

    positions.reverse()  # In descending order
    return positions

def lex_cmp(a: list[int], b: list[int]):
    """
    Determines the ordering of lists of integers lexicographically
    :param a: A list of integers
    :param b: A list of integers
    :return: 1 if a > b, 0 if a == b, -1 if a < b
    """
    max_ties = min(len(a), len(b))

    for ties in range(max_ties):
        if a[ties] < b[ties]:
            return -1
        elif a[ties] > b[ties]:
            return 1

    # If there is no winner by this point then the one with more neighbours is greater
    if len(a) < len(b):
        return -1
    elif len(a) > len(b):
        return 1
    else:
        return 0


def position_lexicographic_pop(nodes: set[str], edges: set[tuple[str, str]], ordered_nodes: list[str]):
    if len(nodes) <= 1:
        return nodes.pop()

    max_positions = []
    max_node = ''
    for node in nodes:
        node_positions = get_incoming_neighbour_positions(node, ordered_nodes, edges)
        if lex_cmp(node_positions, max_positions) >= 0:
            max_positions = node_positions
            max_node = node

    nodes.remove(max_node)
    return max_node

def kahns_topological_sort(nodes: set[str], edges: set[tuple[str, str]]):
    remaining_edges = deepcopy(edges)

    l = list()
    s = nodes_without_incoming_edge(nodes, edges)

    while len(s) > 0:

        n = position_lexicographic_pop(s, edges, l)
        l.append(n)

        for edge in get_edges(n, remaining_edges):
            m = edge[1]
            remaining_edges.remove(edge)
            if not node_has_incoming_edge(m, remaining_edges):
                s.add(m)
    return l

def dfs_topological_sort(nodes, edges):
    l = list()
    visited = set()

    adj = get_adjacency_list(nodes, edges)

    def visit(n):
        if n in visited:
            return

        for m in adj[n]:
            visit(m)

        visited.add(n)
        l.append(n)

    for node in nodes:
        if node not in visited:
            visit(node)
    l.reverse()
    return l

def transitive_reduction(dag: DiagramDag):
    topo = dfs_topological_sort(dag.get_node_ids(), dag.edges)

    # Start with all edges in the reduction
    edges_reduced = set(dag.edges)

    # Instantiate a dictionary mapping each node to known reachable nodes (initially empty set)
    reachable: dict[str, set[str]] = {u: set() for u in dag.get_node_ids()}

    adj = get_adjacency_list(dag.get_node_ids(), dag.edges)

    # Go in reverse topological order so we find the longest paths
    for u in reversed(topo):
        # --- Start of new, corrected logic for each node u ---

        # Pass 1: For each neighbor v, determine the complete set of nodes reachable
        # from u if one were to traverse the edge (u, v).
        reach_via = {v: {v} | reachable[v] for v in adj[u]}

        # Pass 2: For each edge (u, v), check if v is reachable from u via any *other*
        # neighbor w. If so, the edge (u, v) is redundant.
        for v in adj[u]:
            is_redundant = False
            for w in adj[u]:
                if v == w:
                    continue
                # If v is reachable through w's path, then (u, v) is a shortcut.
                if v in reach_via[w]:
                    is_redundant = True
                    break

            if is_redundant:
                if (u, v) in edges_reduced:
                    edges_reduced.remove((u, v))

        # Pass 3: Update the main `reachable` dictionary for u based ONLY on the
        # non-redundant edges that were kept.
        for v in adj[u]:
            if (u, v) in edges_reduced:
                reachable[u].add(v)
                reachable[u].update(reachable[v])

    return dag.nodes, edges_reduced