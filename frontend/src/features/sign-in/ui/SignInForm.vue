<script setup lang="ts">
import { RouterLink } from 'vue-router'
import AuthField from '@/shared/ui/auth-field/AuthField.vue'
import AuthSubmitButton from '@/shared/ui/auth-submit-button/AuthSubmitButton.vue'
</script>

<template>
  <form class="auth-form" @submit.prevent>
    <AuthField
      id="sign-in-email"
      label="Email address"
      name="email"
      placeholder="you@example.com"
      autocomplete="email"
    />

    <AuthField
      id="sign-in-password"
      label="Password"
      name="password"
      placeholder="Enter your password"
      autocomplete="current-password"
      type="password"
    />

    <div class="form-options">
      <RouterLink class="text-link" to="/reset-password">Forgot password?</RouterLink>
    </div>

    <AuthSubmitButton>Login</AuthSubmitButton>
  </form>
</template>

<style scoped>
.auth-form {
  display: grid;
  gap: 18px;
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  margin-top: -2px;
  font-size: 11px;
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

.text-link:focus-visible {
  outline: 3px solid rgb(90 98 232 / 35%);
  outline-offset: 3px;
}
</style>
