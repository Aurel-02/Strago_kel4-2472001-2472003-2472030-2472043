from data import NODE_NAMES, DEFAULT_EDGES

NUM_NODES = len(NODE_NAMES)
EDGES = DEFAULT_EDGES


def build_adjacency_matrix(num_nodes, edges):
    matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]

    for start, end, weight in edges:
        if start == end:
            continue
        if weight <= 0:
            continue

        matrix[start][end] = weight
        matrix[end][start] = weight

    return matrix


def get_neighbors(matrix, node):
    neighbors = []

    for neighbor, weight in enumerate(matrix[node]):
        if weight > 0:
            neighbors.append((neighbor, weight))

    return neighbors


def get_graph_info(edges=None):
    if edges is None:
        edges = EDGES

    total_weight = sum(weight for _, _, weight in edges)

    return {
        "jumlah_node": NUM_NODES,
        "jumlah_edge": len(edges),
        "total_bobot": total_weight,
        "rata_rata_bobot": round(total_weight / len(edges), 2) if edges else 0
    }


def route_to_text(route):
    return " -> ".join(NODE_NAMES[node] for node in route)


def _edge_key(start, end):
    return tuple(sorted((start, end)))


def full_graph_to_dot(edges):
    lines = [
        "graph G {",
        "layout=dot;",
        "rankdir=LR;",
        'node [shape=box, style="rounded,filled", fillcolor="#EAF2FF", color="#0259DD", fontname="Arial", fontsize=10];',
        'edge [color="#84AFFB", fontname="Arial", fontsize=9];'
    ]

    for start, end, weight in edges:
        start_name = NODE_NAMES[start]
        end_name = NODE_NAMES[end]
        lines.append(
            f'"{start_name}" -- "{end_name}" [label="{weight}"];'
        )

    lines.append("}")
    return "\n".join(lines)


def graph_with_route_to_dot(edges, route=None, closed_edge=None):
    if route is None:
        route = []

    route_edges = set()
    for index in range(len(route) - 1):
        route_edges.add(_edge_key(route[index], route[index + 1]))

    closed_key = None
    if closed_edge is not None:
        closed_key = _edge_key(closed_edge[0], closed_edge[1])

    lines = [
        "graph G {",
        "layout=dot;",
        "rankdir=LR;",
        'node [shape=box, style="rounded,filled", fillcolor="#EAF2FF", color="#0259DD", fontname="Arial", fontsize=10];',
        'edge [fontname="Arial", fontsize=9];'
    ]

    for start, end, weight in edges:
        key = _edge_key(start, end)
        start_name = NODE_NAMES[start]
        end_name = NODE_NAMES[end]

        attributes = [f'label="{weight}"', 'color="#84AFFB"', 'penwidth="1.4"']

        if key in route_edges:
            attributes = [f'label="{weight}"', 'color="#FF6648"', 'penwidth="3.2"']

        if closed_key is not None and key == closed_key:
            attributes = [f'label="{weight} ditutup"', 'color="#991B1B"', 'penwidth="3.2"', 'style="dashed"']

        lines.append(
            f'"{start_name}" -- "{end_name}" [{", ".join(attributes)}];'
        )

    lines.append("}")
    return "\n".join(lines)


def route_to_dot(route):
    if len(route) <= 1:
        return "digraph G { }"

    lines = [
        "digraph G {",
        "rankdir=LR;",
        'node [shape=box, style="rounded,filled", fillcolor="#FFE1D7", color="#0259DD", fontname="Arial"];',
        'edge [color="#FF6648", penwidth=2, fontname="Arial"];'
    ]

    for index, node in enumerate(route):
        node_id = f"step_{index}"
        node_name = NODE_NAMES[node]
        lines.append(
            f'{node_id} [label="{index}. {node_name}"];'
        )

    for index in range(len(route) - 1):
        lines.append(
            f"step_{index} -> step_{index + 1};"
        )

    lines.append("}")
    return "\n".join(lines)


def route_to_dot_partial(route, active_step):
    if len(route) <= 1:
        return "digraph G { }"

    active_step = max(0, min(active_step, len(route) - 1))

    lines = [
        "digraph G {",
        "rankdir=LR;",
        'node [shape=box, style="rounded,filled", color="#0259DD", fontname="Arial"];',
        'edge [fontname="Arial"];'
    ]

    for index, node in enumerate(route):
        node_name = NODE_NAMES[node]

        if index < active_step:
            fill_color = "#EAF2FF"
            border_color = "#0259DD"
        elif index == active_step:
            fill_color = "#FFE1D7"
            border_color = "#FF6648"
        else:
            fill_color = "#F8FAFC"
            border_color = "#CBD5E1"

        lines.append(
            f'step_{index} [label="{index}. {node_name}", fillcolor="{fill_color}", color="{border_color}"];'
        )

    for index in range(len(route) - 1):
        if index < active_step:
            edge_color = "#FF6648"
            pen_width = "3"
        else:
            edge_color = "#CBD5E1"
            pen_width = "1.5"

        lines.append(
            f'step_{index} -> step_{index + 1} [color="{edge_color}", penwidth="{pen_width}"];'
        )

    lines.append("}")
    return "\n".join(lines)


if __name__ == "__main__":
    matrix = build_adjacency_matrix(NUM_NODES, EDGES)
    info = get_graph_info(EDGES)

    print("Informasi Graf RouteWise")
    print(f"Jumlah node : {info['jumlah_node']}")
    print(f"Jumlah edge : {info['jumlah_edge']}")
    print(f"Total bobot : {info['total_bobot']}")
    print(f"Rata-rata   : {info['rata_rata_bobot']}")

    print("\nTetangga Gudang Pusat:")
    for neighbor, weight in get_neighbors(matrix, 0):
        print(f"- {NODE_NAMES[neighbor]} ({weight})")
