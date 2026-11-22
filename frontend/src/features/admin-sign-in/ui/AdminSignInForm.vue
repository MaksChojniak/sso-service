<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthField from '@/shared/ui/auth-field/AuthField.vue'
import AuthSubmitButton from '@/shared/ui/auth-submit-button/AuthSubmitButton.vue'
import { apiRequest } from '@/shared/api/client'

const router = useRouter()
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

async function handleAdminSignIn() {
  errorMessage.value = ''
  isLoading.value = true

  const { data, error } = await apiRequest('/api/v1/admin/login', {
    method: 'POST',
    body: JSON.stringify({ email: email.value, password: password.value }),
  })

  isLoading.value = false

  if (error) {
    errorMessage.value = error
    return
  }

  void router.push('/admin')
}
</script>

<template>
  <form class="admin-sign-in-form" @submit.prevent="handleAdminSignIn">
    <div v-if="errorMessage" class="error-banner">
      {{ errorMessage }}
    </div>

    <AuthField
      id="admin-email"
      v-model="email"
      label="Email address"
      name="email"
      placeholder="you@example.com"
      autocomplete="username"
    />
    <AuthField
      id="admin-password"
      v-model="password"
      label="Password"
      name="password"
      placeholder="Enter your password"
      autocomplete="current-password"
      type="password"
    />
    <AuthSubmitButton :disabled="isLoading">
      {{ isLoading ? 'Signing in...' : 'Sign in' }}
    </AuthSubmitButton>
  </form>
</template>

<style scoped>
.admin-sign-in-form {
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
</style>

