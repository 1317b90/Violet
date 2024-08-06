import { createRouter, createWebHistory } from 'vue-router'
import homeView from '../views/home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: homeView
    },
    {
      path: '/file',
      name: 'file',
      component: () => import('../views/file/index.vue')
    },
    {
      path: '/IP',
      name: 'IP',
      component: () => import('../views/IP/index.vue')
    },
    {
      path: '/itemSetup',
      name: 'itemSetup',
      component: () => import('../views/itemSetup/index.vue')
    },
    {
      path: '/RDactivate',
      name: 'RDactivate',
      component: () => import('../views/RDactivate/index.vue')
    },
    {
      path: '/highTech',
      name: 'highTech',
      component: () => import('../views/highTech/index.vue')
    },
    {
      path: '/achieve',
      name: 'achieve',
      component: () => import('../views/achieve/index.vue')
    },
    {
      path: '/innovative',
      name: 'innovative',
      component: () => import('../views/innovative/index.vue')
    },
    {
      path: '/manage',
      name: 'manage',
      component: () => import('../views/manage/index.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/login/login.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/login/register.vue')
    }
  ]
})

export default router
