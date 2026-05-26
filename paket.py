class Paket:

    def __init__(self, id_paket, berat):
        self.id_paket = id_paket
        self.berat = berat

    def tampilkan_paket(self):

        print(f"Paket {self.id_paket} - Berat: {self.berat} kg")


daftar_paket = [
    Paket(1, 2),
    Paket(2, 4),
    Paket(3, 5),
    Paket(4, 3)
]

def checklist_paket():
    print("\n========== CHECKLIST PAKET ==========")
    total_berat = 0
    for paket in daftar_paket:
        paket.tampilkan_paket()
        total_berat += paket.berat
    print("-------------------------------------")
    print(f"Total Berat Paket : {total_berat} kg")
    print("-------------------------------------")
    return total_berat