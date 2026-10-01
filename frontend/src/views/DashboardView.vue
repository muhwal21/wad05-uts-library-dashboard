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

const categoryOptions = computed(() => {
  const defaults = [
    'Novel',
    'Teknologi',
    'Sejarah',
    'Desain',
    'Pengembangan Diri',
    'Psikologi',
    'Produktivitas',
    'Bisnis',
  ]

  const fromBooks = books.value.map((book) => book.kategori).filter(Boolean)

  return [...new Set([...fromBooks, ...defaults])].sort((a, b) =>
    a.localeCompare(b, 'id', { sensitivity: 'base' }),
  )
})

const resultsLabel = computed(() => `${sortedBooks.value.length} buku`)

function getStockStatus(stock) {
  if (stock === 0) return { label: 'Stok Habis', className: 'stock-out' }
  if (stock <= 3) return { label: 'Menipis', className: 'stock-low' }
  return { label: 'Tersedia', className: 'stock-available' }
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

  const rawCategory = form.value.kategori.trim()
  const existingCategory = categoryOptions.value.find(
    (category) => category.toLowerCase() === rawCategory.toLowerCase(),
  )

  const payload = {
    judul: form.value.judul.trim(),
    penulis: form.value.penulis.trim(),
    kategori: existingCategory || rawCategory,
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
      <p class="breadcrumb">Koleksi buku</p>

      <div class="title-row">
        <div>
          <h1>Perpustakaan</h1>
          <p class="collection-count">{{ totalBooks }} buku dalam koleksi</p>
        </div>

        <button class="button button-dark" type="button" @click="openCreateForm">
          Tambah buku
        </button>
      </div>
    </section>

    <section class="page-container stats-row" aria-label="Ringkasan perpustakaan">
      <article class="stat-box">
        <span>Total buku</span>
        <strong>{{ totalBooks }}</strong>
      </article>
      <article class="stat-box">
        <span>Menipis + habis</span>
        <strong>{{ lowAndOutStock }}</strong>
      </article>
      <article class="stat-box">
        <span>Kategori</span>
        <strong>{{ totalCategories }}</strong>
      </article>
      <article class="stat-box">
        <span>Total eksemplar</span>
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
            placeholder="Cari judul atau penulis"
            aria-label="Cari berdasarkan judul atau penulis"
          />
        </label>

        <button class="sort-control" type="button" @click="toggleSort">
          {{ sortDirection === 'asc' ? 'A–Z' : 'Z–A' }}
        </button>
      </div>

      <div class="catalog-line">
        <strong>{{ resultsLabel }}</strong>
      </div>

      <div v-if="successMessage" class="message message-success" role="status">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="message message-error" role="alert">
        <div>
          <strong>Koneksi bermasalah</strong>
          <p>{{ errorMessage }}</p>
        </div>
        <button class="text-button" type="button" @click="loadBooks">Coba lagi</button>
      </div>

      <div v-if="loading" class="loading-grid" aria-live="polite">
        <div v-for="index in 8" :key="index" class="book-card book-card-loading">
          <div class="cover-placeholder"></div>
          <div class="loading-line"></div>
          <div class="loading-line loading-line-short"></div>
        </div>
      </div>

      <div v-else-if="!errorMessage && sortedBooks.length === 0" class="empty-state">
        <h2>Buku tidak ditemukan</h2>
        <p>Coba kata kunci lain atau tambahkan buku baru.</p>
        <button class="text-button" type="button" @click="searchQuery = ''">
          Hapus pencarian
        </button>
      </div>

      <div v-else-if="!errorMessage" class="book-grid">
        <article v-for="book in sortedBooks" :key="book.id" class="book-card">
          <div class="book-cover" :class="getStockStatus(book.stok).className">
            <span class="cover-category">{{ book.kategori }}</span>
            <div class="cover-copy">
              <span class="cover-kicker">Library</span>
              <strong>{{ book.judul }}</strong>
            </div>
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
              <span>Stok {{ book.stok }}</span>
            </div>

            <div class="book-actions">
              <button type="button" @click="openEditForm(book)">Edit</button>
              <button type="button" @click="removeBook(book)">Hapus</button>
            </div>
          </div>
        </article>
      </div>
    </section>

    <section v-if="!loading && !errorMessage" class="page-container stock-section">
      <div class="stock-heading">
        <h2>Stok per kategori</h2>
      </div>

      <div class="category-list">
        <div v-for="item in categorySummary" :key="item.category" class="category-row">
          <div class="category-meta">
            <span>{{ item.category }}</span>
            <strong>{{ item.stock }}</strong>
          </div>

          <div class="bar-track" aria-hidden="true">
            <div class="bar-fill" :style="{ width: `${item.width}%` }"></div>
          </div>
        </div>
      </div>
    </section>

    <div v-if="isFormOpen" class="modal-backdrop" @click.self="closeForm">
      <section class="book-modal" role="dialog" aria-modal="true" aria-labelledby="form-title">
        <div class="modal-header">
          <div>
            <p class="overline">{{ editingId ? 'Edit koleksi' : 'Buku baru' }}</p>
            <h2 id="form-title">{{ editingId ? 'Edit buku' : 'Tambah buku' }}</h2>
          </div>

          <button class="modal-close" type="button" aria-label="Tutup form" @click="closeForm">
            ×
          </button>
        </div>

        <form class="book-form" @submit.prevent="submitForm">
          <label>
            <span>Judul buku</span>
            <input
              v-model="form.judul"
              required
              minlength="2"
              maxlength="120"
              placeholder="Contoh: Clean Code"
            />
          </label>

          <label>
            <span>Penulis</span>
            <input
              v-model="form.penulis"
              required
              minlength="2"
              maxlength="100"
              placeholder="Nama penulis"
            />
          </label>

          <div class="form-row">
            <label class="category-field">
              <span>Kategori</span>
              <div class="combo-field">
                <input
                  v-model="form.kategori"
                  list="category-options"
                  required
                  minlength="2"
                  maxlength="60"
                  autocomplete="off"
                  placeholder="Pilih atau ketik kategori"
                />
                <span class="combo-chevron" aria-hidden="true">⌄</span>
              </div>

              <datalist id="category-options">
                <option
                  v-for="category in categoryOptions"
                  :key="category"
                  :value="category"
                />
              </datalist>
            </label>

            <label>
              <span>Stok</span>
              <input
                v-model.number="form.stok"
                type="number"
                min="0"
                max="9999"
                required
                placeholder="0"
              />
            </label>
          </div>

          <div class="form-actions">
            <button class="button button-light" type="button" :disabled="saving" @click="closeForm">
              Batal
            </button>
            <button class="button button-dark" type="submit" :disabled="saving">
              {{ saving ? 'Menyimpan...' : editingId ? 'Simpan perubahan' : 'Tambah buku' }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </main>
</template>
