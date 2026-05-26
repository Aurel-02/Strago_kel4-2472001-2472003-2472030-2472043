class Kendaraan:

    def __init__(self, nama, kapasitas, biaya_per_km):
        self.nama = nama
        self.kapasitas = kapasitas
        self.biaya_per_km = biaya_per_km

    def tampilkan_info(self):

        print(f"Nama Kendaraan : {self.nama}")
        print(f"Kapasitas      : {self.kapasitas} kg")
        print(f"Biaya per KM   : Rp{self.biaya_per_km}")


# DATA KENDARAAN
daftar_kendaraan = [

    Kendaraan("Motor", 5, 2000),

    Kendaraan("Mobil Van", 20, 5000),

    Kendaraan("Truck", 50, 10000)

]