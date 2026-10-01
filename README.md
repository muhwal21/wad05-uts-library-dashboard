# WAD05 UTS — Library Dashboard

Mini dashboard perpustakaan full-stack yang dibuat dengan Vue 3 dan FastAPI. Aplikasi ini digunakan untuk mengelola koleksi buku, melihat ringkasan stok, melakukan pencarian dan pengurutan, serta menambah, mengubah, dan menghapus data buku.

## Features

- Menampilkan daftar buku dari backend
- Pencarian berdasarkan judul atau penulis
- Pengurutan judul A–Z dan Z–A
- Tambah, edit, dan hapus buku
- Status stok otomatis: Tersedia, Menipis, dan Stok Habis
- Ringkasan total buku, stok menipis/habis, kategori, dan total eksemplar
- Ringkasan stok per kategori
- Loading, empty state, dan error handling
- Responsive untuk desktop, tablet, dan mobile

## Tech Stack

**Frontend**
- Vue 3
- Composition API
- Vue Router
- JavaScript
- Fetch API
- CSS

**Backend**
- FastAPI
- Pydantic
- Uvicorn
- Python

## Project Structure

```text
wad05-uts-library-dashboard/
├── backend/
│   ├── data/
│   │   └── books.json
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── router/
│   │   ├── services/
│   │   ├── views/
│   │   ├── App.vue
│   │   └── main.js
│   └── package.json
└── README.md
```

## Running the Project

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

OpenAPI documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/books` | Mengambil seluruh data buku |
| POST | `/api/books` | Menambahkan buku baru |
| PUT | `/api/books/{book_id}` | Mengubah data buku |
| DELETE | `/api/books/{book_id}` | Menghapus buku |

## Stock Status

Status stok menggunakan aturan berikut:

- **Stok Habis**: `0`
- **Menipis**: `1–3`
- **Tersedia**: `4+`

## Development Check

```bash
cd frontend
npm run lint
npm run build
```

## Author

**Muh. Awaluddin**  
NIM: `25120300003`
