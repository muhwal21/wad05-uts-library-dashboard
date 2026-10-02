from json import JSONDecodeError, load
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
SEED_FILE = BASE_DIR / "data" / "books.json"


class BookCreate(BaseModel):
    """Payload untuk membuat atau memperbarui buku."""

    judul: str = Field(..., min_length=2, max_length=120, examples=["Clean Architecture"])
    penulis: str = Field(..., min_length=2, max_length=100, examples=["Robert C. Martin"])
    kategori: str = Field(..., min_length=2, max_length=60, examples=["Teknologi"])
    stok: int = Field(..., ge=0, le=9999, examples=[4])


class Book(BookCreate):
    """Representasi buku lengkap yang dikirim ke frontend."""

    id: int = Field(..., ge=1)


def load_seed_books() -> list[dict]:
    """Muat daftar buku dari file JSON."""
    try:
        with SEED_FILE.open("r", encoding="utf-8") as file:
            data = load(file)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Seed file tidak ditemukan: {SEED_FILE}") from exc
    except JSONDecodeError as exc:
        raise RuntimeError("Format books.json tidak valid.") from exc

    if not isinstance(data, list):
        raise RuntimeError("books.json harus berisi array/list.")

    validated_books = [Book(**item).model_dump() for item in data]
    return validated_books


books: list[dict] = load_seed_books()

app = FastAPI(
    title="WAD05 Library Dashboard API",
    description=(
        "REST API sederhana untuk UTS Web Application Development. "
        "Data awal dibaca dari file JSON."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["System"], summary="Informasi API")
async def root():
    return {
        "message": "WAD05 Library Dashboard API",
        "docs": "/docs",
        "books": "/api/books",
    }


@app.get("/health", tags=["System"], summary="Cek kesehatan API")
async def health():
    return {"status": "ok", "total_books": len(books)}


@app.get(
    "/api/books",
    response_model=list[Book],
    tags=["Books"],
    summary="Ambil seluruh buku",
    description="Mengembalikan seluruh data buku.",
)
async def get_books():
    return books


@app.post(
    "/api/books",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
    summary="Tambah buku baru",
    description="Menambahkan buku baru.",
)
async def create_book(payload: BookCreate):
    next_id = max((book["id"] for book in books), default=0) + 1
    new_book = Book(id=next_id, **payload.model_dump()).model_dump()
    books.append(new_book)
    return new_book


@app.put(
    "/api/books/{book_id}",
    response_model=Book,
    tags=["Books"],
    summary="Perbarui buku",
    description="Memperbarui data buku berdasarkan ID.",
)
async def update_book(book_id: int, payload: BookCreate):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            updated_book = Book(id=book_id, **payload.model_dump()).model_dump()
            books[index] = updated_book
            return updated_book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Buku dengan id {book_id} tidak ditemukan.",
    )


@app.delete(
    "/api/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
    summary="Hapus buku",
    description="Menghapus buku berdasarkan ID.",
)
async def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(index)
            return None

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Buku dengan id {book_id} tidak ditemukan.",
    )
