<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
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

const form = reactive(emptyForm())

const filteredBooks = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()

  if (!query) {
    return books.value
  }

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

const resultsLabel = computed(() => {
  const count = sortedBooks.value.length
  return `${count} ${count === 1 ? 'buku' : 'buku'} ditampilkan`
})

function getStockStatus(stock) {
  if (stock === 0) {
    return { label: 'Stok Habis', className: 'stock-out' }
  }

  if (stock <= 3) {
    return { label: 'Menipis', className: 'stock-low' }
  }

  return { label: 'Tersedia', className: 'stock-available' }
}

function toggleSort() {
  sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
}

function resetForm() {
  Object.assign(form, emptyForm())
  editingId.value = null
}

function openCreateForm() {
  resetForm()
  isFormOpen.value = true
}

function openEditForm(book) {
  form.judul = book.judul
  form.penulis = book.penulis
  form.kategori = book.kategori
  form.stok = book.stok
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
  }, 3000)
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
    judul: form.judul.trim(),
    penulis: form.penulis.trim(),
    kategori: form.kategori.trim(),
    stok: Number(form.stok),
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
  const confirmed = window.confirm(`Hapus "${book.judul}" dari daftar?`)

  if (!confirmed) {
    return
  }

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
    <section class="hero-section">
      <div class="hero-copy">
        <p class="eyebrow">LIBRARY INVENTORY / LIVE CATALOG</p>
        <h1>Books, tracked<br />without the noise.</h1>
        <p class="hero-description">
          Kelola koleksi, pantau stok, dan temukan judul dalam satu dashboard.
          Data terhubung langsung ke FastAPI.
        </p>
      </div>

      <div class="hero-side">
        <span class="hero-index">WAD / 05</span>
        <p>
          A minimal full-stack library interface built with Vue 3 Composition API and
          native Fetch API.
        </p>
      </div>
    </section>

    <section class="page-container dashboard-section">
      <div class="section-heading">
        <div>
          <p class="eyebrow">OVERVIEW</p>
          <h2>Library at a glance</h2>
        </div>
        <button class="primary-button" type="button" @click="openCreateForm">
          <span>+</span>
          Tambah Buku
        </button>
      </div>

      <div class="stats-grid">
        <article class="stat-card stat-card-dark">
          <span class="stat-kicker">01 / COLLECTION</span>
          <strong>{{ totalBooks }}</strong>
          <p>Total Buku</p>
        </article>
        <article class="stat-card">
          <span class="stat-kicker">02 / ATTENTION</span>
          <strong>{{ lowAndOutStock }}</strong>
          <p>Menipis + Habis</p>
        </article>
        <article class="stat-card">
          <span class="stat-kicker">03 / CATEGORIES</span>
          <strong>{{ totalCategories }}</strong>
          <p>Jumlah Kategori</p>
        </article>
        <article class="stat-card">
          <span class="stat-kicker">04 / COPIES</span>
          <strong>{{ totalCopies }}</strong>
          <p>Total Eksemplar</p>
        </article>
      </div>

      <div v-if="successMessage" class="notice notice-success" role="status">
        <span class="notice-icon">✓</span>
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="notice notice-error" role="alert">
        <span class="notice-icon">!</span>
        <div>
          <strong>Koneksi bermasalah</strong>
          <p>{{ errorMessage }}</p>
        </div>
        <button type="button" @click="loadBooks">Coba lagi</button>
      </div>

      <section class="catalog-panel">
        <div class="catalog-toolbar">
          <label class="search-field">
            <span class="search-icon">⌕</span>
            <input
              v-model="searchQuery"
              type="search"
              placeholder="Cari judul atau penulis..."
              aria-label="Cari berdasarkan judul atau penulis"
            />
          </label>

          <button class="sort-button" type="button" @click="toggleSort">
            Judul {{ sortDirection === 'asc' ? 'A—Z' : 'Z—A' }}
            <span>↕</span>
          </button>
        </div>

        <div class="catalog-meta">
          <p>{{ resultsLabel }}</p>
          <span v-if="!loading && !errorMessage" class="live-label">
            <span class="status-dot"></span>
            Data berhasil dimuat
          </span>
        </div>

        <div v-if="loading" class="loading-state" aria-live="polite">
          <div v-for="index in 5" :key="index" class="skeleton-row">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
          </div>
          <p>Memuat koleksi dari backend...</p>
        </div>

        <div v-else-if="!errorMessage && sortedBooks.length === 0" class="empty-state">
          <div class="empty-symbol">Ø</div>
          <h3>Tidak ada buku ditemukan</h3>
          <p>Coba kata kunci lain atau tambahkan buku baru.</p>
          <button class="secondary-button" type="button" @click="searchQuery = ''">
            Hapus pencarian
          </button>
        </div>

        <div v-else-if="!errorMessage" class="table-wrapper">
          <table class="books-table">
            <thead>
              <tr>
                <th>Book / Author</th>
                <th>Kategori</th>
                <th>Stok</th>
                <th>Status</th>
                <th><span class="sr-only">Aksi</span></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="book in sortedBooks" :key="book.id">
                <td data-label="Book / Author">
                  <div class="book-cell">
                    <span class="book-index">{{ String(book.id).padStart(2, '0') }}</span>
                    <div>
                      <strong>{{ book.judul }}</strong>
                      <small>{{ book.penulis }}</small>
                    </div>
                  </div>
                </td>
                <td data-label="Kategori">
                  <span class="category-chip">{{ book.kategori }}</span>
                </td>
                <td data-label="Stok">
                  <span class="stock-number">{{ book.stok }}</span>
                </td>
                <td data-label="Status">
                  <span
                    class="stock-badge"
                    :class="getStockStatus(book.stok).className"
                  >
                    <span></span>
                    {{ getStockStatus(book.stok).label }}
                  </span>
                </td>
                <td data-label="Aksi">
                  <div class="action-buttons">
                    <button
                      class="icon-button"
                      type="button"
                      :aria-label="`Edit ${book.judul}`"
                      title="Edit buku"
                      @click="openEditForm(book)"
                    >
                      Edit
                    </button>
                    <button
                      class="icon-button icon-button-danger"
                      type="button"
                      :aria-label="`Hapus ${book.judul}`"
                      title="Hapus buku"
                      @click="removeBook(book)"
                    >
                      Hapus
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="category-section">
        <div class="section-heading section-heading-compact">
          <div>
            <p class="eyebrow">BONUS / CSS VISUAL</p>
            <h2>Stok per kategori</h2>
          </div>
          <p class="section-note">Dihitung dengan computed, tanpa chart library.</p>
        </div>

        <div class="category-bars">
          <div v-for="item in categorySummary" :key="item.category" class="bar-row">
            <div class="bar-meta">
              <span>{{ item.category }}</span>
              <strong>{{ item.stock }} eks.</strong>
            </div>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: `${item.width}%` }"></div>
            </div>
          </div>
        </div>
      </section>
    </section>

    <div v-if="isFormOpen" class="modal-backdrop" @click.self="closeForm">
      <section class="book-modal" role="dialog" aria-modal="true" aria-labelledby="form-title">
        <div class="modal-header">
          <div>
            <p class="eyebrow">{{ editingId ? 'EDIT RECORD' : 'NEW RECORD' }}</p>
            <h2 id="form-title">{{ editingId ? 'Edit buku' : 'Tambah buku' }}</h2>
          </div>
          <button class="close-button" type="button" aria-label="Tutup form" @click="closeForm">
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

          <div class="threshold-note">
            <span class="mini-dot"></span>
            Habis = 0 · Menipis = 1–3 · Tersedia = 4+
          </div>

          <div class="form-actions">
            <button class="secondary-button" type="button" :disabled="saving" @click="closeForm">
              Batal
            </button>
            <button class="primary-button" type="submit" :disabled="saving">
              {{ saving ? 'Menyimpan...' : editingId ? 'Simpan Perubahan' : 'Tambah Buku' }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </main>
</template>
