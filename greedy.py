def seleksi_greedy(total_berat, daftar_kendaraan):

    # Urutkan kendaraan dari kapasitas terkecil
    kendaraan_urut = sorted(
        daftar_kendaraan,
        key=lambda kendaraan: kendaraan.kapasitas
    )

    # Pilih kendaraan paling efisien
    for kendaraan in kendaraan_urut:

        if total_berat <= kendaraan.kapasitas:

            return kendaraan

    return None