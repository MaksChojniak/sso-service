<script setup lang="ts">
import AuthLayout from '@/shared/ui/auth-layout/AuthLayout.vue'
import ResetPasswordForm from '@/features/reset-password/ui/ResetPasswordForm.vue'
</script>

<template>
  <AuthLayout title="Reset your password" description="Use the code sent to your email to set a new password.">
    <ResetPasswordForm />
    <template #footer>
      <RouterLink class="card-link" to="/login">Back to sign in</RouterLink>
    </template>
  </AuthLayout>
</template>

<style scoped>
.card-link {
  color: var(--color-primary);
  font-weight: 700;
  text-decoration: none;
}

.card-link:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}
</style>
