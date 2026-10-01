<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="site-shell">
    <div class="top-strip">WAD05 UTS · VUE 3 + FASTAPI · MUH. AWALUDDIN / 25120300003</div>

    <header class="site-header">
      <RouterLink class="brand" to="/">AWAL LIBRARY</RouterLink>

      <nav class="nav-links" aria-label="Navigasi utama">
        <RouterLink to="/">Collection</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </header>

    <RouterView />

    <footer class="site-footer">
      <span>WAD05 · Library Dashboard</span>
      <span>MUH. AWALUDDIN · 25120300003</span>
    </footer>
  </div>
</template>
