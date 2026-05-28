# UI Streamlit untuk RouteWise.

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


def setup_page() -> None:
    st.set_page_config(page_title="RouteWise", page_icon="📦", layout="wide")

    st.markdown(
        """
        <style>
        :root {
            --peach: #FFE1D7;
            --light-blue: #84AFFB;
            --strong-blue: #0259DD;
            --coral: #FF6648;
        }

        .stApp {
            background: linear-gradient(135deg, #FFF7F4 0%, #EAF2FF 55%, #FFE1D7 100%);
        }

        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            display: none;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        .block-container {
            padding-top: 0.8rem;
            padding-bottom: 1.5rem;
        }

        .main-title {
            font-size: 38px;
            font-weight: 900;
            color: var(--strong-blue);
            margin-bottom: 0px;
            letter-spacing: -0.8px;
        }

        .subtitle {
            color: #334155;
            font-size: 15px;
            margin-top: 3px;
            margin-bottom: 0px;
        }

        .brand-card {
            padding: 16px 22px;
            border-radius: 20px;
            background: linear-gradient(135deg, #FFE1D7 0%, #84AFFB 100%);
            border: 1px solid rgba(2, 89, 221, 0.18);
            box-shadow: 0 5px 16px rgba(2, 89, 221, 0.10);
            margin-bottom: 14px;
        }

        .card {
            padding: 18px;
            border-radius: 18px;
            background-color: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(2, 89, 221, 0.15);
            box-shadow: 0 6px 18px rgba(2, 89, 221, 0.08);
            margin-bottom: 15px;
        }

        .success-card {
            padding: 16px;
            border-radius: 16px;
            background-color: #EAF2FF;
            border-left: 8px solid var(--strong-blue);
            color: #0f172a;
            margin-bottom: 15px;
            box-shadow: 0 4px 14px rgba(2, 89, 221, 0.08);
        }

        .warning-card {
            padding: 16px;
            border-radius: 16px;
            background-color: #FFE1D7;
            border-left: 8px solid var(--coral);
            color: #7c2d12;
            margin-bottom: 15px;
        }

        .danger-card {
            padding: 16px;
            border-radius: 16px;
            background-color: #FFE1D7;
            border-left: 8px solid var(--coral);
            color: #991b1b;
            margin-bottom: 15px;
        }

        div.stButton > button {
            background-color: var(--strong-blue);
            color: white;
            border-radius: 14px;
            border: none;
            padding: 0.6rem 1rem;
            font-weight: 700;
        }

        div.stButton > button:hover {
            background-color: var(--coral);
            color: white;
            border: none;
        }

        [data-testid="stMetricValue"] {
            color: var(--strong-blue);
            font-weight: 800;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="brand-card">
            <div class="main-title">RouteWise</div>
            <div class="subtitle">
                Dashboard rekomendasi rute pengiriman paket menggunakan Dijkstra dan strategi Greedy.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_vehicle_detail(vehicle: str) -> tuple[str, int, str]:
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


def get_next_package_id(packages: list[dict]) -> str:
    numbers = []

    for package in packages:
        package_id = str(package["id"]).upper().strip()

        if package_id.startswith("P") and package_id[1:].isdigit():
            numbers.append(int(package_id[1:]))

    return f"P{max(numbers, default=0) + 1:03d}"


def find_duplicate_ids(packages: list[dict]) -> list[str]:
    ids = [str(package["id"]).upper().strip() for package in packages]
    return sorted(set(package_id for package_id in ids if ids.count(package_id) > 1))


def packages_to_dataframe(packages: list[dict]) -> pd.DataFrame:
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


def dataframe_to_packages(dataframe: pd.DataFrame) -> list[dict]:
    name_to_index = {name: index for index, name in enumerate(NODE_NAMES)}
    converted_packages = []

    for _, row in dataframe.iterrows():
        package_id = str(row["ID Paket"]).upper().strip()
        origin_name = row["Asal"]
        destination_name = row["Tujuan"]

        if not package_id:
            continue

        if origin_name not in name_to_index or destination_name not in name_to_index:
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


def edges_to_dataframe(edges: list[tuple[int, int, int]]) -> pd.DataFrame:
    rows = []

    for start, end, weight in edges:
        rows.append({
            "Dari": NODE_NAMES[start],
            "Ke": NODE_NAMES[end],
            "Jarak": weight
        })

    return pd.DataFrame(rows)


def dataframe_to_edges(dataframe: pd.DataFrame) -> list[tuple[int, int, int]]:
    name_to_index = {name: index for index, name in enumerate(NODE_NAMES)}
    edges = []
    seen = set()

    for _, row in dataframe.iterrows():
        start_name = row["Dari"]
        end_name = row["Ke"]

        if start_name not in name_to_index or end_name not in name_to_index:
            continue

        start = name_to_index[start_name]
        end = name_to_index[end_name]

        if start == end:
            continue

        try:
            weight = int(row["Jarak"])
        except ValueError:
            continue

        if weight <= 0:
            continue

        edge_key = tuple(sorted((start, end)))

        if edge_key in seen:
            continue

        seen.add(edge_key)
        edges.append((start, end, weight))

    return edges


def go_to_result_page() -> None:
    st.session_state.nav_page = "Hasil Rute"


def init_session_state() -> None:
    if "packages" not in st.session_state:
        st.session_state.packages = [package.copy() for package in DEFAULT_PACKAGES]

    if "edges" not in st.session_state:
        st.session_state.edges = DEFAULT_EDGES[:]

    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "Input Paket"


def render_sidebar() -> tuple[str, str, int, str, int]:
    st.sidebar.header("Pengaturan Pengiriman")

    vehicle = st.sidebar.selectbox("Pilih kendaraan", list(VEHICLES.keys()))
    vehicle_name, capacity, vehicle_description = get_vehicle_detail(vehicle)

    start_location = st.sidebar.selectbox("Titik awal kurir", NODE_NAMES, index=0)
    start_node = NODE_NAMES.index(start_location)

    st.sidebar.markdown(
        f"""
        <div class="card">
            <b>Jenis Kendaraan:</b> {vehicle}<br>
            <b>Nama Kendaraan:</b> {vehicle_name}<br>
            <b>Kapasitas:</b> {capacity} unit<br>
            <b>Titik awal:</b> {start_location}<br>
            <b>Keterangan:</b> {vehicle_description}
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

            new_origin = st.selectbox("Asal", NODE_NAMES, key="new_origin")
            new_destination = st.selectbox("Tujuan", NODE_NAMES, key="new_destination")
            new_priority = st.slider("Prioritas", 1, 5, 3)
            new_volume = st.number_input("Volume", min_value=1, max_value=100, value=10)
            new_deadline = st.number_input("Deadline", min_value=1, max_value=200, value=40)

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
            st.session_state.packages = [package.copy() for package in DEFAULT_PACKAGES]
            st.rerun()

    with st.sidebar.expander("Tambah Jalan / Rute Graf"):
        with st.form("add_edge_form"):
            edge_start = st.selectbox("Dari", NODE_NAMES, key="edge_start")
            edge_end = st.selectbox("Ke", NODE_NAMES, key="edge_end")
            edge_weight = st.number_input("Jarak", min_value=1, max_value=100, value=5)

            submitted_edge = st.form_submit_button("Tambah Jalan")

            if submitted_edge:
                start_index = NODE_NAMES.index(edge_start)
                end_index = NODE_NAMES.index(edge_end)

                if start_index == end_index:
                    st.error("Node awal dan tujuan tidak boleh sama.")
                else:
                    existing_edges = {
                        tuple(sorted((start, end)))
                        for start, end, _ in st.session_state.edges
                    }

                    new_edge_key = tuple(sorted((start_index, end_index)))

                    if new_edge_key in existing_edges:
                        st.warning("Jalan tersebut sudah ada.")
                    else:
                        st.session_state.edges.append((start_index, end_index, int(edge_weight)))
                        st.success("Jalan berhasil ditambahkan.")
                        st.rerun()

        if st.button("Reset graf ke data awal"):
            st.session_state.edges = DEFAULT_EDGES[:]
            st.rerun()

    return vehicle, vehicle_name, capacity, start_location, start_node


def render_input_page(vehicle: str, capacity: int) -> None:
    st.subheader("Daftar Paket")
    st.write("Centang paket yang ingin dibawa. Data paket bisa diedit, tetapi ID Paket dikunci agar tidak dobel.")

    package_df = packages_to_dataframe(st.session_state.packages)

    edited_df = st.data_editor(
        package_df,
        use_container_width=True,
        hide_index=True,
        disabled=["ID Paket"],
        column_config={
            "Pilih": st.column_config.CheckboxColumn("Pilih"),
            "Asal": st.column_config.SelectboxColumn("Asal", options=NODE_NAMES),
            "Tujuan": st.column_config.SelectboxColumn("Tujuan", options=NODE_NAMES),
            "Prioritas": st.column_config.NumberColumn("Prioritas", min_value=1, max_value=5),
            "Volume": st.column_config.NumberColumn("Volume", min_value=1, max_value=100),
            "Deadline": st.column_config.NumberColumn("Deadline", min_value=1, max_value=200),
        },
        key="package_editor"
    )

    current_packages = dataframe_to_packages(edited_df)
    st.session_state.packages = current_packages

    duplicate_ids = find_duplicate_ids(current_packages)
    selected_packages = [package for package in current_packages if package["selected"]]

    total_volume = sum(package["volume"] for package in selected_packages)
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


def render_graph_page() -> None:
    total_edges = len(st.session_state.edges)

    st.subheader(f"Peta Graf {NUM_NODES} Node dan {total_edges} Jalan")
    st.write("Graf berikut menunjukkan hubungan antar lokasi dan bobot jarak antar node.")

    edge_df = edges_to_dataframe(st.session_state.edges)

    edited_edge_df = st.data_editor(
        edge_df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "Dari": st.column_config.SelectboxColumn("Dari", options=NODE_NAMES),
            "Ke": st.column_config.SelectboxColumn("Ke", options=NODE_NAMES),
            "Jarak": st.column_config.NumberColumn("Jarak", min_value=1, max_value=100),
        },
        key="edge_editor"
    )

    current_edges = dataframe_to_edges(edited_edge_df)
    st.session_state.edges = current_edges

    if not current_edges:
        st.error("Graf belum memiliki edge/jalan yang valid.")
    else:
        st.graphviz_chart(full_graph_to_dot(current_edges), use_container_width=True)


def render_result_page(vehicle: str, vehicle_name: str, capacity: int, start_node: int) -> None:
    st.subheader("Hasil Perhitungan Rute")

    current_packages = st.session_state.packages
    current_edges = st.session_state.edges

    duplicate_ids = find_duplicate_ids(current_packages)
    selected_packages = [package for package in current_packages if package["selected"]]
    total_volume = sum(package["volume"] for package in selected_packages)
    remaining_capacity = capacity - total_volume

    if duplicate_ids:
        st.error("Tidak bisa menghitung rute karena ada ID paket yang dobel.")
        return

    if not selected_packages:
        st.info("Pilih paket terlebih dahulu pada bagian Input Paket.")
        return

    if total_volume > capacity:
        st.error("Total volume paket melebihi kapasitas kendaraan. Kurangi paket atau pilih kendaraan dengan kapasitas lebih besar.")
        return

    if not current_edges:
        st.error("Graf belum memiliki jalan yang valid.")
        return

    matrix = build_adjacency_matrix(NUM_NODES, current_edges)
    route_results = get_route_alternatives(matrix, selected_packages, start_node=start_node)
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
    col1.metric("Total Jarak", f'{best_route["result"]["total_distance"]} km')
    col2.metric("Paket Terpenuhi", f"{len(fulfilled_rows)} paket")
    col3.metric("Sisa Kapasitas", f"{remaining_capacity} unit")

    st.subheader("Rute Rekomendasi")
    st.write(route_to_text(best_route["result"]["route"]))

    st.subheader("Peta Rute Rekomendasi")
    st.graphviz_chart(route_to_dot(best_route["result"]["route"]), use_container_width=True)

    st.subheader("Urutan Pengantaran")
    st.dataframe(pd.DataFrame(best_route["result"]["delivery_rows"]), use_container_width=True)

    st.subheader("Perbandingan Rute Alternatif")

    comparison_rows = []

    for item in route_results:
        comparison_rows.append({
            "Jenis Rute": item["name"],
            "Total Jarak": item["result"]["total_distance"],
            "Urutan Paket": " -> ".join(package["id"] for package in item["ordered_packages"])
        })

    st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True)

    st.subheader("Paket Terpenuhi")

    if fulfilled_rows:
        st.write(", ".join(row["ID Paket"] for row in fulfilled_rows))
    else:
        st.warning("Tidak ada paket yang memenuhi deadline.")

    st.subheader("Paket Gagal / Tidak Diangkut")

    selected_ids = {package["id"] for package in selected_packages}
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
        st.dataframe(pd.DataFrame(failed_rows), use_container_width=True)
    else:
        st.success("Tidak ada paket gagal.")


def run_app() -> None:
    setup_page()
    init_session_state()

    vehicle, vehicle_name, capacity, _, start_node = render_sidebar()

    pages = ["Input Paket", "Peta Graf", "Hasil Rute"]

    page = st.radio(
        "Navigasi",
        pages,
        horizontal=True,
        key="nav_page",
        label_visibility="collapsed"
    )

    if page == "Input Paket":
        render_input_page(vehicle, capacity)

    elif page == "Peta Graf":
        render_graph_page()

    elif page == "Hasil Rute":
        render_result_page(vehicle, vehicle_name, capacity, start_node)