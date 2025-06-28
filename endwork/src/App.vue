<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <div class="logo">
          <router-link to="/">
            <img src="./assets/logo.png" alt="Logo" v-if="false" />
            <span>食品管理系统</span>
          </router-link>
        </div>
        
        <div class="menu-toggle" @click="toggleMenu">
          <i class="el-icon-menu"></i>
          <el-icon><Menu /></el-icon>
        </div>
        
        <nav class="nav-menu" :class="{ 'active': menuActive }">
          <router-link to="/" class="nav-link" @click="closeMenu">首页</router-link>
          <router-link to="/foods" class="nav-link" @click="closeMenu">食品列表</router-link>
          <router-link to="/my" class="nav-link" @click="closeMenu">个人中心</router-link>
          
          <!-- 根据登录状态显示不同的内容 -->
          <div v-if="isLoggedIn" class="user-welcome">
            <span>欢迎，{{ username }}</span>
            <el-button size="small" type="text" @click="handleLogout">退出</el-button>
          </div>
          <div v-else class="auth-buttons">
            <router-link to="/login" class="btn btn-login" @click="closeMenu">登录</router-link>
            <router-link to="/register" class="btn btn-register" @click="closeMenu">注册</router-link>
          </div>
        </nav>
      </div>
    </header>
    
    <main class="main-content">
      <router-view></router-view>
    </main>
    
    <footer class="footer">
      <div class="container">
        <p>© 2025 食品管理系统 - 版权所有</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { Menu } from '@element-plus/icons-vue';

const menuActive = ref(false);
const currentUser = ref(null);

// 计算属性：检查用户是否已登录
const isLoggedIn = computed(() => !!currentUser.value);

// 计算属性：获取用户名
const username = computed(() => currentUser.value?.username || '');

// 在组件挂载时获取用户信息
onMounted(() => {
  const userInfo = localStorage.getItem('currentUser');
  if (userInfo) {
    try {
      currentUser.value = JSON.parse(userInfo);
    } catch (error) {
      console.error('解析用户信息失败', error);
    }
  }
});

// 登出功能
const handleLogout = () => {
  localStorage.removeItem('currentUser');
  currentUser.value = null;
  // 可以添加跳转到首页的逻辑
  window.location.reload(); // 刷新页面以更新状态
};

const toggleMenu = () => {
  menuActive.value = !menuActive.value;
};

const closeMenu = () => {
  menuActive.value = false;
};
</script>

<style>
:root {
  --primary-color: #1976d2;
  --primary-light: #63a4ff;
  --primary-dark: #004ba0;
  --white: #ffffff;
  --light-gray: #f5f5f5;
  --text-color: #333333;
  --shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  color: var(--text-color);
  background-color: var(--light-gray);
  line-height: 1.6;
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 头部导航样式 */
.header {
  background-color: var(--primary-color);
  color: var(--white);
  box-shadow: var(--shadow);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
}

.logo a {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--white);
  font-size: 1.5rem;
  font-weight: bold;
}

.logo img {
  height: 40px;
  margin-right: 10px;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: var(--white);
  text-decoration: none;
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover,
.router-link-active {
  background-color: var(--primary-light);
}

.auth-buttons {
  display: flex;
  gap: 10px;
  margin-left: 20px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-login {
  color: var(--white);
  border: 1px solid var(--white);
}

.btn-login:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.btn-register {
  background-color: var(--white);
  color: var(--primary-color);
}

.btn-register:hover {
  background-color: var(--light-gray);
}

.menu-toggle {
  display: none;
  cursor: pointer;
  font-size: 24px;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  padding: 30px 0;
}

/* 页脚样式 */
.footer {
  background-color: var(--primary-dark);
  color: var(--white);
  padding: 20px 0;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .menu-toggle {
    display: block;
  }

  .nav-menu {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background-color: var(--primary-color);
    flex-direction: column;
    align-items: flex-start;
    padding: 20px;
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    box-shadow: var(--shadow);
  }

  .nav-menu.active {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }

  .nav-link {
    width: 100%;
    padding: 12px;
  }

  .auth-buttons {
    width: 100%;
    margin: 10px 0 0 0;
    justify-content: center;
  }
}

.user-welcome {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: 20px;
  color: var(--white);
}

.user-welcome span {
  font-weight: 500;
}
</style>
