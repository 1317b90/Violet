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
      path: '/item',
      name: 'item',
      component: () => import('../views/item/index.vue')
    },
    {
      path: '/IP',
      name: 'IP',
      component: () => import('../views/IP/index.vue')
    },
    {
      path: '/setup',
      name: 'setup',
      component: () => import('../views/setup/index.vue')
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


router.beforeEach(async (to, from) => {
  const noLoginList=['login','register']

  if (
    // 检查用户是否已登录
    !sessionStorage.getItem('username') &&
    // 避免无限重定向
    !noLoginList.includes(String(to.name))
  ) {
    // 将用户重定向到登录页面
    return { name: 'login' }
  }
})


export default router
