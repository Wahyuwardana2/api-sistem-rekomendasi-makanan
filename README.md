# API untuk Sistem Rekomendasi Penyakit dan Makanan

Sistem Rekomendasi Penyakit dan Makanan

## Petunjuk Instalasi

1. Pastikan Anda telah menginstal Python. Jika belum, instal Python dari [situs resmi Python](https://www.python.org/).
2. Unduh atau salin script ke direktori lokal Anda.

   ```bash
   git clone https://github.com/nama-pengguna/proyek-api-fastapi.git
   ```

3. Buka terminal atau command prompt dan navigasi ke direktori tempat Anda menyimpan script.
4. Buat virtual environment (opsional, tapi disarankan):
   ```bash
   python -m venv venv
   ```
5. Aktifkan virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix atau MacOS:
     ```bash
     source venv/bin/activate
     ```
6. Instal dependensi dengan menjalankan perintah:
   ```bash
   pip install -r requirements.txt
   ```

## Petunjuk Menjalankan Code

1. Pastikan virtual environment sudah aktif.
2. Jalankan script menggunakan perintah:
   ```bash
   python script.py
   ```

## Petunjuk Penggunaan Pencarian Penyakit dan Makanan melalui Link API

1. Jalankan API menggunakan perintah:
   ```bash
   uvicorn app:app --reload
   ```
2. Buka browser dan akses [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) untuk menggunakan Swagger UI.
3. Pada Swagger UI, gunakan endpoint `/api/recommend_food/{nama_penyakit}` untuk mencari rekomendasi makanan berdasarkan penyakit. Ganti `{nama_penyakit}` dengan nama penyakit yang ingin dicari.
4. Juga, Anda dapat menggunakan endpoint `/api/recommend_disease/{nama_makanan}` untuk mencari rekomendasi penyakit berdasarkan makanan. Ganti `{nama_makanan}` dengan nama makanan yang ingin dicari.

**Catatan**: Pastikan untuk mengganti placeholder seperti `script.py`, `requirements.txt`, `app:app`, dll., sesuai dengan struktur direktori dan nama file yang sesungguhnya.
