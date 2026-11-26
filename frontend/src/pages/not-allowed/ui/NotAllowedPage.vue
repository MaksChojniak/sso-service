<script setup lang="ts">
import { RouterLink } from 'vue-router'
import AuthLayout from '@/shared/ui/auth-layout/AuthLayout.vue'
</script>

<template>
  <AuthLayout
    eyebrow="403 • ACCESS DENIED"
    brand-suffix="admin"
    brand-to="/admin/login"
    brand-label="mk.dev admin sign in"
    title="Not allowed"
    description="You do not have permission to view the admin panel. Please sign in with an administrator account."
  >
    <div class="status-actions">
      <RouterLink class="action-primary" to="/admin/login">Sign in as Admin</RouterLink>
      <RouterLink class="action-secondary" to="/login">Go to User Sign In</RouterLink>
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
