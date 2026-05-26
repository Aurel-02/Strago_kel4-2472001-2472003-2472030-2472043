# Seed data untuk aplikasi RouteWise.

# File ini berfungsi sebagai pengganti database sementara.
# Data kendaraan, node, edge, dan paket disimpan dalam bentuk list/dictionary

VEHICLES = {
    "Motor": {
        "capacity": 60,
        "description": "Cocok untuk paket kecil/sedang"
    },
    "Mobil Box": {
        "capacity": 250,
        "description": "Cocok untuk paket banyak/besar"
    },
    "Truck": {
        "capacity": 500,
        "description": "Cocok untuk paket sangat besar/berat"
    }
}

NODE_NAMES = [
    "Gudang Pusat", "Agen Barat", "Agen Utara", "Agen Timur", "Agen Selatan",
    "Pasar Lama", "Pasar Baru", "Mall Kota", "Kampus", "Sekolah",
    "Rumah Sakit", "Perumahan A", "Perumahan B", "Perumahan C",
    "Apartemen A", "Apartemen B", "Ruko A", "Ruko B", "Terminal",
    "Stasiun", "Pabrik", "Kantor Pos", "Gudang Cabang", "Hub Selatan"
]

DEFAULT_EDGES = [
    (0, 1, 4), (0, 2, 5), (0, 4, 6),
    (1, 5, 3), (1, 11, 5),
    (2, 6, 4), (2, 8, 6),
    (3, 7, 4), (3, 16, 5), (3, 22, 9),
    (4, 18, 4), (4, 23, 7),
    (5, 6, 3), (5, 12, 6),
    (6, 7, 4), (6, 9, 5),
    (7, 8, 3), (7, 14, 6),
    (8, 9, 4), (8, 10, 5),
    (9, 13, 5),
    (10, 15, 4), (10, 17, 7),
    (11, 12, 3), (11, 19, 8),
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
    (22, 23, 5)
]

DEFAULT_PACKAGES = [
    {"selected": True,  "id": "P001", "origin": 0,  "destination": 8,  "priority": 5, "volume": 10, "deadline": 25},
    {"selected": True,  "id": "P002", "origin": 0,  "destination": 9,  "priority": 4, "volume": 8,  "deadline": 28},
    {"selected": False, "id": "P003", "origin": 1,  "destination": 12, "priority": 3, "volume": 12, "deadline": 35},
    {"selected": True,  "id": "P004", "origin": 2,  "destination": 7,  "priority": 5, "volume": 15, "deadline": 30},
    {"selected": False, "id": "P005", "origin": 5,  "destination": 10, "priority": 4, "volume": 9,  "deadline": 32},
    {"selected": False, "id": "P006", "origin": 6,  "destination": 14, "priority": 3, "volume": 14, "deadline": 40},
    {"selected": False, "id": "P007", "origin": 3,  "destination": 17, "priority": 5, "volume": 18, "deadline": 38},
    {"selected": False, "id": "P008", "origin": 4,  "destination": 18, "priority": 2, "volume": 7,  "deadline": 26},
    {"selected": True,  "id": "P009", "origin": 11, "destination": 19, "priority": 4, "volume": 16, "deadline": 45},
    {"selected": False, "id": "P010", "origin": 13, "destination": 15, "priority": 3, "volume": 11, "deadline": 42},
    {"selected": False, "id": "P011", "origin": 10, "destination": 22, "priority": 5, "volume": 20, "deadline": 55},
    {"selected": False, "id": "P012", "origin": 18, "destination": 21, "priority": 4, "volume": 13, "deadline": 50},
    {"selected": False, "id": "P013", "origin": 19, "destination": 20, "priority": 2, "volume": 22, "deadline": 60},
    {"selected": False, "id": "P014", "origin": 20, "destination": 23, "priority": 3, "volume": 25, "deadline": 70},
    {"selected": False, "id": "P015", "origin": 7,  "destination": 13, "priority": 5, "volume": 10, "deadline": 36},
    {"selected": False, "id": "P016", "origin": 8,  "destination": 16, "priority": 4, "volume": 12, "deadline": 44},
    {"selected": False, "id": "P017", "origin": 9,  "destination": 15, "priority": 3, "volume": 9,  "deadline": 48},
    {"selected": False, "id": "P018", "origin": 22, "destination": 23, "priority": 4, "volume": 17, "deadline": 65},
]