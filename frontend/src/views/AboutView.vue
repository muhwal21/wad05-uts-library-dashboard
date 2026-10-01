<template>
  <main class="page-container about-page">
    <section class="about-hero">
      <p class="eyebrow">PROJECT NOTES / 2026</p>
      <h1>Built for clarity.<br />Designed for the shelf.</h1>
      <p class="about-lead">
        NOIRARY adalah mini dashboard perpustakaan untuk UTS Web Application Development.
        Frontend dibangun dengan Vue 3 Composition API, sementara REST API menggunakan FastAPI.
      </p>
    </section>

    <section class="about-grid">
      <article class="about-card">
        <span>01</span>
        <h2>Frontend</h2>
        <p>
          Vue 3 Composition API, Vue Router, computed filter/sort/statistics, Fetch API,
          async/await, dan state loading/error/empty.
        </p>
      </article>
      <article class="about-card">
        <span>02</span>
        <h2>Backend</h2>
        <p>
          FastAPI, Pydantic validation, CORS, seed JSON ke list Python in-memory, serta
          endpoint GET, POST, PUT, dan DELETE.
        </p>
      </article>
      <article class="about-card">
        <span>03</span>
        <h2>Stock Rules</h2>
        <p>
          Stok Habis = 0, Menipis = 1–3, dan Tersedia = 4 atau lebih. Threshold yang sama
          digunakan pada badge dan ringkasan.
        </p>
      </article>
    </section>
  </main>
</template>
