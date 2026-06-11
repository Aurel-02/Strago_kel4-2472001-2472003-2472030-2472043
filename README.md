# Strategi Algoritmik - RouteWise

RouteWise adalah aplikasi rekomendasi rute pengiriman paket menggunakan algoritma Dijkstra dan strategi Greedy. Aplikasi ini membantu menentukan rute pengiriman berdasarkan graf berbobot, daftar paket, kapasitas kendaraan, prioritas, volume, dan deadline.

## Identitas Kelompok

| No | NRP | Nama Anggota |
|---:|---|---|
| 1 | 2472001 | Aurellia Yemima Tomy |
| 2 | 2472003 | Maria Mayang Prihariyanti Panduwardani |
| 3 | 2472030 | Felicia Ivanna Widian |
| 4 | 2472043 | Keyren Estevania |

## Topik

**Rute Pengiriman Paket**

## Deskripsi Singkat

Sistem menerima peta kota dalam bentuk graf berbobot dan daftar paket yang memiliki asal, tujuan, prioritas, volume, dan deadline. Sistem kemudian membantu memilih kendaraan, mengecek kapasitas, menghitung jarak terpendek menggunakan Dijkstra, serta menampilkan rute pengiriman rekomendasi.

## Fitur

- Menampilkan graf berbobot dengan 24 node.
- Menghitung jarak terpendek menggunakan Dijkstra.
- Menyediakan pilihan kendaraan seperti Motor, Mobil Box, dan Truk.
- Menampilkan daftar paket dengan checkbox.
- Mengecek kapasitas kendaraan berdasarkan total volume paket.
- Menampilkan rute rekomendasi, total jarak, urutan pengantaran, paket terpenuhi, dan paket gagal.

## Cara Menjalankan Program

Install dependency terlebih dahulu:

```powershell
pip install streamlit pandas graphviz

Jalankan aplikasi Streamlit:

```powershell
python -m streamlit run app.py

Atau jalankan versi terminal:

```powershell
python main.py
