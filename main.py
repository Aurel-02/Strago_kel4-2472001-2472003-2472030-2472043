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

from dijkstra import get_shortest_path_with_steps


def tampilkan_daftar_node():
    print("\n========== DAFTAR NODE ==========")

    index = 0

    while (index < len(NODE_NAMES)):
        nama_node = NODE_NAMES[index]
        print(f"{index:2d}. {nama_node}")
        index = index + 1


def input_node(pesan):
    while (True):
        try:
            node = int(input(pesan))

            if (node < 0 or node >= NUM_NODES):
                print(f"Node tidak valid. Silakan coba dari 0-{NUM_NODES - 1}.")
                continue

            return node

        except ValueError:
            print("Input harus berupa angka. Silakan coba lagi.")


def input_titik_awal_dan_tujuan():
    while (True):
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

    index = 0

    while (index < len(daftar_kendaraan)):
        kendaraan = daftar_kendaraan[index]
        nomor = index + 1

        print(f"{nomor}. {kendaraan.jenis}")

        if (hasattr(kendaraan, "nama")):
            print(f"   Nama       : {kendaraan.nama}")

        print(f"   Kapasitas  : {kendaraan.kapasitas} unit")
        print(f"   Biaya/km   : Rp{kendaraan.biaya_per_km}")

        index = index + 1


def input_paket_manual():
    print("\n========== INPUT PAKET MANUAL ==========")
    print("Masukkan berat setiap paket.")
    print("Contoh: 10")

    while (True):
        try:
            jumlah_paket = int(input("\nMasukkan jumlah paket: "))

            if (jumlah_paket <= 0):
                print("Jumlah paket harus lebih dari 0.")
                continue

            break

        except ValueError:
            print("Input jumlah paket harus berupa angka.")

    total_berat = 0
    nomor_paket = 1

    while (nomor_paket <= jumlah_paket):
        id_paket = f"P{nomor_paket:03d}"

        print(f"\nPaket {id_paket}")

        try:
            berat = int(input("Masukkan berat paket: "))

            if (berat <= 0):
                print("Berat paket harus lebih dari 0.")
                continue

        except ValueError:
            print("Berat paket harus berupa angka.")
            continue

        print(f"Paket {id_paket} berhasil ditambahkan dengan berat {berat} unit.")

        total_berat = total_berat + berat
        nomor_paket = nomor_paket + 1

    print("\n-------------------------------------")
    print(f"Total Berat Paket : {total_berat} unit")
    print("-------------------------------------")

    return total_berat


def pilih_mode_paket():
    while (True):
        print("\n========== PILIH MODE PAKET ==========")
        print("1. Gunakan paket default")
        print("2. Input paket manual")

        pilihan = input("Pilih mode paket (1/2): ")
        pilihan = pilihan.strip()

        if (pilihan == "1"):
            return checklist_paket()

        elif (pilihan == "2"):
            return input_paket_manual()

        else:
            print("Pilihan tidak valid. Silakan pilih 1 atau 2.")


def pilih_kendaraan_manual(total_berat):
    while (True):
        tampilkan_daftar_kendaraan()

        try:
            pilihan = int(input("\nPilih nomor kendaraan: "))

            if (pilihan < 1 or pilihan > len(daftar_kendaraan)):
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
    while (True):
        print("\n========== PILIH MODE KENDARAAN ==========")
        print("1. Pilih kendaraan sendiri")
        print("2. Gunakan rekomendasi Greedy")

        pilihan = input("Pilih mode kendaraan (1/2): ")
        pilihan = pilihan.strip()
        if (pilihan == "1"):
            return pilih_kendaraan_manual(total_berat)
        elif (pilihan == "2"):
            kendaraan = seleksi_greedy(total_berat, daftar_kendaraan)
            if (kendaraan == None):
                print("Tidak ada kendaraan yang cukup untuk membawa total paket.")
                return None
            print("\nKendaraan dipilih berdasarkan rekomendasi Greedy.")
            return kendaraan
        else:
            print("Pilihan tidak valid. Silakan pilih 1 atau 2.")

def tampilkan_jejak_dijkstra(steps):
    print("\n========== JEJAK ITERASI DIJKSTRA ==========")
    print("Bagian ini menampilkan proses pemilihan node dan update jarak sementara.")
    for step in steps:
        print(f"\nIterasi {step['Iterasi']}")
        print(f"Node dipilih       : {step['Node Dipilih']}")
        print(f"Jarak node dipilih : {step['Jarak Node Dipilih']}")
        print(f"Update tetangga    : {step['Update Tetangga']}")
        print(f"Node terkunci      : {step['Node Terkunci']}")


def tanya_tampilkan_jejak_dijkstra():
    while (True):
        jawaban = input("\nTampilkan jejak iterasi Dijkstra? (ya/tidak): ")
        jawaban = jawaban.lower().strip()
        if (jawaban == "ya" or jawaban == "y"):
            return True
        elif (jawaban == "tidak" or jawaban == "t" or jawaban == "n"):
            return False
        else:
            print("Pilihan tidak valid. Silakan isi ya atau tidak.")

def tampilkan_rute_terpendek(path, jarak):
    if (jarak != float("inf")):
        path_names = []
        for node in path:
            nama_node = NODE_NAMES[node]
            path_names.append(nama_node)
        print("\nRute terpendek:")
        print(" -> ".join(path_names))
        print(f"Total Jarak : {jarak} km")
    else:
        print("\nJalur tidak ditemukan.")

def tampilkan_hasil_kendaraan(kendaraan_terpilih, jarak):
    print("\n========== KENDARAAN ==========")

    if (kendaraan_terpilih):
        kendaraan_terpilih.tampilkan_info()
        if (jarak != float("inf")):
            total_biaya = jarak * kendaraan_terpilih.biaya_per_km
            print(f"Estimasi Biaya : Rp{total_biaya}")
        else:
            print("Estimasi Biaya : Tidak dapat dihitung karena jalur tidak ditemukan.")
    else:
        print("Tidak ada kendaraan yang tersedia.")


def jalankan_program():
    print("\n=====================================")
    print("      SISTEM PENGIRIMAN STRAGO")
    print("=====================================")

    matrix = build_adjacency_matrix(NUM_NODES, EDGES)

    start_node, target_node = input_titik_awal_dan_tujuan()

    path, jarak, steps = get_shortest_path_with_steps(
        matrix,
        start_node,
        target_node
    )

    total_berat = pilih_mode_paket()
    kendaraan_terpilih = pilih_mode_kendaraan(total_berat)

    print("\n========== JALUR PENGIRIMAN ==========")
    print(f"Dari   : {NODE_NAMES[start_node]}")
    print(f"Tujuan : {NODE_NAMES[target_node]}")

    tampilkan_rute_terpendek(path, jarak)

    tampilkan_jejak = tanya_tampilkan_jejak_dijkstra()

    if (tampilkan_jejak):
        tampilkan_jejak_dijkstra(steps)
    else:
        print("\nJejak iterasi Dijkstra tidak ditampilkan.")

    tampilkan_hasil_kendaraan(kendaraan_terpilih, jarak)
    
if (__name__ == "__main__"):
    jalankan_program()