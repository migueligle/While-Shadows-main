import Vue from 'vue'
import VueRouter from 'vue-router'
import adminWhile from '@/views/administrator/index'
import Index from '@/views/index/index.vue'
import othersSettings from '@/views/administrator/othersSettings'
import settingsUsers from '@/views/administrator/settingsUsers'
import settingsProducts from '@/views/administrator/settingsProducts'
import settingsOrders from '@/views/administrator/settingsOrders'
import settingsCategories from '@/views/administrator/settingsCategories'
import signUpView from '@/components/signUp/signUp.vue'
import RecoverPasswordView from '@/components/RecoverPassword/RecoverPassword.vue'
import { jwtDecode } from 'jwt-decode'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Index
  },
  {
    path: '/admin',
    component: adminWhile,
    meta: { requiresAdmin: true }
  },
  {
    path: '/RecoverPassword',
    component: RecoverPasswordView,
    meta: { requiresSignIn: true }
  },
  {
    path: '/signUp',
    component: signUpView,
    meta: { requiresSignIn: true }
  },
  {
    path: '/admin/othersSettings',
    name: 'othersSettings',
    component: othersSettings,
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/settingsUsers',
    name: 'settingsUsers',
    component: settingsUsers,
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/settingsProducts',
    name: 'settingsProducts',
    component: settingsProducts,
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/settingsOrders',
    name: 'settingsOrders',
    component: settingsOrders,
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/settingsCategories&marker',
    name: 'settingsCategories',
    component: settingsCategories,
    meta: { requiresAdmin: true }
  },
  {
    path: '/products',
    name: 'products',
    component: () => import('@/views/products/index')
  },
  {
    path: '/Politics',
    name: 'PoliticsWhile',
    component: () => import('@/views/politics/index')
  },
  {
    path: '/frequentQuestions',
    name: 'frecuentsWhile',
    component: () => import('@/views/frequentQuestions/index')
  },
  {
    path: '/products/product/:productId',
    name: 'product_while',
    component: () => import('@/views/products/show')
  },
  {
    path: '/categories',
    name: 'categoryWhile',
    component: () => import('@/views/categories/index')
  },
  {
    path: '/categories/products/:CategoryId',
    name: 'categoryProductWhile',
    component: () => import('@/views/categories/show')
  },
  {
    path: '/user',
    name: 'userWhile',
    component: () => import('@/views/user/index'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/date',
    name: 'dateUserWhile',
    component: () => import('@/views/user/dateUser'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/direction',
    name: 'directionWhile',
    component: () => import('@/views/user/direction'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/orders',
    name: 'ordersWhile',
    component: () => import('@/views/user/orders'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/orders/show',
    name: 'orderShow',
    component: () => import('@/views/user/orderShow'),
    meta: { requiresAuth: true }
  },
  {
    path: '/shoppingCart',
    name: 'shoppingCart',
    component: () => import('@/views/shopping/index'),
    meta: { requiresAuth: true }
  },
  {
    path: '/shoppingCart/ProcessOrder',
    name: 'Process the order',
    component: () => import('@/views/shopping/show'),
    meta: { requiresAuth: true }
  },
  {
    path: '/contact',
    name: 'ContactIndex',
    component: () => import('@/views/contact/index')
  },
  {
    path: '/notfound',
    component: () => import('@/views/notfound.vue')
  },
  {
    path: '*',
    redirect: '/notfound'
  }
]

const router = new VueRouter({
  routes,
  mode: 'history',
  base: '/'
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('color')
  let isStaff = false
  if (isAuthenticated && isAuthenticated !== null) {
    const decodedToken = jwtDecode(isAuthenticated)
    isStaff = decodedToken.is_staff
  }
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/')
  } else if (to.meta.requiresAdmin && (!isStaff || isStaff === 'false')) {
    next('/')
  } else if (to.meta.requiresSignIn && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

router.onError((error) => {
  console.error('Error en la navegación:', error)
  router.push('/notfound')
})
export default router
