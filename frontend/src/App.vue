<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="site-shell">
    <div class="top-strip">LIBRARY CATALOG · 2026</div>

    <header class="site-header">
      <RouterLink class="brand" to="/">LIBRARY</RouterLink>

      <nav class="nav-links" aria-label="Navigasi utama">
        <RouterLink to="/">Koleksi</RouterLink>
      </nav>
    </header>

    <RouterView />

    <footer class="site-footer">
      <span>Library Catalog</span>
      <span>2026</span>
    </footer>
  </div>
</template>
