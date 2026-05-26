import pandas as pd
import streamlit as st

from data import DEFAULT_EDGES, DEFAULT_PACKAGES, NODE_NAMES, VEHICLES
from graph import (
    NUM_NODES,
    build_adjacency_matrix,
    full_graph_to_dot,
    route_to_dot,
    route_to_text
)
from greedy import get_route_alternatives, get_best_route


def setup_page():
    st.set_page_config(
        page_title="RouteWise",
        page_icon="📦",
        layout="wide"
    )

    st.markdown(
        """
        <style>
        .main-title {
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 0px;
        }

        .subtitle {
            color: #666;
            font-size: 17px;
            margin-top: 0px;
            margin-bottom: 25px;
        }

        .card {
            padding: 18px;
            border-radius: 16px;
            background-color: #f8fafc;
            border: 1px solid #e5e7eb;
            margin-bottom: 15px;
        }

        .success-card {
            padding: 16px;
            border-radius: 14px;
            background-color: #ecfdf5;
            border: 1px solid #86efac;
            color: #166534;
            margin-bottom: 15px;
        }

        .warning-card {
            padding: 16px;
            border-radius: 14px;
            background-color: #fffbeb;
            border: 1px solid #facc15;
            color: #854d0e;
            margin-bottom: 15px;
        }

        .danger-card {
            padding: 16px;
            border-radius: 14px;
            background-color: #fef2f2;
            border: 1px solid #fca5a5;
            color: #991b1b;
            margin-bottom: 15px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">RouteWise</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Aplikasi rekomendasi rute pengiriman paket menggunakan Dijkstra dan strategi Greedy.</div>',
        unsafe_allow_html=True
    )


def get_vehicle_detail(vehicle):
    vehicle_data = VEHICLES[vehicle]

    if isinstance(vehicle_data, dict):
        vehicle_name = vehicle_data.get("name", vehicle)
        capacity = vehicle_data.get("capacity", 0)
        description = vehicle_data.get("description", "-")
    else:
        vehicle_name = vehicle
        capacity = vehicle_data
        description = "-"

    return vehicle_name, capacity, description


def get_next_package_id(packages):
    numbers = []

    for package in packages:
        package_id = str(package["id"]).upper().strip()

        if package_id.startswith("P") and package_id[1:].isdigit():
            numbers.append(int(package_id[1:]))

    return f"P{max(numbers, default=0) + 1:03d}"


def find_duplicate_ids(packages):
    ids = [str(package["id"]).upper().strip() for package in packages]
    duplicates = sorted(
        set(package_id for package_id in ids if ids.count(package_id) > 1)
    )

    return duplicates


def packages_to_dataframe(packages):
    rows = []

    for package in packages:
        rows.append({
            "Pilih": bool(package.get("selected", False)),
            "ID Paket": package["id"],
            "Asal": NODE_NAMES[package["origin"]],
            "Tujuan": NODE_NAMES[package["destination"]],
            "Prioritas": package["priority"],
            "Volume": package["volume"],
            "Deadline": package["deadline"]
        })

    return pd.DataFrame(rows)


def dataframe_to_packages(dataframe):
    name_to_index = {
        name: index for index, name in enumerate(NODE_NAMES)
    }

    converted_packages = []

    for _, row in dataframe.iterrows():
        package_id = str(row["ID Paket"]).upper().strip()
        origin_name = row["Asal"]
        destination_name = row["Tujuan"]

        if not package_id:
            continue

        if origin_name not in name_to_index:
            continue

        if destination_name not in name_to_index:
            continue

        converted_packages.append({
            "selected": bool(row["Pilih"]),
            "id": package_id,
            "origin": name_to_index[origin_name],
            "destination": name_to_index[destination_name],
            "priority": int(row["Prioritas"]),
            "volume": int(row["Volume"]),
            "deadline": int(row["Deadline"])
        })

    return converted_packages


def go_to_result_page():
    st.session_state.nav_page = "Hasil Rute"


def init_session_state():
    if "packages" not in st.session_state:
        st.session_state.packages = [
            package.copy() for package in DEFAULT_PACKAGES
        ]

    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "Input Paket"


def render_sidebar():
    st.sidebar.header("Pengaturan Pengiriman")

    vehicle = st.sidebar.selectbox(
        "Pilih kendaraan",
        list(VEHICLES.keys())
    )

    vehicle_name, capacity, description = get_vehicle_detail(vehicle)

    start_location = st.sidebar.selectbox(
        "Titik awal kurir",
        NODE_NAMES,
        index=0
    )

    start_node = NODE_NAMES.index(start_location)

    st.sidebar.markdown(
        f"""
        <div class="card">
            <b>Jenis Kendaraan:</b> {vehicle}<br>
            <b>Nama Kendaraan:</b> {vehicle_name}<br>
            <b>Kapasitas:</b> {capacity} unit<br>
            <b>Titik awal:</b> {start_location}<br>
            <b>Keterangan:</b> {description}
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar.expander("Tambah Paket Manual"):
        with st.form("add_package_form"):
            new_id = st.text_input(
                "ID Paket",
                value=get_next_package_id(st.session_state.packages),
                disabled=True
            )

            new_origin = st.selectbox(
                "Asal",
                NODE_NAMES,
                key="new_origin"
            )

            new_destination = st.selectbox(
                "Tujuan",
                NODE_NAMES,
                key="new_destination"
            )

            new_priority = st.slider(
                "Prioritas",
                1,
                5,
                3
            )

            new_volume = st.number_input(
                "Volume",
                min_value=1,
                max_value=100,
                value=10
            )

            new_deadline = st.number_input(
                "Deadline",
                min_value=1,
                max_value=200,
                value=40
            )

            submitted = st.form_submit_button("Tambah Paket")

            if submitted:
                if NODE_NAMES.index(new_origin) == NODE_NAMES.index(new_destination):
                    st.error("Asal dan tujuan tidak boleh sama.")
                else:
                    st.session_state.packages.append({
                        "selected": False,
                        "id": new_id,
                        "origin": NODE_NAMES.index(new_origin),
                        "destination": NODE_NAMES.index(new_destination),
                        "priority": new_priority,
                        "volume": int(new_volume),
                        "deadline": int(new_deadline)
                    })

                    st.success("Paket berhasil ditambahkan.")
                    st.rerun()

        if st.button("Reset paket ke data awal"):
            st.session_state.packages = [
                package.copy() for package in DEFAULT_PACKAGES
            ]

            st.rerun()

    return vehicle, vehicle_name, capacity, start_node


def render_input_page(vehicle, capacity):
    st.subheader("Daftar Paket")

    st.write(
        "Centang paket yang ingin dibawa. Data paket bisa diedit, tetapi ID Paket dikunci agar tidak dobel."
    )

    package_df = packages_to_dataframe(st.session_state.packages)

    edited_df = st.data_editor(
        package_df,
        use_container_width=True,
        hide_index=True,
        disabled=["ID Paket"],
        column_config={
            "Pilih": st.column_config.CheckboxColumn("Pilih"),
            "Asal": st.column_config.SelectboxColumn(
                "Asal",
                options=NODE_NAMES
            ),
            "Tujuan": st.column_config.SelectboxColumn(
                "Tujuan",
                options=NODE_NAMES
            ),
            "Prioritas": st.column_config.NumberColumn(
                "Prioritas",
                min_value=1,
                max_value=5
            ),
            "Volume": st.column_config.NumberColumn(
                "Volume",
                min_value=1,
                max_value=100
            ),
            "Deadline": st.column_config.NumberColumn(
                "Deadline",
                min_value=1,
                max_value=200
            ),
        },
        key="package_editor"
    )

    current_packages = dataframe_to_packages(edited_df)
    st.session_state.packages = current_packages

    duplicate_ids = find_duplicate_ids(current_packages)

    selected_packages = [
        package for package in current_packages
        if package["selected"]
    ]

    total_volume = sum(
        package["volume"] for package in selected_packages
    )

    remaining_capacity = capacity - total_volume

    if duplicate_ids:
        st.markdown(
            f"""
            <div class="danger-card">
                <b>ID Paket tidak valid.</b><br>
                ID berikut terdeteksi dobel: {", ".join(duplicate_ids)}.<br>
                Setiap paket harus memiliki ID yang unik.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("Status Kapasitas")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Kendaraan", vehicle)
    col2.metric("Kapasitas", f"{capacity} unit")
    col3.metric("Volume Terpilih", f"{total_volume} unit")
    col4.metric("Sisa Kapasitas", f"{remaining_capacity} unit")

    if not selected_packages:
        st.markdown(
            '<div class="warning-card"><b>Status:</b> Belum ada paket yang dipilih.</div>',
            unsafe_allow_html=True
        )
    elif total_volume <= capacity:
        st.markdown(
            '<div class="success-card"><b>Status:</b> Paket yang dipilih masih memenuhi kapasitas kendaraan.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="danger-card"><b>Status:</b> Paket yang dipilih melebihi kapasitas kendaraan.</div>',
            unsafe_allow_html=True
        )

    st.divider()

    st.button(
        "Hitung Rute",
        use_container_width=True,
        on_click=go_to_result_page,
        disabled=bool(duplicate_ids) or not selected_packages or total_volume > capacity
    )

    if duplicate_ids:
        st.caption("Tombol Hitung Rute nonaktif karena terdapat ID paket yang dobel.")
    elif not selected_packages:
        st.caption("Pilih minimal satu paket untuk menghitung rute.")
    elif total_volume > capacity:
        st.caption("Kurangi paket atau pilih kendaraan dengan kapasitas lebih besar.")
    else:
        st.caption("Klik Hitung Rute untuk langsung membuka bagian Hasil Rute.")


def render_graph_page():
    st.subheader("Peta Graf 24 Node")

    st.write(
        "Graf berikut menunjukkan hubungan antar lokasi dan bobot jarak antar node."
    )

    st.graphviz_chart(
        full_graph_to_dot(DEFAULT_EDGES),
        use_container_width=True
    )


def render_result_page(vehicle, vehicle_name, capacity, start_node):
    st.subheader("Hasil Perhitungan Rute")

    current_packages = st.session_state.packages

    duplicate_ids = find_duplicate_ids(current_packages)

    selected_packages = [
        package for package in current_packages
        if package["selected"]
    ]

    total_volume = sum(
        package["volume"] for package in selected_packages
    )

    remaining_capacity = capacity - total_volume

    if duplicate_ids:
        st.error("Tidak bisa menghitung rute karena ada ID paket yang dobel.")
        return

    if not selected_packages:
        st.info("Pilih paket terlebih dahulu pada bagian Input Paket.")
        return

    if total_volume > capacity:
        st.error(
            "Total volume paket melebihi kapasitas kendaraan. Kurangi paket atau pilih kendaraan dengan kapasitas lebih besar."
        )
        return

    matrix = build_adjacency_matrix(
        NUM_NODES,
        DEFAULT_EDGES
    )

    route_results = get_route_alternatives(
        matrix,
        selected_packages,
        start_node=start_node
    )

    best_route = get_best_route(route_results)

    fulfilled_rows = [
        row for row in best_route["result"]["delivery_rows"]
        if row["Status Deadline"] == "Memenuhi"
    ]

    deadline_failed = [
        row for row in best_route["result"]["delivery_rows"]
        if row["Status Deadline"] == "Melewati deadline"
    ]

    st.markdown(
        f"""
        <div class="success-card">
            <b>Jenis Kendaraan:</b> {vehicle}<br>
            <b>Nama Kendaraan:</b> {vehicle_name}<br>
            <b>Kapasitas:</b> {capacity} unit<br>
            <b>Rute Rekomendasi:</b> {best_route["name"]}<br>
            <b>Total Jarak:</b> {best_route["result"]["total_distance"]} km<br>
            <b>Paket Dipilih:</b> {len(selected_packages)} paket<br>
            <b>Paket Memenuhi Deadline:</b> {len(fulfilled_rows)} paket<br>
            <b>Catatan:</b> Rute ini adalah rute dengan jarak paling kecil dari alternatif yang dihitung.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Jarak",
        f'{best_route["result"]["total_distance"]} km'
    )

    col2.metric(
        "Paket Terpenuhi",
        f"{len(fulfilled_rows)} paket"
    )

    col3.metric(
        "Sisa Kapasitas",
        f"{remaining_capacity} unit"
    )

    st.subheader("Rute Rekomendasi")

    st.write(
        route_to_text(best_route["result"]["route"])
    )

    st.subheader("Peta Rute Rekomendasi")

    st.graphviz_chart(
        route_to_dot(best_route["result"]["route"]),
        use_container_width=True
    )

    st.subheader("Urutan Pengantaran")

    st.dataframe(
        pd.DataFrame(best_route["result"]["delivery_rows"]),
        use_container_width=True
    )

    st.subheader("Perbandingan Rute Alternatif")

    comparison_rows = []

    for item in route_results:
        comparison_rows.append({
            "Jenis Rute": item["name"],
            "Total Jarak": item["result"]["total_distance"],
            "Urutan Paket": " -> ".join(
                package["id"] for package in item["ordered_packages"]
            )
        })

    st.dataframe(
        pd.DataFrame(comparison_rows),
        use_container_width=True
    )

    st.subheader("Paket Terpenuhi")

    if fulfilled_rows:
        st.write(
            ", ".join(row["ID Paket"] for row in fulfilled_rows)
        )
    else:
        st.warning("Tidak ada paket yang memenuhi deadline.")

    st.subheader("Paket Gagal / Tidak Diangkut")

    selected_ids = {
        package["id"] for package in selected_packages
    }

    failed_rows = []

    for package in current_packages:
        if package["id"] not in selected_ids:
            failed_rows.append({
                "ID Paket": package["id"],
                "Asal": NODE_NAMES[package["origin"]],
                "Tujuan": NODE_NAMES[package["destination"]],
                "Alasan": "Tidak dipilih"
            })

    for row in deadline_failed:
        failed_rows.append({
            "ID Paket": row["ID Paket"],
            "Asal": row["Asal"],
            "Tujuan": row["Tujuan"],
            "Alasan": "Melewati deadline"
        })

    for row in best_route["result"]["failed_rows"]:
        failed_rows.append(row)

    if failed_rows:
        st.dataframe(
            pd.DataFrame(failed_rows),
            use_container_width=True
        )
    else:
        st.success("Tidak ada paket gagal.")


def run_app():
    setup_page()
    init_session_state()

    vehicle, vehicle_name, capacity, start_node = render_sidebar()

    pages = [
        "Input Paket",
        "Peta Graf",
        "Hasil Rute"
    ]

    page = st.radio(
        "Navigasi",
        pages,
        horizontal=True,
        key="nav_page",
        label_visibility="collapsed"
    )

    if page == "Input Paket":
        render_input_page(
            vehicle,
            capacity
        )

    elif page == "Peta Graf":
        render_graph_page()

    elif page == "Hasil Rute":
        render_result_page(
            vehicle,
            vehicle_name,
            capacity,
            start_node
        )