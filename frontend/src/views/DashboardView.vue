<script setup>
import { computed, onMounted, ref } from 'vue'
import {
  createBook as createBookRequest,
  deleteBook as deleteBookRequest,
  fetchBooks,
  updateBook as updateBookRequest,
} from '../services/api'

const books = ref([])
const searchQuery = ref('')
const sortDirection = ref('asc')
const loading = ref(true)
const errorMessage = ref('')
const successMessage = ref('')
const isFormOpen = ref(false)
const editingId = ref(null)
const saving = ref(false)

const emptyForm = () => ({
  judul: '',
  penulis: '',
  kategori: '',
  stok: 0,
})

// State form memakai ref agar sesuai ketentuan UTS.
const form = ref(emptyForm())

const filteredBooks = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()

  if (!query) return books.value

  return books.value.filter((book) => {
    return (
      book.judul.toLowerCase().includes(query) ||
      book.penulis.toLowerCase().includes(query)
    )
  })
})

const sortedBooks = computed(() => {
  return [...filteredBooks.value].sort((firstBook, secondBook) => {
    const result = firstBook.judul.localeCompare(secondBook.judul, 'id', {
      sensitivity: 'base',
    })

    return sortDirection.value === 'asc' ? result : -result
  })
})

const totalBooks = computed(() => books.value.length)

const lowAndOutStock = computed(() => {
  return books.value.filter((book) => book.stok <= 3).length
})

const totalCategories = computed(() => {
  return new Set(books.value.map((book) => book.kategori)).size
})

const totalCopies = computed(() => {
  return books.value.reduce((total, book) => total + Number(book.stok), 0)
})

const categorySummary = computed(() => {
  const totals = books.value.reduce((summary, book) => {
    summary[book.kategori] = (summary[book.kategori] || 0) + Number(book.stok)
    return summary
  }, {})

  const rows = Object.entries(totals)
    .map(([category, stock]) => ({ category, stock }))
    .sort((a, b) => b.stock - a.stock)

  const highestStock = Math.max(...rows.map((item) => item.stock), 1)

  return rows.map((item) => ({
    ...item,
    width: Math.round((item.stock / highestStock) * 100),
  }))
})

const resultsLabel = computed(() => `${sortedBooks.value.length} books`)

function getStockStatus(stock) {
  if (stock === 0) return { label: 'Sold out', className: 'stock-out' }
  if (stock <= 3) return { label: 'Low stock', className: 'stock-low' }
  return { label: 'Available', className: 'stock-available' }
}

function toggleSort() {
  sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
}

function resetForm() {
  form.value = emptyForm()
  editingId.value = null
}

function openCreateForm() {
  resetForm()
  isFormOpen.value = true
}

function openEditForm(book) {
  form.value = {
    judul: book.judul,
    penulis: book.penulis,
    kategori: book.kategori,
    stok: book.stok,
  }
  editingId.value = book.id
  isFormOpen.value = true
}

function closeForm() {
  if (saving.value) return
  isFormOpen.value = false
  resetForm()
}

function showSuccess(message) {
  successMessage.value = message
  window.setTimeout(() => {
    successMessage.value = ''
  }, 2500)
}

async function loadBooks() {
  loading.value = true
  errorMessage.value = ''

  try {
    books.value = await fetchBooks()
  } catch (error) {
    errorMessage.value = error.message || 'Gagal terhubung ke backend.'
  } finally {
    loading.value = false
  }
}

async function submitForm() {
  saving.value = true
  errorMessage.value = ''

  const payload = {
    judul: form.value.judul.trim(),
    penulis: form.value.penulis.trim(),
    kategori: form.value.kategori.trim(),
    stok: Number(form.value.stok),
  }

  try {
    if (editingId.value) {
      await updateBookRequest(editingId.value, payload)
      showSuccess('Data buku berhasil diperbarui.')
    } else {
      await createBookRequest(payload)
      showSuccess('Buku baru berhasil ditambahkan.')
    }

    await loadBooks()
    isFormOpen.value = false
    resetForm()
  } catch (error) {
    errorMessage.value = error.message || 'Data gagal disimpan.'
  } finally {
    saving.value = false
  }
}

async function removeBook(book) {
  const confirmed = window.confirm(`Hapus "${book.judul}" dari koleksi?`)
  if (!confirmed) return

  errorMessage.value = ''

  try {
    await deleteBookRequest(book.id)
    await loadBooks()
    showSuccess('Buku berhasil dihapus.')
  } catch (error) {
    errorMessage.value = error.message || 'Buku gagal dihapus.'
  }
}

onMounted(loadBooks)
</script>

<template>
  <main>
    <section class="collection-head page-container">
      <p class="breadcrumb">Home / Library</p>
      <div class="title-row">
        <div>
          <h1>Library Collection</h1>
          <p class="collection-count">{{ totalBooks }} books in catalog</p>
        </div>
        <button class="button button-dark" type="button" @click="openCreateForm">
          Add book
        </button>
      </div>
    </section>

    <section class="page-container stats-row" aria-label="Ringkasan perpustakaan">
      <article class="stat-box">
        <span>Total books</span>
        <strong>{{ totalBooks }}</strong>
      </article>
      <article class="stat-box">
        <span>Low + out</span>
        <strong>{{ lowAndOutStock }}</strong>
      </article>
      <article class="stat-box">
        <span>Categories</span>
        <strong>{{ totalCategories }}</strong>
      </article>
      <article class="stat-box">
        <span>Total copies</span>
        <strong>{{ totalCopies }}</strong>
      </article>
    </section>

    <section class="page-container catalog-section">
      <div class="catalog-toolbar">
        <label class="search-field">
          <span class="sr-only">Cari berdasarkan judul atau penulis</span>
          <input
            v-model="searchQuery"
            type="search"
            placeholder="Search title or author"
            aria-label="Cari berdasarkan judul atau penulis"
          />
        </label>

        <button class="sort-control" type="button" @click="toggleSort">
          Sort: {{ sortDirection === 'asc' ? 'A–Z' : 'Z–A' }}
        </button>
      </div>

      <div class="catalog-line">
        <strong>{{ resultsLabel }}</strong>
        <span v-if="!loading && !errorMessage">Data loaded from FastAPI</span>
      </div>

      <div v-if="successMessage" class="message message-success" role="status">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="message message-error" role="alert">
        <div>
          <strong>Connection error</strong>
          <p>{{ errorMessage }}</p>
        </div>
        <button class="text-button" type="button" @click="loadBooks">Try again</button>
      </div>

      <div v-if="loading" class="loading-grid" aria-live="polite">
        <div v-for="index in 8" :key="index" class="book-card book-card-loading">
          <div class="cover-placeholder"></div>
          <div class="loading-line"></div>
          <div class="loading-line loading-line-short"></div>
        </div>
      </div>

      <div v-else-if="!errorMessage && sortedBooks.length === 0" class="empty-state">
        <h2>No books found</h2>
        <p>Coba kata kunci lain atau tambahkan buku baru.</p>
        <button class="text-button" type="button" @click="searchQuery = ''">
          Clear search
        </button>
      </div>

      <div v-else-if="!errorMessage" class="book-grid">
        <article v-for="book in sortedBooks" :key="book.id" class="book-card">
          <div class="book-cover" :class="getStockStatus(book.stok).className">
            <span class="cover-category">{{ book.kategori }}</span>
            <span class="cover-number">{{ String(book.id).padStart(2, '0') }}</span>
          </div>

          <div class="book-info">
            <div class="book-heading">
              <div>
                <h2>{{ book.judul }}</h2>
                <p>{{ book.penulis }}</p>
              </div>
              <span class="stock-label" :class="getStockStatus(book.stok).className">
                {{ getStockStatus(book.stok).label }}
              </span>
            </div>

            <div class="book-meta">
              <span>{{ book.kategori }}</span>
              <span>Stock {{ book.stok }}</span>
            </div>

            <div class="book-actions">
              <button type="button" @click="openEditForm(book)">Edit</button>
              <button type="button" @click="removeBook(book)">Delete</button>
            </div>
          </div>
        </article>
      </div>
    </section>

    <section class="page-container stock-section">
      <div class="stock-heading">
        <div>
          <p class="overline">BONUS</p>
          <h2>Stock by category</h2>
        </div>
        <p>Computed from the same book data.</p>
      </div>

      <div class="category-list">
        <div v-for="item in categorySummary" :key="item.category" class="category-row">
          <div class="category-meta">
            <span>{{ item.category }}</span>
            <strong>{{ item.stock }}</strong>
          </div>
          <div class="bar-track">
            <div class="bar-fill" :style="{ width: `${item.width}%` }"></div>
          </div>
        </div>
      </div>
    </section>

    <div v-if="isFormOpen" class="modal-backdrop" @click.self="closeForm">
      <section class="book-modal" role="dialog" aria-modal="true" aria-labelledby="form-title">
        <div class="modal-header">
          <div>
            <p class="overline">{{ editingId ? 'EDIT BOOK' : 'NEW BOOK' }}</p>
            <h2 id="form-title">{{ editingId ? 'Edit book' : 'Add book' }}</h2>
          </div>
          <button class="modal-close" type="button" aria-label="Tutup form" @click="closeForm">
            ×
          </button>
        </div>

        <form class="book-form" @submit.prevent="submitForm">
          <label>
            <span>Judul buku</span>
            <input v-model="form.judul" required minlength="2" maxlength="120" />
          </label>

          <label>
            <span>Penulis</span>
            <input v-model="form.penulis" required minlength="2" maxlength="100" />
          </label>

          <div class="form-row">
            <label>
              <span>Kategori</span>
              <input v-model="form.kategori" required minlength="2" maxlength="60" />
            </label>

            <label>
              <span>Stok</span>
              <input v-model.number="form.stok" type="number" min="0" max="9999" required />
            </label>
          </div>

          <p class="form-note">Habis = 0 · Menipis = 1–3 · Tersedia = 4+</p>

          <div class="form-actions">
            <button class="button button-light" type="button" :disabled="saving" @click="closeForm">
              Cancel
            </button>
            <button class="button button-dark" type="submit" :disabled="saving">
              {{ saving ? 'Saving...' : editingId ? 'Save changes' : 'Add book' }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </main>
</template>
