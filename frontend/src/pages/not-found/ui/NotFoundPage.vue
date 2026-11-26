<script setup lang="ts">
import { RouterLink } from 'vue-router'
import AuthLayout from '@/shared/ui/auth-layout/AuthLayout.vue'
</script>

<template>
  <AuthLayout
    eyebrow="404 • PAGE NOT FOUND"
    title="Page not found"
    description="The page you are looking for does not exist or has not been created yet."
  >
    <div class="status-actions">
      <RouterLink class="action-primary" to="/login">Go to Sign In</RouterLink>
      <RouterLink class="action-secondary" to="/admin/login">Admin Sign In</RouterLink>
    </div>
  </AuthLayout>
</template>

<style scoped>
.status-actions {
  display: grid;
  gap: 10px;
}

.action-primary,
.action-secondary {
  display: flex;
  min-height: 44px;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition:
    background 150ms ease,
    border-color 150ms ease,
    opacity 150ms ease;
}

.action-primary {
  background: var(--color-primary);
  color: #fff;
}

.action-primary:hover {
  background: var(--color-primary-dark);
}

.action-secondary {
  border: 1px solid #dfe3ed;
  background: #fff;
  color: #59657b;
}

.action-secondary:hover {
  background: #f5f6fa;
  color: var(--color-ink);
}
</style>
