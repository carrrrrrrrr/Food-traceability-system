<template>
  <div class="my-container">
    <div class="my-sidebar">
      <h2>个人中心</h2>
      <!-- 根据用户身份显示不同的导航项 -->
      <div class="sidebar-nav">
        <!-- 所有用户都有的导航项 -->
        <router-link to="/my/myinfo" class="nav-item">个人信息</router-link>
        
        <!-- 只有消费者才有的导航项 -->
        <router-link v-if="userIdentity === '消费者'" to="/my/favorites" class="nav-item">我的收藏</router-link>
        
        <!-- 只有商家和农户才有的导航项 -->
        <router-link v-if="userIdentity === '商户' || userIdentity === '农户'" to="/my/myfoods" class="nav-item">我的产品</router-link>
        <router-link v-if="userIdentity === '商户' || userIdentity === '农户'" to="/my/myworkingtogether" class="nav-item">我的合作伙伴</router-link>
        
        <!-- 只有农户才有的导航项 -->
        <router-link v-if="userIdentity === '农户'" to="/my/myingredients" class="nav-item">我的农产</router-link>
      </div>
    </div>
    
    <div class="my-content">
      <!-- 子路由视图 -->
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 用户身份
const userIdentity = ref('');

// 在组件挂载时获取用户信息
onMounted(() => {
  const userInfo = localStorage.getItem('currentUser');
  if (userInfo) {
    try {
      const user = JSON.parse(userInfo);
      userIdentity.value = user.identity;
      console.log('用户身份:', userIdentity.value);
    } catch (error) {
      console.error('解析用户信息失败', error);
    }
  }
});
</script>

<style scoped>
.my-container {
  display: flex;
  min-height: calc(100vh - 150px); /* 减去头部和底部的高度 */
}

.my-sidebar {
  width: 200px;
  background-color: #f5f7fa;
  padding: 20px;
  border-right: 1px solid #e6e6e6;
}

.my-sidebar h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #333;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
}

.nav-item {
  padding: 10px 15px;
  margin-bottom: 5px;
  color: #333;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background-color: #e6f7ff;
}

.nav-item.router-link-active {
  background-color: #1976d2;
  color: white;
}

.my-content {
  flex: 1;
  padding: 20px;
}
</style>