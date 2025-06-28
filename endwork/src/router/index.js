import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/foods',
    name: 'Foods',
    component: () => import('../views/Foods.vue')
  },
  {
    path: '/my',
    name: 'My',
    component: () => import('../views/My.vue'),
    meta: { requiresAuth: true },  // 添加需要认证的元信息
    children: [
      {
        path: '',  // 空路径表示/my的默认子路由
        name: 'MyDefault',
        component: () => import('../views/My.vue'),
        beforeEnter: (to, from, next) => {
          // 获取用户身份
          const userInfo = localStorage.getItem('currentUser');
          if (userInfo) {
            try {
              const user = JSON.parse(userInfo);
              // 根据用户身份重定向到不同页面
              if (user.identity === '消费者') {
                next({ path: '/my/favorites' });
              } else if (user.identity === '商户' || user.identity === '农户') {
                next({ path: '/my/myfoods' });
              } else {
                // 默认情况下重定向到个人信息页
                next({ path: '/my/myinfo' });
              }
            } catch (error) {
              console.error('解析用户信息失败', error);
              next({ path: '/my/myinfo' });
            }
          } else {
            next({ path: '/my/myinfo' });
          }
        }
      },
      {
        path: 'myfoods',
        name: 'MyFoods',
        component: () => import('../views/my/MyFoods.vue')
      },
      {
        path: 'myinfo',
        name: 'MyInfo',
        component: () => import('../views/my/MyInfo.vue')
      },
      {
        path: 'favorites',
        name: 'Favorites',
        component: () => import('../views/my/Favorites.vue')
      },
      {
        path: 'myworkingtogether',
        name: 'MyWorkingTogether',
        component: () => import('../views/my/MyWorkingTogether.vue')
      }
      // 在路由配置中添加
      ,{
        path: 'myingredients',
        name: 'MyIngredients',
        component: () => import('../views/my/MyIngredients.vue'),
        meta: { requiresAuth: true }
      }
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  console.log('路由守卫触发', to.path)
  // 检查路由是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    console.log('该路由需要认证')
    // 检查用户是否已登录
    const currentUser = localStorage.getItem('currentUser')
    console.log('当前用户状态:', currentUser ? '已登录' : '未登录')
    if (!currentUser) {
      // 未登录，重定向到登录页面
      console.log('重定向到登录页')
      next({ path: '/login' })
    } else {
      // 已登录，允许访问
      console.log('允许访问受保护路由')
      next()
    }
  } else {
    // 不需要认证的路由，直接访问
    console.log('不需要认证的路由，直接访问')
    next()
  }
})

export default router