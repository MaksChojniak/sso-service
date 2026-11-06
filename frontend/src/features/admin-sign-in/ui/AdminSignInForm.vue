<script setup lang="ts">
import AuthField from '@/shared/ui/auth-field/AuthField.vue'
import AuthSubmitButton from '@/shared/ui/auth-submit-button/AuthSubmitButton.vue'

const emit = defineEmits<{
  submit: []
}>()
</script>

<template>
  <form class="admin-sign-in-form" @submit.prevent="emit('submit')">
    <AuthField
      id="admin-email"
      label="Email address"
      name="email"
      placeholder="you@example.com"
      autocomplete="username"
    />
    <AuthField
      id="admin-password"
      label="Password"
      name="password"
      placeholder="Enter your password"
      autocomplete="current-password"
      type="password"
    />
    <AuthSubmitButton>Sign in</AuthSubmitButton>
  </form>
</template>

<style scoped>
.admin-sign-in-form {
  display: grid;
  gap: 18px;
}
</style>
