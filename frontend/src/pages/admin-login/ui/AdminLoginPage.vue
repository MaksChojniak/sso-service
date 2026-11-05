<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const passwordVisible = ref(false)

function handleSubmit() {
  void router.push('/admin')
}
</script>

<template>
  <main class="admin-login">
    <section class="login-card" aria-labelledby="admin-login-title">
      <RouterLink class="brand" to="/admin/login" aria-label="mk.dev admin">
        <span class="brand-mark" aria-hidden="true">
          <span></span><span></span><span></span><span></span>
        </span>
        <span>mk.dev <span class="brand-suffix">admin</span></span>
      </RouterLink>

      <div class="login-heading">
        <span class="eyebrow">ADMINISTRATION</span>
        <h1 id="admin-login-title">Welcome back</h1>
        <p>Sign in to manage your workspace.</p>
      </div>

      <form class="login-form" @submit.prevent="handleSubmit">
        <label class="field" for="admin-email">
          <span>Email address</span>
          <input
            id="admin-email"
            type="email"
            name="email"
            placeholder="you@example.com"
            autocomplete="username"
            required
          />
        </label>

        <label class="field" for="admin-password">
          <span>Password</span>
          <span class="password-input">
            <input
              id="admin-password"
              :type="passwordVisible ? 'text' : 'password'"
              name="password"
              placeholder="Enter your password"
              autocomplete="current-password"
              required
            />
            <button
              class="visibility-toggle"
              type="button"
              :aria-label="passwordVisible ? 'Hide password' : 'Show password'"
              @click="passwordVisible = !passwordVisible"
            >
              {{ passwordVisible ? 'Hide' : 'Show' }}
            </button>
          </span>
        </label>

        <button class="submit-button" type="submit">Sign in</button>
      </form>

      <p class="login-note">Authentication will be connected to Django later.</p>
    </section>
    <footer class="login-footer">© 2026 mk.dev</footer>
  </main>
</template>

<style scoped>
.admin-login {
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

.login-card {
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

.brand-suffix {
  color: var(--color-muted);
  font-weight: 500;
}

.login-heading {
  margin: 42px 0 28px;
}

.eyebrow {
  color: var(--color-primary);
  font-size: 10px;
  font-weight: 750;
  letter-spacing: 1.4px;
}

h1 {
  margin: 10px 0 8px;
  color: var(--color-ink);
  font-size: 27px;
  letter-spacing: -0.8px;
}

.login-heading p,
.login-note {
  color: var(--color-muted);
  font-size: 13px;
}

.login-heading p {
  margin: 0;
}

.login-form {
  display: grid;
  gap: 20px;
}

.field {
  display: grid;
  gap: 8px;
  color: #36425a;
  font-size: 12px;
  font-weight: 650;
}

.field input {
  width: 100%;
  height: 44px;
  padding: 0 12px;
  border: 1px solid #dfe3ed;
  border-radius: 6px;
  outline: none;
  background: #fff;
  color: var(--color-ink);
  font-size: 13px;
  font-weight: 400;
  transition:
    border-color 150ms ease,
    box-shadow 150ms ease;
}

.field input::placeholder {
  color: #a6adbb;
}

.field input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgb(90 98 232 / 12%);
}

.password-input {
  position: relative;
}

.password-input input {
  padding-right: 60px;
}

.visibility-toggle {
  position: absolute;
  top: 50%;
  right: 12px;
  padding: 4px 0;
  transform: translateY(-50%);
  border: 0;
  background: transparent;
  color: #77839a;
  cursor: pointer;
  font-size: 11px;
  font-weight: 650;
}

.submit-button {
  height: 44px;
  margin-top: 2px;
  border: 0;
  border-radius: 6px;
  background: var(--color-primary);
  color: #fff;
  cursor: pointer;
  font-size: 13px;
  font-weight: 650;
  transition: background 150ms ease;
}

.submit-button:hover {
  background: var(--color-primary-dark);
}

.submit-button:focus-visible,
.visibility-toggle:focus-visible {
  outline: 3px solid rgb(90 98 232 / 35%);
  outline-offset: 3px;
}

.login-note {
  margin: 22px 0 0;
  text-align: center;
  font-size: 11px;
}

.login-footer {
  color: #687386;
  font-size: 11px;
}

@media (max-width: 520px) {
  .admin-login {
    justify-content: flex-start;
    gap: 18px;
    padding: 0 0 18px;
    background: #fff;
  }

  .login-card {
    width: 100%;
    padding: 32px 24px 26px;
    border: 0;
    border-radius: 0;
    box-shadow: none;
  }

  .login-footer {
    margin-top: auto;
  }
}
</style>
