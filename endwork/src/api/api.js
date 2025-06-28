import axios from 'axios'

// 创建 axios 实例
const request = axios.create({
  baseURL: 'http://localhost:5000/api',  // 后端服务器地址
  timeout: 5000  // 请求超时时间
})

// 认证相关接口
export const auth = {
  // 用户登录
  login: (data) => request.post('/auth/login', data),
  // 用户注册
  register: (data) => request.post('/auth/register', data),
  // 用户登出
  logout: () => request.post('/auth/logout')
}

// 用户相关接口
export const user = {
  // 获取用户信息
  getInfo: (userId) => request.get('/user/info', { params: { id: userId } }),
  // 更新用户信息
  updateInfo: (data) => request.put('/user/info', data),
  // 注销用户
  deleteUser: (userId) => request.delete('/user/delete', { params: { id: userId } }),
  // 搜索用户（用于添加合作伙伴）
  searchUsers: (keyword, currentUserId) => request.get('/user/search', { 
    params: { keyword, current_user_id: currentUserId } 
  }),
  // 发送合作伙伴请求
  sendPartnerRequest: (userId, partnerId) => request.post('/user/partner/request', { 
    user_id: userId, 
    partner_id: partnerId 
  }),
  // 获取收到的合作伙伴请求
  getReceivedRequests: (userId) => request.get('/user/partner/requests/received', { 
    params: { user_id: userId } 
  }),
  // 响应合作伙伴请求
  respondToRequest: (requestId, userId, action) => request.post('/user/partner/request/respond', { 
    request_id: requestId, 
    user_id: userId, 
    action: action // 'accept' 或 'reject'
  }),
  // 删除合作伙伴
  removePartner: (userId, partnerId) => request.post('/user/partner/remove', { 
    user_id: userId, 
    partner_id: partnerId 
  }),
  // 获取合作伙伴列表
  getPartners: (userId) => request.get('/user/partners', { 
    params: { user_id: userId } 
  })
}

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 可以在这里添加token等认证信息
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    // 统一处理响应
    return response.data
  },
  error => {
    // 统一处理错误
    console.error('请求错误：', error)
    return Promise.reject(error)
  }
)

// 食品相关接口
export const food = {
  // 获取所有食品列表
  getAllFoods: () => request.get('/foods'),
  // 获取用户的食品列表
  getUserFoods: (userId) => request.get('/foods/user', { params: { user_id: userId } }),
  // 添加食品
  addFood: (data) => request.post('/foods', data),
  // 删除食品
  deleteFood: (foodId, userId) => request.delete(`/foods/${foodId}`, { params: { user_id: userId } }),
  // 修改食品
  updateFood: (foodId, data) => request.put(`/foods/${foodId}`, data),
}

// 原料相关接口
export const ingredient = {
  // 获取所有原料
  getIngredients: () => request.get('/ingredients'),
  // 获取用户的原料
  getUserIngredients: (userId) => request.get('/ingredients', { params: { user_id: userId } }),
  // 获取合作伙伴的原料（商户专用）
  getPartnerIngredients: (userId) => request.get('/ingredients/partners', { params: { user_id: userId } }),
  // 添加原料（使用FormData上传文件）
  addIngredient: (formData) => {
    return request.post('/ingredients', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  // 删除原料
  deleteIngredient: (ingredientId, userId) => request.delete(`/ingredients/${ingredientId}`, { params: { user_id: userId } }),
  // 修改原料（使用FormData上传文件）
  updateIngredient: (ingredientId, formData) => {
    return request.put(`/ingredients/${ingredientId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
}

export default {
  auth,
  user,
  food,
  ingredient
}