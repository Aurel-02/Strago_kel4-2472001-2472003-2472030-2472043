from kendaraan import daftar_kendaraan
from paket import checklist_paket
from greedy import seleksi_greedy

from graph import (
    build_adjacency_matrix,
    NUM_NODES,
    EDGES,
    NODE_NAMES
)

from dijkstra import get_shortest_path_and_distance


print("\n=====================================")
print("      SISTEM PENGIRIMAN STRAGO")
print("=====================================")

# bikin graf
matrix = build_adjacency_matrix(NUM_NODES, EDGES)

# Titik awal dan tujuan
start_node = 0      # Gudang Pusat
target_node = 23    # Hub Selatan


# djikstra
path, jarak = get_shortest_path_and_distance(
    matrix,
    start_node,
    target_node
)

# checklist paket
total_berat = checklist_paket()


# seleksi greedy
kendaraan_terpilih = seleksi_greedy(
    total_berat,
    daftar_kendaraan
)

# tampilkan jalur
print("\n========== JALUR PENGIRIMAN ==========")

if jarak != float('inf'):

    path_names = [NODE_NAMES[node] for node in path]

    print(" -> ".join(path_names))
    print(f"Total Jarak : {jarak} km")

else:

    print("Jalur tidak ditemukan")


# tampilkan kendaraan
print("\n========== HASIL GREEDY ==========")

if kendaraan_terpilih:

    kendaraan_terpilih.tampilkan_info()

    total_biaya = jarak * kendaraan_terpilih.biaya_per_km

    print(f"Estimasi Biaya : Rp{total_biaya}")

else:

    print("Tidak ada kendaraan yang tersedia")