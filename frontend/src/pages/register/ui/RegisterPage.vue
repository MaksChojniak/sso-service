<script setup lang="ts">
import AuthLayout from '@/shared/ui/auth-layout/AuthLayout.vue'
import SignUpForm from '@/features/sign-up/ui/SignUpForm.vue'
</script>

<template>
  <AuthLayout title="Create your account" description="A few details and you’re ready to go.">
    <SignUpForm />
    <template #footer>
      <span>Already have an account?</span>
      <RouterLink class="card-link" to="/login">Sign in</RouterLink>
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
