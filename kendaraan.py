class Kendaraan:
    def __init__(self, jenis, nama, kapasitas, biaya_per_km):
        self.jenis = jenis
        self.nama = nama
        self.kapasitas = kapasitas
        self.biaya_per_km = biaya_per_km

    def tampilkan_info(self):
        print(f"Jenis Kendaraan : {self.jenis}")
        print(f"Nama Kendaraan  : {self.nama}")
        print(f"Kapasitas       : {self.kapasitas} unit")
        print(f"Biaya per KM    : Rp{self.biaya_per_km}")

daftar_kendaraan = [
    Kendaraan("Motor", "Motor Kurir Swift", 60, 2000),
    Kendaraan("Mobil Box", "BoxVan Cargo Lite", 250, 5000),
    Kendaraan("Truk", "Truk Logistik HeavyMove", 500, 8000)
]
