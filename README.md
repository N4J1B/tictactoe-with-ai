# Tic-Tac-Toe with AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Proyek ini menghadirkan permainan Tic-Tac-Toe berbasis web yang dilengkapi dengan dua lawan AI yang berbeda: AI Minimax dan AI Pembelajaran Penguatan (Reinforcement Learning/RL). Frontend dibangun menggunakan React dan Vite, sementara backend, yang bertugas melayani AI RL, didukung oleh Flask.

## Daftar Isi

- [Fitur](#fitur)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Memulai](#memulai)
  - [Prasyarat](#prasyarat)
  - [Instalasi](#instalasi)
  - [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Cara Bermain](#cara-bermain)
- [Pelatihan AI (Opsional)](#pelatihan-ai-opsional)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

## Fitur

* **Papan Tic-Tac-Toe Interaktif**: Mainkan melawan AI di papan Tic-Tac-Toe klasik 3x3.
* **Dua Mode AI**:
    * **AI Minimax**: Lawan AI yang menggunakan algoritma Minimax dengan Pemangkasan Alpha-Beta untuk membuat langkah terbaik.
    * **AI Pembelajaran Penguatan (RL)**: AI yang dilatih menggunakan Tabular Q-Learning untuk mempelajari strategi optimal melalui pengalaman. Model AI ini disimpan dalam file `.pkl`.
* **Pemain vs. AI**: Pilih apakah Anda bermain sebagai 'X' atau 'O' melawan AI.
* **Kontrol Permainan**:
    * **Undo**: Mengembalikan dua langkah terakhir (langkah pemain dan langkah AI).
    * **Reset**: Memulai permainan baru.
* **Frontend Modern**: Dikembangkan dengan React untuk antarmuka pengguna yang dinamis dan Vite untuk pengalaman pengembangan yang cepat.
* **Backend Python untuk AI RL**: Logika AI RL diimplementasikan dalam Python menggunakan Flask untuk menyajikan prediksi melalui API REST.

## Teknologi yang Digunakan

### Frontend
* **React**: Pustaka JavaScript untuk membangun antarmuka pengguna.
* **Vite**: Alat build cepat untuk proyek web modern.
* **CSS**: Untuk menata antarmuka game.

### Backend
* **Python**: Bahasa pemrograman untuk logika AI.
* **Flask**: Mikro framework web untuk Python, digunakan untuk membuat API prediksi AI.
* **NumPy**: Paket fundamental untuk komputasi numerik di Python, digunakan untuk representasi papan di AI.
* **`pickle`**: Modul Python untuk menserialisasi dan deserialisasi struktur objek Python, digunakan untuk menyimpan dan memuat model AI yang dilatih.
* **Flask-CORS**: Ekstensi Flask untuk menangani Cross Origin Resource Sharing (CORS).

### AI
* **Minimax Algorithm dengan Alpha-Beta Pruning**: Digunakan di frontend JavaScript untuk salah satu lawan AI.
* **Tabular Q-Learning**: Algoritma inti yang digunakan untuk AI Pembelajaran Penguatan di backend Python.

## Memulai

Untuk menjalankan proyek ini secara lokal, ikuti langkah-langkah berikut:

### Prasyarat

* **Node.js** (versi LTS direkomendasikan) dan `npm` (Node Package Manager) atau `yarn`.
* **Python 3.x**.

### Instalasi

1.  **Kloning repositori**:
    ```bash
    git clone https://github.com/N4J1B/tictactoe-with-ai.git
    cd n4j1b-tictactoe-with-ai
    ```

2.  **Siapkan Backend**:
    Navigasi ke direktori `backend` dan instal semua paket Python yang diperlukan.
    ```bash
    cd backend
    pip install -r requirement.txt
    ```

3.  **Siapkan Frontend**:
    Kembali ke direktori utama proyek dan instal dependensi JavaScript.
    ```bash
    cd .. # Jika Anda berada di direktori backend
    npm install # atau yarn install
    ```

### Menjalankan Aplikasi

1.  **Jalankan Server Backend**:
    Dari direktori `backend`, mulai server Flask. Secara default, ia akan berjalan pada `http://0.0.0.0:82`.
    ```bash
    python app.py
    ```
    Anda akan melihat pesan di konsol yang menunjukkan bahwa agen AI telah dimuat. Jika model tidak ditemukan, pastikan Anda telah melatihnya atau file `.pkl` berada di lokasi yang benar.

2.  **Konfigurasi URL Backend (Opsional)**:
    Jika backend Anda berjalan di URL atau port yang berbeda dari `http://localhost:82/`, perbarui variabel lingkungan `VITE_BACKEND_URL` di file `.env.example` dan ganti namanya menjadi `.env`.
    ```
    # .env
    VITE_BACKEND_URL = "http://localhost:82/" # ganti sesuai URL backend Anda
    ```

3.  **Jalankan Frontend**:
    Buka terminal baru, pastikan Anda berada di direktori utama proyek, lalu jalankan aplikasi React.
    ```bash
    npm run dev # atau yarn dev
    ```
    Ini akan membuka aplikasi di browser web default Anda, biasanya di `http://localhost:5173`.

## Pelatihan AI (Opsional)

AI Pembelajaran Penguatan dilatih menggunakan Tabular Q-Learning. Kode pelatihan dapat ditemukan di `backend/main.ipynb`. File ini berisi proses inisialisasi agen, siklus pelatihan (sejumlah episode), dan penyimpanan model yang sudah dilatih ke file `.pkl` (`tictactoe_agent_x.pkl` dan `tictactoe_agent_o.pkl`). Anda dapat menjalankan notebook ini untuk melatih ulang AI atau menyesuaikan parameter pembelajarannya.

## Kontribusi

Jika Anda memiliki saran atau menemukan *bug*, silakan buka *issue* atau kirim *pull request*.

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.

---
