from dijkstra import get_shortest_path_and_distance


def seleksi_greedy(total_berat, daftar_kendaraan):
    # Mengurutkan kendaraan dari kapasitas terkecil agar kendaraan yang dipilih paling efisien
    kendaraan_urut = sorted(
        daftar_kendaraan,
        key=lambda kendaraan: kendaraan.kapasitas
    )

    for kendaraan in kendaraan_urut:
        if total_berat <= kendaraan.kapasitas:
            return kendaraan

    return None


def merge_path(route, new_path):
    if not new_path:
        return route

    if not route:
        return new_path[:]

    if route[-1] == new_path[0]:
        return route + new_path[1:]

    return route + new_path


def calculate_route_for_order(matrix, ordered_packages, node_names, start_node=0):
    current_node = start_node
    total_distance = 0
    full_route = [start_node]
    delivery_rows = []
    failed_rows = []

    for index, package in enumerate(ordered_packages, start=1):
        path_to_origin, distance_to_origin = get_shortest_path_and_distance(
            matrix,
            current_node,
            package["origin"]
        )

        path_to_destination, distance_to_destination = get_shortest_path_and_distance(
            matrix,
            package["origin"],
            package["destination"]
        )

        if distance_to_origin == float("inf") or distance_to_destination == float("inf"):
            failed_rows.append({
                "ID Paket": package["id"],
                "Asal": node_names[package["origin"]],
                "Tujuan": node_names[package["destination"]],
                "Alasan": "Node asal/tujuan tidak dapat dijangkau"
            })
            continue

        added_distance = distance_to_origin + distance_to_destination
        total_distance += added_distance

        full_route = merge_path(full_route, path_to_origin)
        full_route = merge_path(full_route, path_to_destination)

        deadline_status = "Memenuhi" if total_distance <= package["deadline"] else "Melewati deadline"

        delivery_rows.append({
            "Urutan": index,
            "ID Paket": package["id"],
            "Asal": node_names[package["origin"]],
            "Tujuan": node_names[package["destination"]],
            "Prioritas": package["priority"],
            "Volume": package["volume"],
            "Deadline": package["deadline"],
            "Jarak Tambahan": added_distance,
            "Jarak Kumulatif": total_distance,
            "Status Deadline": deadline_status
        })

        current_node = package["destination"]

    return {
        "route": full_route,
        "total_distance": total_distance,
        "delivery_rows": delivery_rows,
        "failed_rows": failed_rows
    }


def greedy_order(matrix, packages, node_names, start_node=0):
    if not packages:
        return []

    remaining = packages[:]
    ordered = []
    current_node = start_node

    max_priority = max(package["priority"] for package in packages)
    max_deadline = max(package["deadline"] for package in packages)

    while remaining:
        candidates = []

        for package in remaining:
            _, distance_to_origin = get_shortest_path_and_distance(
                matrix,
                current_node,
                package["origin"]
            )

            _, distance_to_destination = get_shortest_path_and_distance(
                matrix,
                package["origin"],
                package["destination"]
            )

            if distance_to_origin == float("inf") or distance_to_destination == float("inf"):
                continue

            added_distance = distance_to_origin + distance_to_destination

            priority_score = package["priority"] / max_priority
            distance_score = 1 / (1 + added_distance)
            deadline_score = (max_deadline - package["deadline"] + 1) / max_deadline

            score = (
                0.55 * priority_score
                + 0.30 * distance_score
                + 0.15 * deadline_score
            )

            candidates.append((score, -added_distance, -package["deadline"], package))

        if not candidates:
            break

        candidates.sort(reverse=True, key=lambda item: (item[0], item[1], item[2]))
        best_package = candidates[0][3]

        ordered.append(best_package)
        current_node = best_package["destination"]
        remaining.remove(best_package)

    return ordered


def priority_order(packages):
    return sorted(
        packages,
        key=lambda package: (
            -package["priority"],
            package["deadline"],
            package["volume"]
        )
    )


def deadline_order(packages):
    return sorted(
        packages,
        key=lambda package: (
            package["deadline"],
            -package["priority"],
            package["volume"]
        )
    )


def distance_based_order(matrix, packages, start_node=0):
    remaining = packages[:]
    ordered = []
    current_node = start_node

    while remaining:
        best_package = None
        best_distance = float("inf")

        for package in remaining:
            _, distance_to_origin = get_shortest_path_and_distance(
                matrix,
                current_node,
                package["origin"]
            )

            _, distance_to_destination = get_shortest_path_and_distance(
                matrix,
                package["origin"],
                package["destination"]
            )

            added_distance = distance_to_origin + distance_to_destination

            if added_distance < best_distance:
                best_distance = added_distance
                best_package = package

        if best_package is None:
            break

        ordered.append(best_package)
        current_node = best_package["destination"]
        remaining.remove(best_package)

    return ordered


def get_route_alternatives(matrix, selected_packages, start_node=0):
    from data import NODE_NAMES

    alternatives = [
        (
            "Greedy gabungan priority + jarak + deadline",
            greedy_order(matrix, selected_packages, NODE_NAMES, start_node)
        ),
        (
            "Prioritas tertinggi dulu",
            priority_order(selected_packages)
        ),
        (
            "Deadline tercepat dulu",
            deadline_order(selected_packages)
        ),
        (
            "Jarak terdekat bertahap",
            distance_based_order(matrix, selected_packages, start_node)
        ),
    ]

    route_results = []

    for route_name, ordered_packages in alternatives:
        route_result = calculate_route_for_order(
            matrix,
            ordered_packages,
            NODE_NAMES,
            start_node
        )

        route_results.append({
            "name": route_name,
            "ordered_packages": ordered_packages,
            "result": route_result
        })

    return route_results


def get_best_route(route_results):
    return min(
        route_results,
        key=lambda item: item["result"]["total_distance"]
    )
