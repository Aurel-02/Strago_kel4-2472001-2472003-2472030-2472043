from graph import build_adjacency_matrix, NUM_NODES, EDGES, NODE_NAMES
 
 
def format_distance(distance):
	if distance == float("inf"):
		return "inf"
	return distance
 
 
def get_node_label(node, node_names=None):
	if node_names is None:
		return str(node)
	return node_names[node]
 
 
def dijkstra_all_nodes(graph_matrix, start_node, return_trace=False, node_names=None):
	n = len(graph_matrix)
 
	L = [float("inf")] * n
	L[start_node] = 0
	S = set()
	previous_nodes = [None] * n
	trace_rows = []
 
	for iteration in range(1, n + 1):
		min_distance = float("inf")
		u = -1
 
		for i in range(n):
			if i not in S and L[i] < min_distance:
				min_distance = L[i]
				u = i
 
		if u == -1:
			break
 
		S.add(u)
		updated_nodes = []
 
		for v in range(n):
			if v not in S:
				weight = graph_matrix[u][v]
 
				if weight > 0:
					new_distance = L[u] + weight
 
					if new_distance < L[v]:
						old_distance = L[v]
						L[v] = new_distance
						previous_nodes[v] = u
						updated_nodes.append(
							f"{get_node_label(v, node_names)}: "
							f"{format_distance(old_distance)} -> {format_distance(new_distance)} "
							f"lewat {get_node_label(u, node_names)}"
						)
 
		if return_trace:
			trace_rows.append({
				"Iterasi": iteration,
				"Node Dipilih": get_node_label(u, node_names),
				"Jarak Node": format_distance(L[u]),
				"Node Diperbarui": "; ".join(updated_nodes) if updated_nodes else "-",
				"Node Selesai": ", ".join(get_node_label(node, node_names) for node in sorted(S))
			})
 
	if return_trace:
		return L, previous_nodes, trace_rows
 
	return L, previous_nodes
 
 
def build_path(previous_nodes, start_node, target_node):
	path = []
	current = target_node
 
	while current is not None:
		path.insert(0, current)
		current = previous_nodes[current]
 
	if not path or path[0] != start_node:
		return []
 
	return path
 
 
def get_shortest_path_and_distance(graph_matrix, start_node, target_node):
	distances, previous_nodes = dijkstra_all_nodes(graph_matrix, start_node)
 
	if distances[target_node] == float("inf"):
		return [], float("inf")
 
	path = build_path(previous_nodes, start_node, target_node)
	return path, distances[target_node]
 
 
def get_dijkstra_trace(graph_matrix, start_node, target_node, node_names=None):
	distances, previous_nodes, trace_rows = dijkstra_all_nodes(
		graph_matrix,
		start_node,
		return_trace=True,
		node_names=node_names
	)
 
	if distances[target_node] == float("inf"):
		path = []
	else:
		path = build_path(previous_nodes, start_node, target_node)
 
	return {
		"path": path,
		"distance": distances[target_node],
		"trace_rows": trace_rows
	}
 
 
if __name__ == "__main__":
	matrix = build_adjacency_matrix(NUM_NODES, EDGES)
 
	start_node = 0
	target_node = 23
 
	print("--- Pengujian Algoritma Dijkstra ---")
	print(f"Mencari jalur terpendek dari '{NODE_NAMES[start_node]}' ke '{NODE_NAMES[target_node]}'")
 
	result = get_dijkstra_trace(matrix, start_node, target_node, NODE_NAMES)
 
	if result["distance"] != float("inf"):
		path_names = [NODE_NAMES[node] for node in result["path"]]
		print("\nJalur yang ditemukan:")
		print(" -> ".join(path_names))
		print(f"Total Jarak: {result['distance']}")
	else:
		print(f"\nTidak ditemukan jalur dari {NODE_NAMES[start_node]} ke {NODE_NAMES[target_node]}")
 
	print("\nJejak Perhitungan:")
	for row in result["trace_rows"]:
		print(f"Iterasi {row['Iterasi']} | Node: {row['Node Dipilih']} | Jarak: {row['Jarak Node']}")
		print(f"Update: {row['Node Diperbarui']}")
