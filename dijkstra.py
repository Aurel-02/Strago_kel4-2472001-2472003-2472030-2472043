from graph import build_adjacency_matrix, NUM_NODES, EDGES, NODE_NAMES


def _format_distance(value):
    if value == float("inf"):
        return "∞"
    return str(value)


def _build_path(previous_nodes, start_node, target_node):
    path = []
    current = target_node

    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    if not path or path[0] != start_node:
        return []

    return path


def _dijkstra_core(graph_matrix, start_node, record_steps=False):
    n = len(graph_matrix)

    distances = [float("inf")] * n
    distances[start_node] = 0

    visited = set()
    previous_nodes = [None] * n
    steps = []

    for iteration in range(1, n + 1):
        minimum_distance = float("inf")
        selected_node = -1

        for node in range(n):
            if node not in visited and distances[node] < minimum_distance:
                minimum_distance = distances[node]
                selected_node = node

        if selected_node == -1:
            if record_steps:
                steps.append({
                    "Iterasi": iteration,
                    "Node Dipilih": "Tidak ada node tersisa yang dapat dijangkau",
                    "Jarak Node Dipilih": "∞",
                    "Update Tetangga": "Proses berhenti",
                    "Node Terkunci": ", ".join(NODE_NAMES[node] for node in sorted(visited)) or "-",
                    "Jarak Sementara": " | ".join(
                        f"{NODE_NAMES[node]}={_format_distance(distances[node])}"
                        for node in range(n)
                    )
                })
            break

        visited.add(selected_node)
        updates = []

        for neighbor in range(n):
            weight = graph_matrix[selected_node][neighbor]

            if neighbor in visited or weight <= 0:
                continue

            new_distance = distances[selected_node] + weight

            if new_distance < distances[neighbor]:
                old_distance = distances[neighbor]
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = selected_node
                updates.append(
                    f"{NODE_NAMES[neighbor]}: {_format_distance(old_distance)} → {new_distance} "
                    f"via {NODE_NAMES[selected_node]}"
                )

        if record_steps:
            steps.append({
                "Iterasi": iteration,
                "Node Dipilih": NODE_NAMES[selected_node],
                "Jarak Node Dipilih": _format_distance(minimum_distance),
                "Update Tetangga": "; ".join(updates) if updates else "Tidak ada update",
                "Node Terkunci": ", ".join(NODE_NAMES[node] for node in sorted(visited)),
                "Jarak Sementara": " | ".join(
                    f"{NODE_NAMES[node]}={_format_distance(distances[node])}"
                    for node in range(n)
                )
            })

    return distances, previous_nodes, steps


def dijkstra_all_nodes(graph_matrix, start_node):
    distances, previous_nodes, _ = _dijkstra_core(
        graph_matrix,
        start_node,
        record_steps=False
    )
    return distances, previous_nodes


def dijkstra_all_nodes_with_steps(graph_matrix, start_node):
    return _dijkstra_core(
        graph_matrix,
        start_node,
        record_steps=True
    )


def get_shortest_path_and_distance(graph_matrix, start_node, target_node):
    distances, previous_nodes = dijkstra_all_nodes(graph_matrix, start_node)

    if distances[target_node] == float("inf"):
        return [], float("inf")

    path = _build_path(previous_nodes, start_node, target_node)
    return path, distances[target_node]


def get_shortest_path_with_steps(graph_matrix, start_node, target_node):
    distances, previous_nodes, steps = dijkstra_all_nodes_with_steps(
        graph_matrix,
        start_node
    )

    if distances[target_node] == float("inf"):
        return [], float("inf"), steps

    path = _build_path(previous_nodes, start_node, target_node)
    return path, distances[target_node], steps


if __name__ == "__main__":
    matrix = build_adjacency_matrix(NUM_NODES, EDGES)

    start_node = 0
    target_node = 23

    print("--- Pengujian Algoritma Dijkstra ---")
    print(f"Mencari jalur terpendek dari '{NODE_NAMES[start_node]}' ke '{NODE_NAMES[target_node]}'")

    path, distance, steps = get_shortest_path_with_steps(
        matrix,
        start_node,
        target_node
    )

    print("\nJejak iterasi Dijkstra:")
    for step in steps:
        print(
            f"Iterasi {step['Iterasi']} | "
            f"Node: {step['Node Dipilih']} | "
            f"Jarak: {step['Jarak Node Dipilih']} | "
            f"Update: {step['Update Tetangga']}"
        )

    if distance != float("inf"):
        path_names = [NODE_NAMES[node] for node in path]
        print("\nJalur yang ditemukan:")
        print(" -> ".join(path_names))
        print(f"Total Jarak: {distance} km")
    else:
        print(f"\nTidak ditemukan jalur dari {NODE_NAMES[start_node]} ke {NODE_NAMES[target_node]}")
