<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="site-shell">
    <header class="site-header">
      <RouterLink class="brand" to="/">LIBRARY</RouterLink>

      <nav class="nav-links" aria-label="Navigasi utama">
        <RouterLink to="/">Koleksi</RouterLink>
      </nav>
    </header>

    <RouterView />
  </div>
</template>
