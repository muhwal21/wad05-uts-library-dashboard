const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    let message = `Request gagal (${response.status})`

    try {
      const body = await response.json()
      if (body.detail) {
        message = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail)
      }
    } catch {}

    throw new Error(message)
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

export async function fetchBooks() {
  return request('/api/books')
}

export async function createBook(payload) {
  return request('/api/books', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function updateBook(id, payload) {
  return request(`/api/books/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function deleteBook(id) {
  return request(`/api/books/${id}`, {
    method: 'DELETE',
  })
}
