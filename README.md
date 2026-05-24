#  CryptoSim — Web Simulasi Kriptografi Klasik

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/flask-3.1.1-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](https://opensource.org/licenses/MIT)

**CryptoSim** adalah aplikasi web interaktif yang dirancang untuk melakukan simulasi enkripsi dan dekripsi menggunakan **5 Algoritma Kriptografi Klasik**. Proyek ini dibuat untuk memenuhi **Tugas 1 Mata Kuliah Kriptografi — Semester 6**.

Aplikasi ini dibangun dengan menggunakan framework **Flask** untuk backend dan **Vanilla HTML, CSS, & Javascript** untuk frontend yang menghasilkan antarmuka modern, responsif, dan dinamis (glassmorphism style).

---

##  Fitur Utama

1. **Simulasi Interaktif 5 Ciphers Klasik**: Proses enkripsi & dekripsi dapat disimulasikan secara langsung.
2. **Validasi Kunci yang Ketat**:
   - Memastikan nilai kunci valid secara matematis.
   - Pengecekan nilai prima relatif (coprime) pada **Affine Cipher** ($\gcd(a, 26) = 1$).
   - Pengecekan matriks invertible modulo 26 pada **Hill Cipher**.
3. **Riwayat Aktivitas (History Log)**: Menyimpan riwayat enkripsi/dekripsi selama sesi aktif menggunakan Flask Session, lengkap dengan waktu eksekusi.
4. **Antarmuka Premium & Responsif**: Tampilan modern dengan transisi halus, mendukung berbagai perangkat (desktop, tablet, handphone).

---

##  Algoritma Kriptografi yang Didukung

### 1. Caesar Cipher
Algoritma tertua dan paling sederhana yang menggunakan pergeseran alfabet secara tetap. Setiap huruf pada plaintext digantikan oleh huruf lain yang memiliki selisih posisi tertentu (shift $K$).
- **Rumus Enkripsi**: $C \equiv (P + K) \pmod{26}$
- **Rumus Dekripsi**: $P \equiv (C - K) \pmod{26}$

### 2.  Vigenère Cipher
Metode enkripsi alfabet majemuk (polyalphabetic substitution) dengan menggunakan kata kunci (keyword). Panjang kata kunci akan diulang atau dicocokkan dengan panjang plaintext.
- **Rumus Enkripsi**: $C_i \equiv (P_i + K_i) \pmod{26}$
- **Rumus Dekripsi**: $P_i \equiv (C_i - K_i) \pmod{26}$

### 3.  Affine Cipher
Perluasan dari Caesar Cipher di mana plaintext dikalikan dengan kunci $a$ kemudian ditambahkan kunci $b$ terhadap modulo 26.
- Syarat: Kunci $a$ harus relatif prima dengan 26 ($\gcd(a, 26) = 1$).
- **Rumus Enkripsi**: $C \equiv (a \cdot P + b) \pmod{26}$
- **Rumus Dekripsi**: $P \equiv a^{-1} \cdot (C - b) \pmod{26}$ (di mana $a^{-1}$ adalah modular multiplicative inverse dari $a$ modulo 26).

### 4.  Hill Cipher
Algoritma kriptografi kunci simetris berbasis **Aljabar Linear**. Plaintext dikelompokkan menjadi blok-blok berukuran $m$, kemudian dikalikan dengan matriks kunci berukuran $m \times m$ modulo 26. Aplikasi ini mendukung matriks berukuran $2\times2$ dan $3\times3$.
- Syarat: Matriks kunci harus memiliki determinan yang memiliki invers modulo 26 ($\gcd(\det(K), 26) = 1$).
- **Rumus Enkripsi**: $C \equiv K \cdot P \pmod{26}$
- **Rumus Dekripsi**: $P \equiv K^{-1} \cdot C \pmod{26}$

### 5.  Playfair Cipher
Teknik enkripsi simetris yang mengenkripsi pasangan huruf (digraf) bukan huruf tunggal. Menggunakan tabel berukuran $5 \times 5$ yang berisi kata kunci yang telah dibersihkan (huruf duplikat dihapus, dan biasanya menggabungkan huruf 'J' ke dalam 'I').
- Mengikuti aturan pemrosesan digraf baris yang sama, kolom yang sama, atau membentuk persegi panjang.

---

##  Struktur Direktori Proyek

```text
UTS/
│
├── app.py                 # File utama aplikasi Flask (Routing & API)
├── requirements.txt       # Daftar dependensi Python
├── .gitignore             # File konfigurasi git untuk mengabaikan folder/file tertentu
├── README.md              # Dokumentasi proyek (file ini)
│
├── ciphers/               # Modul implementasi logika kriptografi
│   ├── __init__.py
│   ├── caesar.py
│   ├── vigenere.py
│   ├── affine.py
│   ├── hill.py
│   └── playfair.py
│
├── static/                # Aset statis frontend
│   ├── css/
│   │   └── style.css      # Styling premium dengan UI modern
│   └── js/                # Logika frontend & AJAX handling untuk masing-masing cipher
│
└── templates/             # File HTML Jinja2 untuk UI web
    ├── base.html          # Layout template utama
    ├── index.html         # Halaman utama (dashboard)
    ├── caesar.html
    ├── vigenere.html
    ├── affine.html
    ├── hill.html
    ├── playfair.html
    └── history.html       # Halaman riwayat aktivitas
```

---

## Panduan Instalasi & Cara Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan aplikasi CryptoSim di komputer lokal Anda:

### 1. Klon Repositori
Klon repositori ini dari GitHub ke direktori lokal Anda:
```bash
git clone https://github.com/jihadakbar911/tugas1kripto.git
cd tugas1kripto
```

### 2. Buat & Aktifkan Virtual Environment (venv)
Sangat direkomendasikan untuk menggunakan virtual environment agar tidak merusak dependensi python global Anda.

* **Windows**:
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

* **Linux / macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instal Dependensi
Instal dependensi Flask yang dibutuhkan melalui `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi
Jalankan file server utama `app.py`:
```bash
python app.py
```

Setelah server aktif, buka browser Anda dan akses tautan berikut:
```text
http://127.0.0.1:5000/
```

---

##  Kontributor

* **Jihad Akbar** - [jihadakbar911](https://github.com/jihadakbar911)

---

##  Lisensi

Proyek ini dilisensikan di bawah **MIT License**. Lihat file [LICENSE](LICENSE) jika tersedia untuk informasi lebih lanjut.
