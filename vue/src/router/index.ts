import { createRouter, createWebHistory } from 'vue-router'
import home from '../views/home.vue'
import initProposal from '../views/itemSetup/index.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: home
    },
    {
      path: '/itemSetup',
      name: 'itemSetup',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: initProposal
    }
  ]
})

export default router
