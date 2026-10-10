<script setup lang="ts">
defineProps<{
  title: string
  description: string
}>()
</script>

<template>
  <main class="auth-shell">
    <section class="auth-card" aria-labelledby="auth-title">
      <RouterLink class="brand" to="/login" aria-label="mk.dev home">
        <span class="brand-mark" aria-hidden="true">
          <span></span><span></span><span></span><span></span>
        </span>
        <span>mk.dev</span>
      </RouterLink>
      <h1 id="auth-title">{{ title }}</h1>
      <p class="card-description">{{ description }}</p>
      <slot />
      <div class="card-footer">
        <slot name="footer" />
      </div>
    </section>
    <footer class="page-footer">© 2026 mk.dev</footer>
  </main>
</template>

<style scoped>
.auth-shell {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 32px 20px 18px;
}

.auth-card {
  width: min(100%, 440px);
  padding: 42px 44px 36px;
  background: #fff;
  box-shadow: 0 2px 8px rgb(0 0 0 / 12%);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 30px;
  color: var(--color-ink);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.6px;
  text-decoration: none;
}

.brand-dot {
  color: var(--color-primary);
}

.brand-mark {
  display: grid;
  width: 21px;
  height: 21px;
  grid-template-columns: repeat(2, 1fr);
  gap: 2px;
}

.brand-mark span {
  background: var(--color-primary);
}

.brand-mark span:nth-child(2),
.brand-mark span:nth-child(3) {
  opacity: 0.68;
}

.auth-card h1 {
  margin: 0;
  color: var(--color-ink);
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -0.6px;
  line-height: 1.3;
}

.card-description {
  margin: 12px 0 26px;
  color: var(--color-muted);
  font-size: 14px;
  line-height: 1.55;
}

.card-footer {
  margin-top: 24px;
  color: #505b70;
  font-size: 13px;
}

.page-footer {
  color: #687386;
  font-size: 11px;
}

@media (max-width: 520px) {
  .auth-shell {
    justify-content: flex-start;
    gap: 18px;
    padding: 0 0 18px;
    background: #fff;
  }

  .auth-card {
    width: 100%;
    padding: 32px 24px 26px;
    box-shadow: none;
  }

  .brand {
    margin-bottom: 32px;
  }

  .page-footer {
    margin-top: auto;
    padding: 0 24px;
  }
}
</style>
