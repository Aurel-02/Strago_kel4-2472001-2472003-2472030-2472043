from kendaraan import daftar_kendaraan
from paket import checklist_paket
from greedy import seleksi_greedy
from graph import (
    build_adjacency_matrix,
    NUM_NODES,
    NODE_NAMES
)
try:
    from graph import EDGES
except ImportError:
    from data import DEFAULT_EDGES as EDGES
from dijkstra import get_shortest_path_and_distance

def tampilkan_daftar_node():
    print("\n========== DAFTAR NODE ==========")
    for index, nama_node in enumerate(NODE_NAMES):
        print(f"{index:2d}. {nama_node}")

def input_node(pesan):
    while True:
        try:
            node = int(input(pesan))
            if node < 0 or node >= NUM_NODES:
                print(f"Node tidak valid. Silakan coba dari 0-{NUM_NODES - 1}.")
                continue
            return node
        except ValueError:
            print("Input harus berupa angka. Silakan coba lagi.")

def input_titik_awal_dan_tujuan():
    while True:
        tampilkan_daftar_node()

        print("\nMasukkan titik awal dan tujuan pengiriman.")
        start_node = input_node(f"Titik awal (0-{NUM_NODES - 1}): ")
        target_node = input_node(f"Titik tujuan (0-{NUM_NODES - 1}): ")
        if (start_node == target_node):
            print("\nTitik awal dan titik tujuan tidak boleh sama. Silakan coba lagi.")
            continue
        return start_node, target_node

def tampilkan_daftar_kendaraan():
    print("\n========== DAFTAR KENDARAAN ==========")

    for index, kendaraan in enumerate(daftar_kendaraan, start=1):
        print(f"{index}. {kendaraan.jenis}")

        if hasattr(kendaraan, "nama"):
            print(f"   Nama       : {kendaraan.nama}")
        print(f"   Kapasitas  : {kendaraan.kapasitas} unit")
        print(f"   Biaya/km   : Rp{kendaraan.biaya_per_km}")

def pilih_kendaraan_manual(total_berat):
    while True:
        tampilkan_daftar_kendaraan()

        try:
            pilihan = int(input("\nPilih nomor kendaraan: "))
            if pilihan < 1 or pilihan > len(daftar_kendaraan):
                print(f"Pilihan tidak valid. Silakan pilih 1-{len(daftar_kendaraan)}.")
                continue
            kendaraan = daftar_kendaraan[pilihan - 1]
            if (total_berat > kendaraan.kapasitas):
                print(
                    f"\nKapasitas {kendaraan.jenis} tidak cukup. "
                    f"Total paket {total_berat} unit, "
                    f"kapasitas kendaraan {kendaraan.kapasitas} unit."
                )
                print("Silakan pilih kendaraan lain.")
                continue

            return kendaraan

        except ValueError:
            print("Input harus berupa angka. Silakan coba lagi.")


def pilih_mode_kendaraan(total_berat):
    while True:
        print("\n========== PILIH MODE KENDARAAN ==========")
        print("1. Pilih kendaraan sendiri")
        print("2. Gunakan rekomendasi Greedy")

        pilihan = input("Pilih mode (1/2): ")

        if pilihan == "1":
            return pilih_kendaraan_manual(total_berat)

        elif pilihan == "2":
            kendaraan = seleksi_greedy(total_berat, daftar_kendaraan)

            if kendaraan is None:
                print("Tidak ada kendaraan yang cukup untuk membawa total paket.")
                return None

            print("\nKendaraan dipilih berdasarkan rekomendasi Greedy.")
            return kendaraan

        else:
            print("Pilihan tidak valid. Silakan pilih 1 atau 2.")


print("\n=====================================")
print("      SISTEM PENGIRIMAN STRAGO")
print("=====================================")

matrix = build_adjacency_matrix(NUM_NODES, EDGES)

start_node, target_node = input_titik_awal_dan_tujuan()

path, jarak = get_shortest_path_and_distance(
    matrix,
    start_node,
    target_node
)

total_berat = checklist_paket()

kendaraan_terpilih = pilih_mode_kendaraan(total_berat)

print("\n========== JALUR PENGIRIMAN ==========")
print(f"Dari   : {NODE_NAMES[start_node]}")
print(f"Tujuan : {NODE_NAMES[target_node]}")

if jarak != float("inf"):
    path_names = [NODE_NAMES[node] for node in path]

    print("\nRute terpendek:")
    print(" -> ".join(path_names))
    print(f"Total Jarak : {jarak} km")
else:
    print("\nJalur tidak ditemukan.")


print("\n========== HASIL KENDARAAN ==========")

if kendaraan_terpilih:
    kendaraan_terpilih.tampilkan_info()

    if jarak != float("inf"):
        total_biaya = jarak * kendaraan_terpilih.biaya_per_km
        print(f"Estimasi Biaya : Rp{total_biaya}")
    else:
        print("Estimasi Biaya : Tidak dapat dihitung karena jalur tidak ditemukan.")
else:
    print("Tidak ada kendaraan yang tersedia.")