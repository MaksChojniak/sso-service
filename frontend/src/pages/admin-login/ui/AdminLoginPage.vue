<script setup lang="ts">
import { useRouter } from 'vue-router'
import AdminSignInForm from '@/features/admin-sign-in/ui/AdminSignInForm.vue'
import AuthLayout from '@/shared/ui/auth-layout/AuthLayout.vue'

const router = useRouter()

function handleSubmit() {
  void router.push('/admin')
}
</script>

<template>
  <AuthLayout
    title="Welcome back"
    description="Sign in to manage your workspace."
    eyebrow="ADMINISTRATION"
    brand-suffix="admin"
    brand-to="/admin/login"
    brand-label="mk.dev admin"
  >
    <AdminSignInForm @submit="handleSubmit" />
    <template #note>Authentication will be connected to Django later.</template>
  </AuthLayout>
</template>
