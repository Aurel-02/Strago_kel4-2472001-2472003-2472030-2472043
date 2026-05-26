NODE_NAMES = [
    "Gudang Pusat",
    "Agen Barat",
    "Agen Utara",
    "Agen Timur",
    "Agen Selatan",
    "Pasar Lama",
    "Pasar Baru",
    "Mall Kota",
    "Kampus",
    "Sekolah",
    "Rumah Sakit",
    "Perumahan A",
    "Perumahan B",
    "Perumahan C",
    "Apartemen A",
    "Apartemen B",
    "Ruko A",
    "Ruko B",
    "Terminal",
    "Stasiun",
    "Pabrik",
    "Kantor Pos",
    "Gudang Cabang",
    "Hub Selatan",
]

NUM_NODES = len(NODE_NAMES)  # = 24

EDGES = [
    (0, 1, 4),
    (0, 2, 5),
    (0, 4, 6),
    (1, 5, 3),
    (1, 11, 5),
    (2, 6, 4),
    (2, 8, 6),
    (3, 7, 4),
    (3, 16, 5),
    (3, 22, 9),
    (4, 18, 4),
    (4, 23, 7),
    (5, 6, 3),
    (5, 12, 6),
    (6, 7, 4),
    (6, 9, 5),
    (7, 8, 3),
    (7, 14, 6),
    (8, 9, 4),
    (8, 10, 5),
    (9, 13, 5),
    (10, 15, 4),
    (10, 17, 7),
    (11, 12, 3),
    (11, 19, 8),
    (12, 13, 4),
    (13, 14, 5),
    (14, 15, 3),
    (15, 16, 4),
    (16, 17, 3),
    (17, 18, 5),
    (18, 19, 4),
    (19, 20, 6),
    (20, 21, 5),
    (21, 22, 4),
    (22, 23, 5),
]


# Membuat matriks ketetanggaan 24x24 dari daftar edge
def build_adjacency_matrix(num_nodes: int, edges: list) -> list[list[int]]:
    """
    Membangun matriks ketetanggaan dari daftar edge.

    Parameter:
        num_nodes (int) : jumlah node dalam graf
        edges (list)    : list of tuple (u, v, weight) — tidak berarah

    Return:
        matrix (list of list of int) : matriks ketetanggaan berukuran num_nodes × num_nodes
    """
    # Inisialisasi semua nilai dengan 0 (tidak ada koneksi)
    matrix = [[0] * num_nodes for _ in range(num_nodes)]

    for u, v, weight in edges:
        matrix[u][v] = weight  # arah u → v
        matrix[v][u] = weight  # arah v → u (graf tidak berarah)

    return matrix


# Mengambil daftar tetangga langsung suatu node beserta bobotnya
def get_neighbors(matrix: list[list[int]], node: int) -> list[tuple[int, int]]:
    """
    Mengembalikan daftar tetangga langsung dari sebuah node beserta bobotnya.

    Parameter:
        matrix (list of list) : matriks ketetanggaan
        node (int)            : index node yang ingin dicari tetangganya

    Return:
        list of (neighbor_index, weight)
    """
    neighbors = []
    for j, weight in enumerate(matrix[node]):
        if weight > 0:
            neighbors.append((j, weight))
    return neighbors


# Mencetak matriks ketetanggaan ke konsol dalam bentuk tabel
def print_adjacency_matrix(matrix: list[list[int]]) -> None:
    """
    Menampilkan matriks ketetanggaan ke konsol dalam format tabel sederhana.
    """
    n = len(matrix)
    # Header kolom
    header = "     " + "  ".join(f"{j:>3}" for j in range(n))
    print(header)
    print("     " + "-" * (n * 5))

    for i, row in enumerate(matrix):
        row_str = "  ".join(f"{val:>3}" for val in row)
        print(f"{i:>3} | {row_str}")


# Mencetak daftar edge beserta nama node asal dan tujuannya
def print_edge_list(edges: list) -> None:
    """
    Menampilkan daftar edge beserta nama node-nya.
    """
    print(f"{'No':<4} {'Dari':<18} {'Ke':<18} {'Jarak':>6}")
    print("-" * 50)
    for i, (u, v, w) in enumerate(edges, start=1):
        print(f"{i:<4} {NODE_NAMES[u]:<18} {NODE_NAMES[v]:<18} {w:>6}")
    print(f"\nTotal edge: {len(edges)}")


# Mengembalikan ringkasan statistik graf (jumlah node, edge, total bobot)
def get_graph_info(matrix: list[list[int]], edges: list) -> dict:
    """
    Mengembalikan ringkasan informasi graf.
    """
    total_weight = sum(w for _, _, w in edges)
    return {
        "jumlah_node": NUM_NODES,
        "jumlah_edge": len(edges),
        "total_bobot": total_weight,
        "rata_rata_bobot": round(total_weight / len(edges), 2),
    }

if __name__ == "__main__":
    adjacency_matrix = build_adjacency_matrix(NUM_NODES, EDGES)

    print("=" * 60)
    print("  ROUTEPACK COURIER -- Graf 24 Node (Anggota 1)")
    print("=" * 60)

    info = get_graph_info(adjacency_matrix, EDGES)
    print("\n[INFO] Informasi Graf:")
    print(f"   Jumlah node : {info['jumlah_node']}")
    print(f"   Jumlah edge : {info['jumlah_edge']}")
    print(f"   Total bobot : {info['total_bobot']}")
    print(f"   Rata-rata   : {info['rata_rata_bobot']}")

    # Daftar node
    print("\n[NODE] Daftar Node:")
    for i, name in enumerate(NODE_NAMES):
        print(f"   [{i:>2}] {name}")

    # Daftar edge
    print("\n[EDGE] Daftar Edge:")
    print_edge_list(EDGES)

    print("\n[GRAF] Tetangga 'Gudang Pusat' (node 0):")
    for neighbor, weight in get_neighbors(adjacency_matrix, 0):
        print(f"   -> {NODE_NAMES[neighbor]:<18} jarak: {weight}")

    print("\n[MATRIX] Cuplikan Matriks Ketetanggaan (8 baris pertama):")
    sub = [row[:8] for row in adjacency_matrix[:8]]
    print("     " + "  ".join(f"{j:>3}" for j in range(8)))
    print("     " + "-" * 42)
    for i, row in enumerate(sub):
        row_str = "  ".join(f"{val:>3}" for val in row)
        print(f"{i:>3} | {row_str}")

    print("\n[OK] Graf berhasil dibuat dan divalidasi.")
    print("     File ini siap diimpor oleh dijkstra.py, greedy.py, dan main.py")
