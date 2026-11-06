<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string
    description: string
    eyebrow?: string
    brandSuffix?: string
    brandTo?: string
    brandLabel?: string
  }>(),
  {
    brandTo: '/login',
    brandLabel: 'mk.dev home',
  },
)
</script>

<template>
  <main class="auth-shell">
    <section class="auth-card" aria-labelledby="auth-title">
      <RouterLink class="brand" :to="brandTo" :aria-label="brandLabel">
        <span class="brand-mark" aria-hidden="true">
          <span></span><span></span><span></span><span></span>
        </span>
        <span>
          mk.dev <span v-if="brandSuffix" class="brand-suffix">{{ brandSuffix }}</span>
        </span>
      </RouterLink>
      <span v-if="eyebrow" class="eyebrow">{{ eyebrow }}</span>
      <h1 id="auth-title">{{ title }}</h1>
      <p class="card-description">{{ description }}</p>
      <slot />
      <div v-if="$slots.note" class="card-note">
        <slot name="note" />
      </div>
      <div v-if="$slots.footer" class="card-footer">
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
  background:
    radial-gradient(ellipse at 50% 0%, rgb(90 98 232 / 8%), transparent 48%),
    #f6f7fb;
}

.auth-card {
  width: min(100%, 420px);
  padding: 38px;
  border: 1px solid #e8eaf2;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 18px 55px rgb(25 36 59 / 8%);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: var(--color-ink);
  font-size: 19px;
  font-weight: 750;
  letter-spacing: -0.5px;
  text-decoration: none;
}

.brand-suffix {
  color: var(--color-muted);
  font-weight: 500;
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

.eyebrow {
  display: block;
  margin-top: 42px;
  color: var(--color-primary);
  font-size: 10px;
  font-weight: 750;
  letter-spacing: 1.4px;
}

.auth-card h1 {
  margin: 10px 0 8px;
  color: var(--color-ink);
  font-size: 27px;
  font-weight: 650;
  letter-spacing: -0.8px;
}

.card-description {
  margin: 0 0 28px;
  color: var(--color-muted);
  font-size: 13px;
}

.card-footer {
  margin-top: 22px;
  color: #505b70;
  font-size: 13px;
}

.card-note {
  margin-top: 22px;
  color: var(--color-muted);
  font-size: 11px;
  text-align: center;
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
    border: 0;
    border-radius: 0;
    box-shadow: none;
  }

  .page-footer {
    margin-top: auto;
    padding: 0 24px;
  }
}
</style>
