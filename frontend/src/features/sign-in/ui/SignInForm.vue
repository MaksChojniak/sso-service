<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const passwordVisible = ref(false)
</script>

<template>
  <form class="auth-form" @submit.prevent>
    <label class="field">
      <span>Email address</span>
      <input
        type="email"
        name="email"
        placeholder="you@example.com"
        autocomplete="email"
        required
      />
    </label>

    <label class="field">
      <span>Password</span>
      <span class="password-input">
        <input
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

    <div class="form-options">
      <label class="remember-option">
        <input type="checkbox" name="remember" />
        <span>Keep me signed in</span>
      </label>
      <RouterLink class="text-link" to="/reset-password">Forgot password?</RouterLink>
    </div>

    <button class="primary-button" type="submit">Login</button>
  </form>
</template>

<style scoped>
.auth-form {
  display: grid;
  gap: 17px;
}

.field {
  display: grid;
  gap: 8px;
  color: #36425a;
  font-size: 13px;
  font-weight: 600;
}

.field input:not([type='checkbox']) {
  width: 100%;
  height: 38px;
  padding: 0 10px;
  border: 0;
  border-bottom: 1px solid #8a94a6;
  border-radius: 0;
  outline: none;
  background: #fff;
  color: var(--color-ink);
  font-size: 12px;
  font-weight: 400;
  transition:
    border-color 150ms ease,
    box-shadow 150ms ease;
}

.field input::placeholder {
  color: #a6adbb;
}

.field input:focus {
  border-color: #8188f1;
  box-shadow: 0 1px 0 var(--color-primary);
}

.password-input {
  position: relative;
}

.password-input input {
  padding-right: 61px !important;
}

.visibility-toggle {
  position: absolute;
  top: 50%;
  right: 13px;
  padding: 4px 0;
  transform: translateY(-50%);
  border: 0;
  background: transparent;
  color: #77839a;
  cursor: pointer;
  font-size: 11px;
  font-weight: 600;
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-top: -2px;
  font-size: 11px;
}

.remember-option {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #727e96;
  cursor: pointer;
}

.remember-option input {
  width: 16px;
  height: 16px;
  margin: 0;
  accent-color: var(--color-primary);
}

.text-link,
.card-link {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
}

.text-link:hover,
.card-link:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}

.primary-button {
  display: flex;
  width: 100%;
  height: 40px;
  align-items: center;
  justify-content: center;
  margin-top: 3px;
  border: 0;
  border-radius: 0;
  background: var(--color-primary);
  box-shadow: none;
  color: #fff;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition:
    transform 150ms ease,
    background 150ms ease;
}

.primary-button:hover {
  background: var(--color-primary-dark);
}

.primary-button:focus-visible,
.visibility-toggle:focus-visible,
.text-link:focus-visible {
  outline: 3px solid rgb(90 98 232 / 35%);
  outline-offset: 3px;
}
</style>
