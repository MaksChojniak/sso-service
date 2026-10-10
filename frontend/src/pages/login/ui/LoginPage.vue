<script setup lang="ts">
import AuthLayout from '@/shared/ui/auth-layout/AuthLayout.vue'
import SignInForm from '@/features/sign-in/ui/SignInForm.vue'
</script>

<template>
  <AuthLayout title="Welcome back" description="Sign in to continue to your account.">
    <SignInForm />
    <template #footer>
      <span>Don't have an account?</span>
      <RouterLink class="card-link" to="/register">Create one!</RouterLink>
    </template>
  </AuthLayout>
</template>

<style scoped>
.card-link {
  margin-left: 5px;
  color: var(--color-primary);
  font-weight: 700;
  text-decoration: none;
}

.card-link:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}
</style>
