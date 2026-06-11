from dijkstra import get_shortest_path_and_distance


def seleksi_greedy(total_berat, daftar_kendaraan):
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


def path_to_text(path, node_names):
    if not path:
        return "Tidak ada rute"
    return " -> ".join(node_names[node] for node in path)


def calculate_route_for_order(matrix, ordered_packages, node_names, start_node=0):
    current_node = start_node
    total_distance = 0
    full_route = [start_node]
    delivery_rows = []
    failed_rows = []

    for index, package in enumerate(ordered_packages, start=1):
        previous_position = current_node

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
            "Posisi Awal Kurir": node_names[previous_position],
            "Asal": node_names[package["origin"]],
            "Tujuan": node_names[package["destination"]],
            "Rute Dijkstra ke Asal": path_to_text(path_to_origin, node_names),
            "Jarak ke Asal": distance_to_origin,
            "Rute Dijkstra ke Tujuan": path_to_text(path_to_destination, node_names),
            "Jarak ke Tujuan": distance_to_destination,
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


def build_candidate_ranking(matrix, remaining_packages, node_names, current_node, iteration, max_priority, max_deadline):
    candidates = []

    for package in remaining_packages:
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
            candidates.append({
                "Iterasi": iteration,
                "ID Paket": package["id"],
                "Posisi Kurir": node_names[current_node],
                "Asal": node_names[package["origin"]],
                "Tujuan": node_names[package["destination"]],
                "Rute ke Asal": "Tidak ada rute",
                "Jarak ke Asal": "∞",
                "Rute ke Tujuan": "Tidak ada rute",
                "Jarak ke Tujuan": "∞",
                "Jarak Tambahan": "∞",
                "Prioritas": package["priority"],
                "Deadline": package["deadline"],
                "Score Prioritas": 0,
                "Score Jarak": 0,
                "Score Deadline": 0,
                "Score Akhir": 0,
                "Dipilih": "Tidak"
            })
            continue

        added_distance = distance_to_origin + distance_to_destination
        priority_score = package["priority"] / max_priority if max_priority else 0
        distance_score = 1 / (1 + added_distance)
        deadline_score = (max_deadline - package["deadline"] + 1) / max_deadline if max_deadline else 0

        final_score = (
            0.55 * priority_score
            + 0.30 * distance_score
            + 0.15 * deadline_score
        )

        candidates.append({
            "Iterasi": iteration,
            "ID Paket": package["id"],
            "Posisi Kurir": node_names[current_node],
            "Asal": node_names[package["origin"]],
            "Tujuan": node_names[package["destination"]],
            "Rute ke Asal": path_to_text(path_to_origin, node_names),
            "Jarak ke Asal": distance_to_origin,
            "Rute ke Tujuan": path_to_text(path_to_destination, node_names),
            "Jarak ke Tujuan": distance_to_destination,
            "Jarak Tambahan": added_distance,
            "Prioritas": package["priority"],
            "Deadline": package["deadline"],
            "Score Prioritas": round(priority_score, 4),
            "Score Jarak": round(distance_score, 4),
            "Score Deadline": round(deadline_score, 4),
            "Score Akhir": round(final_score, 4),
            "Dipilih": "Tidak",
            "_package": package,
            "_sort_key": (final_score, -added_distance, -package["deadline"])
        })

    valid_candidates = [candidate for candidate in candidates if "_package" in candidate]
    valid_candidates.sort(reverse=True, key=lambda candidate: candidate["_sort_key"])

    if valid_candidates:
        selected_id = valid_candidates[0]["ID Paket"]
        for candidate in candidates:
            if candidate["ID Paket"] == selected_id:
                candidate["Dipilih"] = "Ya"

    clean_candidates = []
    for candidate in candidates:
        clean_candidate = {
            key: value
            for key, value in candidate.items()
            if not key.startswith("_")
        }
        clean_candidates.append(clean_candidate)

    selected_package = valid_candidates[0]["_package"] if valid_candidates else None
    return clean_candidates, selected_package


def greedy_order_with_details(matrix, packages, node_names, start_node=0):
    if not packages:
        return [], []

    remaining = packages[:]
    ordered = []
    candidate_rankings = []
    current_node = start_node
    iteration = 1

    max_priority = max(package["priority"] for package in packages)
    max_deadline = max(package["deadline"] for package in packages)

    while remaining:
        ranking_rows, best_package = build_candidate_ranking(
            matrix,
            remaining,
            node_names,
            current_node,
            iteration,
            max_priority,
            max_deadline
        )

        candidate_rankings.extend(ranking_rows)

        if best_package is None:
            break

        ordered.append(best_package)
        current_node = best_package["destination"]
        remaining.remove(best_package)
        iteration += 1

    return ordered, candidate_rankings


def greedy_order(matrix, packages, node_names, start_node=0):
    ordered, _ = greedy_order_with_details(
        matrix,
        packages,
        node_names,
        start_node
    )
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

    greedy_packages, candidate_rankings = greedy_order_with_details(
        matrix,
        selected_packages,
        NODE_NAMES,
        start_node
    )

    alternatives = [
        (
            "Greedy gabungan priority + jarak Dijkstra + deadline",
            greedy_packages,
            candidate_rankings
        ),
        (
            "Prioritas tertinggi dulu",
            priority_order(selected_packages),
            []
        ),
        (
            "Deadline tercepat dulu",
            deadline_order(selected_packages),
            []
        ),
        (
            "Jarak Dijkstra terdekat bertahap",
            distance_based_order(matrix, selected_packages, start_node),
            []
        ),
    ]

    route_results = []

    for route_name, ordered_packages, ranking_rows in alternatives:
        route_result = calculate_route_for_order(
            matrix,
            ordered_packages,
            NODE_NAMES,
            start_node
        )

        route_results.append({
            "name": route_name,
            "ordered_packages": ordered_packages,
            "candidate_rankings": ranking_rows,
            "result": route_result
        })

    return route_results


def get_best_route(route_results):
    return min(
        route_results,
        key=lambda item: (
            -len(item["result"]["delivery_rows"]),
            len(item["result"]["failed_rows"]),
            item["result"]["total_distance"]
        )
    )
