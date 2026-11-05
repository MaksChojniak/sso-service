import { createRouter, createWebHistory } from 'vue-router'

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
      component: () => import('@/pages/admin-panel/ui/AdminPanelPage.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login',
    },
  ],
})

export default router
