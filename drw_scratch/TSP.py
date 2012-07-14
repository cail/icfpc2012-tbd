import collections
import mwmatching

def solve_TSP(nodes, weights, source, target):
    ''' Solve the metric TSP problem with fixed source and target nodes.
        Uses a modification of the Christofides algorithm. '''
    
    tree = build_MST(nodes, weights, (source, target))
    odd_nodes = odd_degree_nodes(tree)
    matching = minimal_weight_perfect_matching(odd_nodes, weights)

    combined_edges = tree + matching
    eulerian = eulerian_path(nodes, combined_edges)
    path = TSP_path(nodes, eulerian, (source, target))
    
    path = path[1:] + [path[0]]
    if path[0] != source:
        path.reverse()
    assert(path[0] == source and path[-1] == target) # sanity check
    return path

def build_MST(nodes, weights, initial_edge):
    ''' Build a spanning tree that is minimal among
        spanning trees containing initial_edge.
        
        Uses Prim's algorithm.'''
    
    tree_edges = [initial_edge]
    tree_nodes = list(initial_edge)
    
    while len(tree_nodes) < len(nodes):
        remaining_nodes = set(nodes) - set(tree_nodes)
        
        next_edge = [tree_nodes[0], next(iter(remaining_nodes))] 
        cost = weights[next_edge[0]][next_edge[1]] # avoids dealing with INF
        for tree_node in tree_nodes:
            for non_tree_node in remaining_nodes:
                if weights[tree_node][non_tree_node] < cost:
                    cost = weights[tree_node][non_tree_node]
                    next_edge = (tree_node, non_tree_node)
        tree_edges.append(next_edge)
        tree_nodes.append(next_edge[1])

    return list(tree_edges)
                    
def odd_degree_nodes(tree):
    degrees = collections.Counter()
    
    for node1, node2 in tree:
        degrees[node1] += 1
        degrees[node2] += 1
    
    return [node for node in degrees if degrees[node] % 2 == 1]

#def minimal_weight_perfect_matching(nodes, weights):
#    ''' Heuristic algorithm for minimal weight perfect matching.
#        Follows http://www.dcg.ethz.ch/publications/ctw04.pdf '''
    
def minimal_weight_perfect_matching(nodes, weights):
    ''' Heuristic algorithm for minimal weight perfect matching.
        A wrapper for something I found on the web. '''
        
    nodes = list(nodes)
   
    weighted_edges = []
    for i, node1 in enumerate(nodes):
        for j, node2 in enumerate(nodes):
            if j > i:
                weighted_edges.append((i, j, -weights[node1][node2]))
    
    mate = mwmatching.maxWeightMatching(weighted_edges, maxcardinality=True)
    
    matching = []
    for (i, j) in enumerate(mate):
        if j > i:   # implies j > -1, i.e. matching exists
            matching.append((nodes[i], nodes[j]))
    
    return matching
    
def eulerian_path(nodes, edges):
    ''' Find an Eulerian path using Hierholzer's algorithm. '''
    edges = list(edges)
    incident_edges = collections.defaultdict(lambda: [])
    for i, (node1, node2) in enumerate(edges):
        incident_edges[node1].append(i)
        incident_edges[node2].append(i)

    used_nodes = set()
    tour = [next(iter(nodes))]
    
    while len(tour) < len(edges) + 1:
        for (position, init_node) in enumerate(tour):
            if incident_edges[init_node]:
                break
        subtour = []
        
        node = init_node
        while True:
            edge_index = incident_edges[node].pop()
            node1, node2 = edges[edge_index]
            next_node = node1 if node2 == node else node2
            incident_edges[next_node].remove(edge_index)
            subtour.append(next_node)
            node = next_node
            if node == init_node: break
        tour = tour[:position + 1] + subtour + tour[position + 1:]
    return tour

def TSP_path(nodes, tour, initial_edge):
    ''' Use shortcuts to turn the Eulerian path into a TSP path. '''
    
    assert(tour[0] == tour[-1])
    tour = tour[:-1]
    
    source, target = initial_edge
    
    for i in xrange(-1, len(tour) - 1):
        if (tour[i] == source and tour[i+1] == target) or \
           (tour[i+1] == source and tour[i] == target):
           break
    
    tour = tour[i:] + tour[:i]

    path = []
    visited = set()
    for node in tour:
        if node not in visited:
            path.append(node)
            visited.add(node)
            
            if len(path) == len(nodes):
                break
    return path
        
                
                
        
        
        
    
    
    
    
    
