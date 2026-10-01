<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="site-shell">
    <div class="announcement">
      <span>UTS WEB APPLICATION DEVELOPMENT</span>
      <span class="announcement-dot">●</span>
      <span>VUE 3 + FASTAPI</span>
      <span class="announcement-dot">●</span>
      <span>MUH. AWALUDDIN / 25120300003</span>
    </div>

    <header class="site-header">
      <RouterLink class="brand" to="/" aria-label="NOIRARY dashboard">
        <span class="brand-mark">N</span>
        <span>NOIRARY</span>
      </RouterLink>

      <nav class="nav-links" aria-label="Navigasi utama">
        <RouterLink to="/">Dashboard</RouterLink>
        <RouterLink to="/about">Tentang</RouterLink>
      </nav>

      <div class="header-meta">
        <span class="status-dot"></span>
        API READY
      </div>
    </header>

    <RouterView />

    <footer class="site-footer">
      <div>
        <strong>NOIRARY / WAD05</strong>
        <p>Mini Dashboard Perpustakaan — Vue 3 + FastAPI</p>
      </div>
      <div class="footer-right">
        <span>MUH. AWALUDDIN</span>
        <span>25120300003</span>
      </div>
    </footer>
  </div>
</template>
