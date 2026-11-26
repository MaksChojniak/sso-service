<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import AuthField from '@/shared/ui/auth-field/AuthField.vue'
import AuthSubmitButton from '@/shared/ui/auth-submit-button/AuthSubmitButton.vue'
import { apiRequest } from '@/shared/api/client'

const router = useRouter()
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

async function handleSignIn() {
  errorMessage.value = ''
  isLoading.value = true

  const { data, error } = await apiRequest('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email: email.value, password: password.value }),
  })

  isLoading.value = false

  if (error) {
    errorMessage.value = error
    return
  }

  // Check if next redirect exists in URL query (e.g. from OIDC authorize flow)
  const urlParams = new URLSearchParams(window.location.search)
  const next = urlParams.get('next')
  if (next) {
    window.location.href = next
    return
  }

  void router.push('/home')
}
</script>

<template>
  <form class="auth-form" @submit.prevent="handleSignIn">
    <div v-if="errorMessage" class="error-banner">
      {{ errorMessage }}
    </div>

    <AuthField
      id="sign-in-email"
      v-model="email"
      label="Email address"
      name="email"
      placeholder="you@example.com"
      autocomplete="email"
    />

    <AuthField
      id="sign-in-password"
      v-model="password"
      label="Password"
      name="password"
      placeholder="Enter your password"
      autocomplete="current-password"
      type="password"
    />

    <div class="form-options">
      <RouterLink class="text-link" to="/reset-password">Forgot password?</RouterLink>
    </div>

    <AuthSubmitButton :disabled="isLoading">
      {{ isLoading ? 'Signing in...' : 'Login' }}
    </AuthSubmitButton>
  </form>
</template>

<style scoped>
.auth-form {
  display: grid;
  gap: 18px;
}

.error-banner {
  padding: 10px 14px;
  border-radius: 6px;
  background: #fef2f2;
  border: 1px solid #fee2e2;
  color: #b91c1c;
  font-size: 12px;
  font-weight: 500;
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  margin-top: -2px;
  font-size: 11px;
}

.text-link {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
}

.text-link:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}

.text-link:focus-visible {
  outline: 3px solid rgb(90 98 232 / 35%);
  outline-offset: 3px;
}
</style>
