def dijkstra_all_nodes(graph_matrix, start_node):
    n = len(graph_matrix)
    
    # Deklarasi & Inisialisasi sesuai pseudocode
    L = [float('inf')] * n   # for i <- 1 to n, L(v_i) <- ∞
    L[start_node] = 0        # L(a) <- 0
    S = set()                # S <-(himpunan simpul yang sudah dipilih)
    
    # Array untuk melacak jalur (node pendahulu), 
    previous_nodes = [None] * n
    
    for k in range(n):
        # u <- pilih simpul yang belum terdapat di dalam S dan memiliki L(u) minimum
        min_distance = float('inf')
        u = -1
        for i in range(n):
            if i not in S and L[i] < min_distance:
                min_distance = L[i]
                u = i
        if u == -1:
            break
            
        S.add(u)
        
        # for semua simpul v yang tidak terdapat di dalam S
        for v in range(n):
            if v not in S:
                # G(u, v) bobot sisi dari u ke v
                weight = graph_matrix[u][v]
                
                # sisi dari u ke v 
                if weight > 0:
                    if L[u] + weight < L[v]:
                        L[v] = L[u] + weight
                        previous_nodes[v] = u
                        
    return L, previous_nodes

def get_shortest_path_and_distance(graph_matrix, start_node, target_node):
    """
    Mendapatkan rute terpendek dan total jarak dari start_node ke target_node.
    """
    distances, previous_nodes = dijkstra_all_nodes(graph_matrix, start_node)
    
    # Jika tidak ada jalur ke tujuan
    if distances[target_node] == float('inf'):
        return [], float('inf')
        
    # Membangun ulang jalur dari target kembali ke start
    path = []
    current = target_node
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]
        
    return path, distances[target_node]
