<script setup lang="ts">
import { ref } from 'vue'

const password = ref('')
const confirmPassword = ref('')
const passwordError = ref('')

function validatePasswords() {
  passwordError.value =
    password.value === confirmPassword.value ? '' : 'Your passwords do not match.'
}
</script>

<template>
  <form class="auth-form" @submit.prevent="validatePasswords">
    <label class="field">
      <span>Full name</span>
      <input
        type="text"
        name="name"
        placeholder="Your name"
        autocomplete="name"
        minlength="2"
        required
      />
    </label>

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
      <input
        v-model="password"
        type="password"
        name="password"
        placeholder="At least 8 characters"
        autocomplete="new-password"
        minlength="8"
        required
      />
    </label>

    <label class="field">
      <span>Confirm password</span>
      <input
        v-model="confirmPassword"
        type="password"
        name="confirmPassword"
        placeholder="Enter your password again"
        autocomplete="new-password"
        minlength="8"
        required
        @input="passwordError = ''"
      />
    </label>

    <p v-if="passwordError" class="form-error" role="alert">{{ passwordError }}</p>
    <button class="primary-button" type="submit">Create account</button>
  </form>
</template>

<style scoped>
.auth-form {
  display: grid;
  gap: 13px;
}

.field {
  display: grid;
  gap: 7px;
  color: #36425a;
  font-size: 12px;
  font-weight: 600;
}

.field input {
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
}

.field input::placeholder {
  color: #a6adbb;
}

.field input:focus {
  border-color: #8188f1;
  box-shadow: 0 1px 0 var(--color-primary);
}

.form-error {
  margin: -4px 0 0;
  color: #bc3546;
  font-size: 11px;
}

.primary-button {
  width: 100%;
  height: 40px;
  margin-top: 1px;
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

.primary-button:focus-visible {
  outline: 3px solid rgb(90 98 232 / 35%);
  outline-offset: 3px;
}
</style>
