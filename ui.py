import streamlit.components.v1 as components
import pandas as pd
import streamlit as st

from data import DEFAULT_EDGES, DEFAULT_PACKAGES, NODE_NAMES, VEHICLES
from graph import (
    NUM_NODES,
    build_adjacency_matrix,
    full_graph_to_dot,
    graph_with_route_to_dot,
    route_to_dot,
    route_to_dot_partial,
    route_to_text
)
from greedy import get_route_alternatives, get_best_route

def render_route_html(route):
    if not route:
        return
    
    html = '<div style="display: flex; flex-direction: row; overflow-x: auto; padding: 20px 10px; gap: 12px; align-items: center; background: linear-gradient(135deg, #FFF7F4 0%, #EAF2FF 100%); border-radius: 16px; min-height: 90px;">'
    
    for i, node in enumerate(route):
        node_name = NODE_NAMES[node]
        html += f'<div style="min-width: 140px; text-align: center; padding: 14px 18px; background-color: #FFE1D7; border: 2px solid #0259DD; border-radius: 12px; font-family: Arial, sans-serif; font-size: 15px; font-weight: bold; color: #0259DD; white-space: nowrap; box-shadow: 0 4px 8px rgba(2,89,221,0.12); flex-shrink: 0;">{i}. {node_name}</div>'
        if i < len(route) - 1:
            html += '<div style="font-size: 26px; font-weight: bold; color: #FF6648; flex-shrink: 0;">&#8594;</div>'
            
    html += '</div>'
    components.html(html, height=140, scrolling=False)

def render_route_html_partial(route, active_step):
    if not route:
        return
    
    html = '<div style="display: flex; flex-direction: row; overflow-x: auto; padding: 20px 10px; gap: 12px; align-items: center; background: linear-gradient(135deg, #FFF7F4 0%, #EAF2FF 100%); border-radius: 16px; min-height: 90px;">'
    
    for i, node in enumerate(route):
        node_name = NODE_NAMES[node]
        
        if i < active_step:
            bg_color = "#EAF2FF"
            border_color = "#0259DD"
            text_color = "#0259DD"
        elif i == active_step:
            bg_color = "#FFE1D7"
            border_color = "#FF6648"
            text_color = "#0259DD"
        else:
            bg_color = "#F8FAFC"
            border_color = "#CBD5E1"
            text_color = "#334155"
            
        html += f'<div style="min-width: 140px; text-align: center; padding: 14px 18px; background-color: {bg_color}; border: 2px solid {border_color}; border-radius: 12px; font-family: Arial, sans-serif; font-size: 15px; font-weight: bold; color: {text_color}; white-space: nowrap; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08); flex-shrink: 0;">{i}. {node_name}</div>'
        if i < len(route) - 1:
            arr_color = "#FF6648" if i < active_step else "#CBD5E1"
            html += f'<div style="font-size: 26px; font-weight: bold; color: {arr_color}; flex-shrink: 0;">&#8594;</div>'
            
    html += '</div>'
    components.html(html, height=140, scrolling=False)

def copy_default_packages():
    copied_packages = []
    for package in DEFAULT_PACKAGES:
        copied_packages.append(package.copy())

    return copied_packages

def copy_default_edges():
    copied_edges = []

    for edge in DEFAULT_EDGES:
        copied_edges.append(edge)

    return copied_edges

def setup_page():
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

        [data-testid="stGraphVizChart"] svg {
            max-width: none !important;
            width: auto !important;
            height: auto !important;
        }
        
        [data-testid="stGraphVizChart"] {
            overflow-x: auto !important;
            overflow-y: hidden !important;
            padding-bottom: 10px;
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


def get_vehicle_detail(vehicle):
    vehicle_data = VEHICLES[vehicle]

    if (isinstance(vehicle_data, dict)):
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
        package_id = str(package["id"])
        package_id = package_id.upper()
        package_id = package_id.strip()

        if (package_id.startswith("P") and package_id[1:].isdigit()):
            numbers.append(int(package_id[1:]))

    if (numbers):
        next_number = max(numbers) + 1
    else:
        next_number = 1

    return f"P{next_number:03d}"


def find_duplicate_ids(packages):
    ids = []

    for package in packages:
        package_id = str(package["id"])
        package_id = package_id.upper()
        package_id = package_id.strip()
        ids.append(package_id)
    duplicate_ids = []

    for package_id in ids:
        if (ids.count(package_id) > 1):
            if (package_id not in duplicate_ids):
                duplicate_ids.append(package_id)
    duplicate_ids.sort()
    return duplicate_ids

def get_node_index_by_name(node_name):
    index = 0

    for name in NODE_NAMES:
        if (name == node_name):
            return index
        index = index + 1
    return None

def packages_to_dataframe(packages):
    rows = []

    for package in packages:
        row = {
            "Pilih": bool(package.get("selected", False)),
            "ID Paket": package["id"],
            "Asal": NODE_NAMES[package["origin"]],
            "Tujuan": NODE_NAMES[package["destination"]],
            "Prioritas": package["priority"],
            "Volume": package["volume"],
            "Deadline": package["deadline"]
        }
        rows.append(row)
    return pd.DataFrame(rows)


def dataframe_to_packages(dataframe):
    converted_packages = []

    for row_index, row in dataframe.iterrows():
        package_id = str(row["ID Paket"])
        package_id = package_id.upper()
        package_id = package_id.strip()

        origin_name = row["Asal"]
        destination_name = row["Tujuan"]

        if (package_id == ""):
            continue

        origin_index = get_node_index_by_name(origin_name)
        destination_index = get_node_index_by_name(destination_name)

        if (origin_index is None or destination_index is None):
            continue

        converted_package = {
            "selected": bool(row["Pilih"]),
            "id": package_id,
            "origin": origin_index,
            "destination": destination_index,
            "priority": int(row["Prioritas"]),
            "volume": int(row["Volume"]),
            "deadline": int(row["Deadline"])
        }
        converted_packages.append(converted_package)
    return converted_packages

def edges_to_dataframe(edges):
    rows = []
    for edge in edges:
        start = edge[0]
        end = edge[1]
        weight = edge[2]
        row = {
            "Dari": NODE_NAMES[start],
            "Ke": NODE_NAMES[end],
            "Jarak": weight
        }

        rows.append(row)

    return pd.DataFrame(rows)

def edge_key(edge):
    start = edge[0]
    end = edge[1]

    if (start < end):
        return str(start) + "-" + str(end)
    else:
        return str(end) + "-" + str(start)


def dataframe_to_edges(dataframe):
    edges = []
    seen = []

    for row_index, row in dataframe.iterrows():
        start_name = row["Dari"]
        end_name = row["Ke"]

        start = get_node_index_by_name(start_name)
        end = get_node_index_by_name(end_name)

        if (start is None or end is None):
            continue
        if (start == end):
            continue
        try:
            weight = int(row["Jarak"])
        except ValueError:
            continue
        if (weight <= 0):
            continue
        edge = (start, end, weight)
        key = edge_key(edge)
        if (key in seen):
            continue
        seen.append(key)
        edges.append(edge)

    return edges

def go_to_result_page():
    st.session_state.nav_page = "Hasil Rute"


def init_session_state():
    if ("packages" not in st.session_state):
        st.session_state.packages = copy_default_packages()

    if ("edges" not in st.session_state):
        st.session_state.edges = copy_default_edges()

    if ("nav_page" not in st.session_state):
        st.session_state.nav_page = "Input Paket"

    if ("closed_road_choice" not in st.session_state):
        st.session_state.closed_road_choice = None

    if ("closed_road_key" not in st.session_state):
        st.session_state.closed_road_key = None

    if ("closed_road_source" not in st.session_state):
        st.session_state.closed_road_source = None


def render_sidebar():
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

            if (submitted):
                origin_index = NODE_NAMES.index(new_origin)
                destination_index = NODE_NAMES.index(new_destination)

                if (origin_index == destination_index):
                    st.error("Asal dan tujuan tidak boleh sama.")
                else:
                    new_package = {
                        "selected": False,
                        "id": new_id,
                        "origin": origin_index,
                        "destination": destination_index,
                        "priority": new_priority,
                        "volume": int(new_volume),
                        "deadline": int(new_deadline)
                    }

                    st.session_state.packages.append(new_package)
                    st.success("Paket berhasil ditambahkan.")
                    st.rerun()

        if (st.button("Reset paket ke data awal")):
            st.session_state.packages = copy_default_packages()
            st.rerun()

    with st.sidebar.expander("Tambah Jalan / Rute Graf"):
        with st.form("add_edge_form"):
            edge_start = st.selectbox("Dari", NODE_NAMES, key="edge_start")
            edge_end = st.selectbox("Ke", NODE_NAMES, key="edge_end")
            edge_weight = st.number_input("Jarak", min_value=1, max_value=100, value=5)

            submitted_edge = st.form_submit_button("Tambah Jalan")

            if (submitted_edge):
                start_index = NODE_NAMES.index(edge_start)
                end_index = NODE_NAMES.index(edge_end)

                if (start_index == end_index):
                    st.error("Node awal dan tujuan tidak boleh sama.")
                else:
                    existing_edges = []

                    for edge in st.session_state.edges:
                        key = edge_key(edge)
                        existing_edges.append(key)

                    new_edge = (start_index, end_index, int(edge_weight))
                    new_edge_key = edge_key(new_edge)

                    if (new_edge_key in existing_edges):
                        st.warning("Jalan tersebut sudah ada.")
                    else:
                        st.session_state.edges.append(new_edge)
                        st.success("Jalan berhasil ditambahkan.")
                        st.rerun()

        if (st.button("Reset graf ke data awal")):
            st.session_state.edges = copy_default_edges()
            st.session_state.closed_road_choice = None
            st.session_state.closed_road_key = None
            st.session_state.closed_road_source = None
            st.rerun()
    return vehicle, vehicle_name, capacity, start_location, start_node

def render_input_page(vehicle, capacity):
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
            "Deadline": st.column_config.NumberColumn("Deadline", min_value=1, max_value=200)
        },
        key="package_editor"
    )

    current_packages = dataframe_to_packages(edited_df)
    st.session_state.packages = current_packages

    duplicate_ids = find_duplicate_ids(current_packages)

    selected_packages = []

    for package in current_packages:
        if (package["selected"]):
            selected_packages.append(package)

    total_volume = 0

    for package in selected_packages:
        total_volume = total_volume + package["volume"]

    remaining_capacity = capacity - total_volume

    if (duplicate_ids):
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

    if (not selected_packages):
        st.markdown(
            '<div class="warning-card"><b>Status:</b> Belum ada paket yang dipilih.</div>',
            unsafe_allow_html=True
        )
    elif (total_volume <= capacity):
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

    button_disabled = False

    if (duplicate_ids):
        button_disabled = True

    if (not selected_packages):
        button_disabled = True

    if (total_volume > capacity):
        button_disabled = True

    st.button(
        "Hitung Rute",
        use_container_width=True,
        on_click=go_to_result_page,
        disabled=button_disabled
    )

    if (duplicate_ids):
        st.caption("Tombol Hitung Rute nonaktif karena terdapat ID paket yang dobel.")
    elif (not selected_packages):
        st.caption("Pilih minimal satu paket untuk menghitung rute.")
    elif (total_volume > capacity):
        st.caption("Kurangi paket atau pilih kendaraan dengan kapasitas lebih besar.")
    else:
        st.caption("Klik Hitung Rute untuk langsung membuka bagian Hasil Rute.")

def render_graph_page():
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
            "Jarak": st.column_config.NumberColumn("Jarak", min_value=1, max_value=100)
        },
        key="edge_editor"
    )

    current_edges = dataframe_to_edges(edited_edge_df)
    st.session_state.edges = current_edges

    if (not current_edges):
        st.error("Graf belum memiliki edge/jalan yang valid.")
    else:
        st.graphviz_chart(full_graph_to_dot(current_edges), use_container_width=True)

def get_selected_packages(current_packages):
    selected_packages = []
    for package in current_packages:
        if (package["selected"]):
            selected_packages.append(package)
    return selected_packages

def get_total_volume(packages):
    total_volume = 0
    for package in packages:
        total_volume = total_volume + package["volume"]
    return total_volume

def render_result_page(vehicle, vehicle_name, capacity, start_node):
    st.subheader("Hasil Perhitungan Rute")

    current_packages = st.session_state.packages
    current_edges = st.session_state.edges

    duplicate_ids = find_duplicate_ids(current_packages)
    selected_packages = get_selected_packages(current_packages)
    total_volume = get_total_volume(selected_packages)
    remaining_capacity = capacity - total_volume

    if (duplicate_ids):
        st.error("Tidak bisa menghitung rute karena ada ID paket yang dobel.")
        return

    if (not selected_packages):
        st.info("Pilih paket terlebih dahulu pada bagian Input Paket.")
        return

    if (total_volume > capacity):
        st.error("Total volume paket melebihi kapasitas kendaraan. Kurangi paket atau pilih kendaraan dengan kapasitas lebih besar.")
        return

    if (not current_edges):
        st.error("Graf belum memiliki jalan yang valid.")
        return

    matrix = build_adjacency_matrix(NUM_NODES, current_edges)
    route_results = get_route_alternatives(matrix, selected_packages, start_node=start_node)
    best_route = get_best_route(route_results)

    fulfilled_rows = []
    deadline_failed = []

    for row in best_route["result"]["delivery_rows"]:
        if (row["Status Deadline"] == "Memenuhi"):
            fulfilled_rows.append(row)
        elif (row["Status Deadline"] == "Melewati deadline"):
            deadline_failed.append(row)

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
    render_route_html(best_route["result"]["route"])

    st.subheader("Route Replay / Simulasi Perjalanan Kurir")
    route = best_route["result"]["route"]

    if (len(route) > 1):
        active_step = st.slider(
            "Geser step untuk melihat posisi kurir",
            min_value=0,
            max_value=len(route) - 1,
            value=0,
            key="route_replay_slider"
        )

        route_until_active_step = []

        index = 0

        while (index <= active_step):
            route_until_active_step.append(route[index])
            index = index + 1

        st.markdown(
            f"""
            <div class="card">
                <b>Step aktif:</b> {active_step}<br>
                <b>Posisi kurir:</b> {NODE_NAMES[route[active_step]]}<br>
                <b>Rute yang sudah dilewati:</b> {route_to_text(route_until_active_step)}
            </div>
            """,
            unsafe_allow_html=True
        )

        render_route_html_partial(route, active_step)
    else:
        st.info("Route replay belum bisa ditampilkan karena rute hanya berisi satu node.")

    st.subheader("Urutan Pengantaran dan Detail Dijkstra Per Paket")
    st.dataframe(pd.DataFrame(best_route["result"]["delivery_rows"]), use_container_width=True)

    greedy_route = None

    for item in route_results:
        if (item.get("candidate_rankings")):
            greedy_route = item
            break

    st.subheader("Candidate Ranking Greedy")

    if (greedy_route and greedy_route["candidate_rankings"]):
        st.write(
            "Tabel ini menunjukkan alasan paket dipilih. Setiap kandidat dihitung menggunakan jarak terpendek Dijkstra, lalu digabungkan dengan prioritas dan deadline."
        )
        st.dataframe(pd.DataFrame(greedy_route["candidate_rankings"]), use_container_width=True)
    else:
        st.info("Tidak ada candidate ranking yang dapat ditampilkan.")

    st.subheader("Perbandingan Rute Alternatif")

    comparison_rows = []

    for item in route_results:
        package_ids = []

        for package in item["ordered_packages"]:
            package_ids.append(package["id"])

        row = {
            "Jenis Rute": item["name"],
            "Total Jarak": item["result"]["total_distance"],
            "Urutan Paket": " -> ".join(package_ids)
        }
        comparison_rows.append(row)

    st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True)

    st.subheader("Paket Terpenuhi")

    if (fulfilled_rows):
        fulfilled_package_ids = []

        for row in fulfilled_rows:
            fulfilled_package_ids.append(row["ID Paket"])

        st.write(", ".join(fulfilled_package_ids))
    else:
        st.warning("Tidak ada paket yang memenuhi deadline.")

    st.subheader("Paket Gagal / Tidak Diangkut")

    selected_ids = []

    for package in selected_packages:
        selected_ids.append(package["id"])

    failed_rows = []

    for package in current_packages:
        if (package["id"] not in selected_ids):
            failed_row = {
                "ID Paket": package["id"],
                "Asal": NODE_NAMES[package["origin"]],
                "Tujuan": NODE_NAMES[package["destination"]],
                "Alasan": "Tidak dipilih"
            }

            failed_rows.append(failed_row)

    for row in deadline_failed:
        failed_row = {
            "ID Paket": row["ID Paket"],
            "Asal": row["Asal"],
            "Tujuan": row["Tujuan"],
            "Alasan": "Melewati deadline"
        }

        failed_rows.append(failed_row)

    for row in best_route["result"]["failed_rows"]:
        failed_rows.append(row)

    if (failed_rows):
        st.dataframe(pd.DataFrame(failed_rows), use_container_width=True)
    else:
        st.success("Tidak ada paket gagal.")


def validate_selected_packages_for_routing(capacity):
    current_packages = st.session_state.packages
    current_edges = st.session_state.edges

    duplicate_ids = find_duplicate_ids(current_packages)
    selected_packages = get_selected_packages(current_packages)
    total_volume = get_total_volume(selected_packages)

    if (duplicate_ids):
        return None, "Tidak bisa menghitung rute karena ada ID paket yang dobel."

    if (not selected_packages):
        return None, "Pilih paket terlebih dahulu pada bagian Input Paket."

    if (total_volume > capacity):
        return None, "Total volume paket melebihi kapasitas kendaraan."

    if (not current_edges):
        return None, "Graf belum memiliki jalan yang valid."

    return selected_packages, None


def edge_label(edge):
    start = edge[0]
    end = edge[1]
    weight = edge[2]
    return f"{NODE_NAMES[start]} - {NODE_NAMES[end]} ({weight} km)"

def route_uses_edge(route, edge):
    target_key = edge_key(edge)
    index = 0

    while (index < len(route) - 1):
        current_edge = (route[index], route[index + 1], 0)
        current_key = edge_key(current_edge)

        if (current_key == target_key):
            return True
        index = index + 1
    return False

def route_is_not_available(route_result):
    route = route_result["result"]["route"]
    distance = route_result["result"]["total_distance"]

    if (distance == float("inf") or not route):
        return True
    return False

def get_edge_by_key(edges, target_key):
    for edge in edges:
        current_key = edge_key(edge)

        if (current_key == target_key):
            return edge
    return None

def get_edge_by_label(edges, target_label):
    for edge in edges:
        current_label = edge_label(edge)

        if (current_label == target_label):
            return edge
    return None

def get_unique_route_edges(route, current_edges):
    route_edges = []
    used_edge_keys = []

    index = 0

    while (index < len(route) - 1):
        start = route[index]
        end = route[index + 1]
        route_edge = (start, end, 0)
        route_edge_key = edge_key(route_edge)

        for edge in current_edges:
            current_key = edge_key(edge)

            if (current_key == route_edge_key):
                if (current_key not in used_edge_keys):
                    route_edges.append(edge)
                    used_edge_keys.append(current_key)

                break

        index = index + 1

    return route_edges

def build_edge_options(edges):
    edge_options = []

    for edge in edges:
        label = edge_label(edge)
        edge_options.append(label)
    return edge_options

def render_dynamic_reroute_page(vehicle, vehicle_name, capacity, start_node):
    st.subheader("Dynamic Re-routing / Simulasi Jalan Ditutup")
    st.write(
        "Fitur ini mensimulasikan kondisi ketika salah satu jalan pada graf tidak dapat dilewati. "
        "Sistem akan menghapus edge tersebut sementara, lalu menjalankan ulang Dijkstra dan Greedy untuk mencari rute alternatif."
    )

    selected_packages, error_message = validate_selected_packages_for_routing(capacity)

    if (error_message):
        st.warning(error_message)
        return

    current_edges = st.session_state.edges

    if (not current_edges):
        st.error("Graf belum memiliki edge/jalan yang valid.")
        return

    normal_matrix = build_adjacency_matrix(NUM_NODES, current_edges)

    normal_results = get_route_alternatives(
        normal_matrix,
        selected_packages,
        start_node=start_node
    )

    normal_best = get_best_route(normal_results)

    if (route_is_not_available(normal_best)):
        st.error("Rute normal tidak dapat dihitung dari paket yang dipilih dan data graf saat ini.")
        return

    normal_route = normal_best["result"]["route"]
    route_edges = get_unique_route_edges(normal_route, current_edges)
    edge_options = build_edge_options(route_edges)

    if (not edge_options):
        st.warning("Belum ada jalan pada rute normal yang bisa disimulasikan.")
        return

    st.info(
        "Daftar jalan hanya menampilkan jalan yang dilewati oleh rute dari paket yang sedang dicentang. "
        "Input manual tetap bisa digunakan untuk mencoba jalan lain yang ada di graf."
    )

    selection_mode = st.radio(
        "Mode input jalan yang ditutup",
        ["Pilih dari daftar jalan", "Input manual titik jalan"],
        horizontal=True
    )

    with st.form("closed_road_form"):
        if (selection_mode == "Pilih dari daftar jalan"):
            chosen_label_input = st.selectbox("Pilih jalan dari rute aktif", edge_options)
            manual_start = None
            manual_end = None
        else:
            chosen_label_input = None
            col_start, col_end = st.columns(2)

            with col_start:
                manual_start = st.selectbox("Dari", NODE_NAMES, key="manual_closed_start")

            with col_end:
                manual_end = st.selectbox("Ke", NODE_NAMES, key="manual_closed_end")

        submitted = st.form_submit_button("Jalankan Simulasi")

    if (submitted):
        if (selection_mode == "Pilih dari daftar jalan"):
            chosen_edge = get_edge_by_label(route_edges, chosen_label_input)

            if (chosen_edge is None):
                st.session_state.closed_road_key = None
                st.session_state.closed_road_source = None
                st.warning("Jalan yang dipilih sudah tidak tersedia. Silakan pilih ulang.")
                return

            st.session_state.closed_road_key = edge_key(chosen_edge)
            st.session_state.closed_road_source = "rute_aktif"

        else:
            start_index = get_node_index_by_name(manual_start)
            end_index = get_node_index_by_name(manual_end)

            if (start_index == end_index):
                st.session_state.closed_road_key = None
                st.session_state.closed_road_source = None
                st.error("Titik awal dan titik akhir jalan tidak boleh sama.")
                return

            manual_edge = (start_index, end_index, 0)
            manual_key = edge_key(manual_edge)
            chosen_edge = get_edge_by_key(current_edges, manual_key)

            if (chosen_edge is None):
                st.session_state.closed_road_key = None
                st.session_state.closed_road_source = None
                st.warning("Jalan tersebut tidak ada pada graf. Pilih titik jalan yang memang terhubung.")
                return

            if (route_uses_edge(normal_route, chosen_edge)):
                st.session_state.closed_road_source = "rute_aktif"
            else:
                st.session_state.closed_road_source = "luar_rute_aktif"

            st.session_state.closed_road_key = edge_key(chosen_edge)

    if (st.session_state.closed_road_key is None):
        st.info("Pilih jalan dari rute aktif atau input titik jalan manual, lalu tekan Jalankan Simulasi.")
        return

    closed_edge = get_edge_by_key(current_edges, st.session_state.closed_road_key)

    if (closed_edge is None):
        st.session_state.closed_road_key = None
        st.session_state.closed_road_source = None
        st.warning("Jalan yang dipilih sudah tidak tersedia pada graf. Silakan pilih ulang.")
        return

    closed_edge_key = edge_key(closed_edge)
    simulated_edges = []

    for edge in current_edges:
        current_edge_key = edge_key(edge)

        if (current_edge_key != closed_edge_key):
            simulated_edges.append(edge)

    simulated_matrix = build_adjacency_matrix(NUM_NODES, simulated_edges)

    simulated_results = get_route_alternatives(
        simulated_matrix,
        selected_packages,
        start_node=start_node
    )

    simulated_best = get_best_route(simulated_results)

    if (route_is_not_available(simulated_best)):
        st.markdown(
            f"""
            <div class="warning-card">
                <b>Jalan ditutup sementara:</b> {edge_label(closed_edge)}<br>
                <b>Kendaraan:</b> {vehicle} - {vehicle_name}<br>
                <b>Kapasitas:</b> {capacity} unit
            </div>
            """,
            unsafe_allow_html=True
        )
        st.error("Tidak ada rute alternatif setelah jalan tersebut ditutup.")
        st.warning("Penutupan jalan ini membuat rute pengiriman tidak bisa dilanjutkan dari graf yang tersedia.")
        return

    simulated_route = simulated_best["result"]["route"]

    normal_distance = normal_best["result"]["total_distance"]
    simulated_distance = simulated_best["result"]["total_distance"]
    distance_delta = simulated_distance - normal_distance

    normal_failed_count = len(normal_best["result"]["failed_rows"])
    simulated_failed_count = len(simulated_best["result"]["failed_rows"])

    affected_by_closed_edge = route_uses_edge(normal_route, closed_edge)

    if (affected_by_closed_edge):
        affected_text = "Ya, jalan ini ada pada rute aktif dari paket yang dicentang"
    else:
        affected_text = "Tidak, jalan ini ada di graf tetapi tidak dilewati rute aktif"

    st.markdown(
        f"""
        <div class="warning-card">
            <b>Jalan ditutup sementara:</b> {edge_label(closed_edge)}<br>
            <b>Terdampak langsung:</b> {affected_text}<br>
            <b>Kendaraan:</b> {vehicle} - {vehicle_name}<br>
            <b>Kapasitas:</b> {capacity} unit
        </div>
        """,
        unsafe_allow_html=True
    )

    if (st.session_state.closed_road_source == "luar_rute_aktif"):
        st.info(
            "Jalan ini dipilih lewat input manual dan tidak termasuk rute aktif. "
            "Hasil rute bisa saja tetap sama karena jalan tersebut memang tidak dilewati sebelumnya."
        )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Jarak Normal", f"{normal_distance} km")
    col2.metric("Jarak Setelah Ditutup", f"{simulated_distance} km")
    col3.metric("Selisih Jarak", f"{distance_delta} km")
    col4.metric("Paket Gagal Setelah Ditutup", f"{simulated_failed_count} paket")

    st.subheader("Perbandingan Sebelum dan Sesudah Re-routing")

    normal_package_ids = []

    for package in normal_best["ordered_packages"]:
        normal_package_ids.append(package["id"])

    simulated_package_ids = []

    for package in simulated_best["ordered_packages"]:
        simulated_package_ids.append(package["id"])

    comparison_rows = [
        {
            "Kondisi": "Sebelum jalan ditutup",
            "Strategi Terpilih": normal_best["name"],
            "Total Jarak": normal_distance,
            "Jumlah Paket Gagal": normal_failed_count,
            "Rute": route_to_text(normal_route),
            "Urutan Paket": " -> ".join(normal_package_ids)
        },
        {
            "Kondisi": "Sesudah jalan ditutup",
            "Strategi Terpilih": simulated_best["name"],
            "Total Jarak": simulated_distance,
            "Jumlah Paket Gagal": simulated_failed_count,
            "Rute": route_to_text(simulated_route),
            "Urutan Paket": " -> ".join(simulated_package_ids)
        }
    ]

    st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True)

    with st.container():
        st.subheader("Graf Sebelum Jalan Ditutup")
        st.graphviz_chart(
            graph_with_route_to_dot(current_edges, normal_route, closed_edge),
            use_container_width=True
        )

    st.divider()

    with st.container():
        st.subheader("Graf Setelah Dijkstra Hitung Ulang")
        st.graphviz_chart(
            graph_with_route_to_dot(current_edges, simulated_route, closed_edge),
            use_container_width=True
        )

    st.subheader("Detail Pengantaran Setelah Re-routing")

    simulated_delivery_rows = simulated_best["result"]["delivery_rows"]

    if (simulated_delivery_rows):
        st.dataframe(pd.DataFrame(simulated_delivery_rows), use_container_width=True)
    else:
        st.warning("Tidak ada paket yang berhasil dibuat rutenya setelah jalan ditutup.")

    st.subheader("Paket Gagal Karena Gangguan Jalan")

    reroute_failed_rows = simulated_best["result"]["failed_rows"]
    simulated_deadline_failed = []

    for row in simulated_delivery_rows:
        if (row["Status Deadline"] == "Melewati deadline"):
            simulated_deadline_failed.append(row)

    displayed_failed_rows = []

    for row in reroute_failed_rows:
        displayed_failed_rows.append(row)

    for row in simulated_deadline_failed:
        failed_row = {
            "ID Paket": row["ID Paket"],
            "Asal": row["Asal"],
            "Tujuan": row["Tujuan"],
            "Alasan": "Melewati deadline setelah re-routing"
        }
        displayed_failed_rows.append(failed_row)

    if (displayed_failed_rows):
        st.dataframe(pd.DataFrame(displayed_failed_rows), use_container_width=True)
    else:
        st.success("Tidak ada paket gagal setelah re-routing.")

def run_app():
    setup_page()
    init_session_state()

    vehicle, vehicle_name, capacity, start_location, start_node = render_sidebar()

    pages = ["Input Paket", "Peta Graf", "Hasil Rute", "Simulasi Gangguan Jalan"]

    page = st.radio(
        "Navigasi",
        pages,
        horizontal=True,
        key="nav_page",
        label_visibility="collapsed"
    )

    if (page == "Input Paket"):
        render_input_page(vehicle, capacity)

    elif (page == "Peta Graf"):
        render_graph_page()

    elif (page == "Hasil Rute"):
        render_result_page(vehicle, vehicle_name, capacity, start_node)

    elif (page == "Simulasi Gangguan Jalan"):
        render_dynamic_reroute_page(vehicle, vehicle_name, capacity, start_node)