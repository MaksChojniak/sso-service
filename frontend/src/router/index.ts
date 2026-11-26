import { createRouter, createWebHistory } from 'vue-router'
import { apiRequest } from '@/shared/api/client'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login',
    },
    {
      path: '/login',
      component: () => import('@/pages/login/ui/LoginPage.vue'),
    },
    {
      path: '/register',
      component: () => import('@/pages/register/ui/RegisterPage.vue'),
    },
    {
      path: '/reset-password',
      component: () => import('@/pages/reset-password/ui/ResetPasswordPage.vue'),
    },
    {
      path: '/admin/login',
      component: () => import('@/pages/admin-login/ui/AdminLoginPage.vue'),
    },
    {
      path: '/admin',
      meta: { requiresAdmin: true },
      component: () => import('@/pages/admin-panel/ui/AdminPanelPage.vue'),
    },
    {
      path: '/not-allowed',
      name: 'not-allowed',
      component: () => import('@/pages/not-allowed/ui/NotAllowedPage.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/pages/not-found/ui/NotFoundPage.vue'),
    },
  ],
})

router.beforeEach(async (to) => {
  if (!to.meta.requiresAdmin) {
    return true
  }

  const { data, error } = await apiRequest('/api/v1/auth/me')
  if (error || !data?.authenticated) {
    return { name: 'not-allowed' }
  }

  const isAdmin = Boolean(data.user?.is_staff || data.user?.is_admin_user)
  if (!isAdmin) {
    return { name: 'not-allowed' }
  }

  return true
})

export default router
