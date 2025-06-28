<template>
  <div class="my-working-together">
    <h2>我的合作伙伴</h2>
    
    <!-- 搜索区域 -->
    <div class="search-section">
      <h3>{{ searchTitle }}</h3>
      <div class="search-box">
        <el-input
          v-model="searchKeyword"
          placeholder="输入用户名搜索"
          class="search-input"
          @keyup.enter="searchUsers"
        ></el-input>
        <el-button type="primary" @click="searchUsers">搜索</el-button>
      </div>
      
      <!-- 搜索结果 -->
      <div v-if="searchResults.length > 0" class="search-results">
        <el-table :data="searchResults" style="width: 100%">
          <el-table-column prop="id" label="ID" width="80"></el-table-column>
          <el-table-column prop="username" label="用户名"></el-table-column>
          <el-table-column prop="identity" label="身份"></el-table-column>
          <el-table-column label="状态" width="120">
            <template #default="scope">
              <el-tag v-if="scope.row.status === 'partner'" type="success">已合作</el-tag>
              <el-tag v-else-if="scope.row.status === 'pending'" type="warning">请求中</el-tag>
              <el-tag v-else-if="scope.row.status === 'rejected'" type="danger">已拒绝</el-tag>
              <el-button 
                v-else
                type="primary" 
                size="small" 
                @click="sendRequest(scope.row.id)"
              >
                发送请求
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <el-empty v-else-if="hasSearched" description="未找到匹配的用户"></el-empty>
    </div>
    
    <!-- 收到的请求 -->
    <div class="requests-section" v-if="receivedRequests.length > 0">
      <h3>待确认的合作请求</h3>
      <el-table :data="receivedRequests" style="width: 100%">
        <el-table-column prop="sender_id" label="ID" width="80"></el-table-column>
        <el-table-column prop="sender_username" label="用户名"></el-table-column>
        <el-table-column prop="sender_identity" label="身份"></el-table-column>
        <el-table-column prop="created_at" label="请求时间" width="180"></el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button 
              type="success" 
              size="small" 
              @click="respondToRequest(scope.row.request_id, 'accept')"
            >
              接受
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="respondToRequest(scope.row.request_id, 'reject')"
            >
              拒绝
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    
    <!-- 合作伙伴列表 -->
    <div class="partners-section">
      <h3>合作伙伴列表</h3>
      <el-table v-if="partners.length > 0" :data="partners" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="username" label="用户名"></el-table-column>
        <el-table-column prop="account" label="账号"></el-table-column>
        <el-table-column prop="identity" label="身份"></el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button 
              type="danger" 
              size="small" 
              @click="removePartner(scope.row.id)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="暂无合作伙伴"></el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { user } from '../../api/api';

// 当前用户信息
const currentUser = ref(null);

// 搜索相关
const searchKeyword = ref('');
const searchResults = ref([]);
const hasSearched = ref(false);

// 合作伙伴列表
const partners = ref([]);

// 收到的请求
const receivedRequests = ref([]);

// 根据用户身份计算搜索标题
const searchTitle = computed(() => {
  if (currentUser.value?.identity === '商户') {
    return '搜索农户';
  } else if (currentUser.value?.identity === '农户') {
    return '搜索商户';
  }
  return '搜索用户';
});

// 初始化
onMounted(async () => {
  // 获取当前用户信息
  const userInfo = localStorage.getItem('currentUser');
  if (userInfo) {
    try {
      currentUser.value = JSON.parse(userInfo);
      // 加载合作伙伴列表
      await loadPartners();
      // 加载收到的请求
      await loadReceivedRequests();
    } catch (error) {
      console.error('解析用户信息失败', error);
    }
  }
});

// 加载合作伙伴列表
async function loadPartners() {
  try {
    const response = await user.getPartners(currentUser.value.id);
    if (response.status === 'success') {
      partners.value = response.data;
    } else {
      ElMessage.error(response.message || '获取合作伙伴列表失败');
    }
  } catch (error) {
    console.error('获取合作伙伴列表失败', error);
    ElMessage.error('获取合作伙伴列表失败，请稍后重试');
  }
}

// 加载收到的请求
async function loadReceivedRequests() {
  try {
    const response = await user.getReceivedRequests(currentUser.value.id);
    if (response.status === 'success') {
      receivedRequests.value = response.data;
    } else {
      ElMessage.error(response.message || '获取合作请求失败');
    }
  } catch (error) {
    console.error('获取合作请求失败', error);
    ElMessage.error('获取合作请求失败，请稍后重试');
  }
}

// 搜索用户
async function searchUsers() {
  if (!searchKeyword.value.trim()) {
    ElMessage.warning('请输入搜索关键词');
    return;
  }
  
  try {
    const response = await user.searchUsers(searchKeyword.value, currentUser.value.id);
    if (response.status === 'success') {
      searchResults.value = response.data;
      hasSearched.value = true;
    } else {
      ElMessage.error(response.message || '搜索用户失败');
    }
  } catch (error) {
    console.error('搜索用户失败', error);
    ElMessage.error('搜索用户失败，请稍后重试');
  }
}

// 发送合作请求
async function sendRequest(partnerId) {
  try {
    const response = await user.sendPartnerRequest(currentUser.value.id, partnerId);
    if (response.status === 'success') {
      ElMessage.success('合作请求已发送，等待对方确认');
      // 更新搜索结果中的状态
      const index = searchResults.value.findIndex(item => item.id === partnerId);
      if (index !== -1) {
        searchResults.value[index].status = 'pending';
      }
    } else {
      ElMessage.error(response.message || '发送合作请求失败');
    }
  } catch (error) {
    console.error('发送合作请求失败', error);
    ElMessage.error('发送合作请求失败，请稍后重试');
  }
}

// 响应合作请求
async function respondToRequest(requestId, action) {
  try {
    const response = await user.respondToRequest(requestId, currentUser.value.id, action);
    if (response.status === 'success') {
      ElMessage.success(action === 'accept' ? '已接受合作请求' : '已拒绝合作请求');
      // 重新加载收到的请求
      await loadReceivedRequests();
      // 如果接受了请求，重新加载合作伙伴列表
      if (action === 'accept') {
        await loadPartners();
      }
    } else {
      ElMessage.error(response.message || '处理合作请求失败');
    }
  } catch (error) {
    console.error('处理合作请求失败', error);
    ElMessage.error('处理合作请求失败，请稍后重试');
  }
}

// 删除合作伙伴
async function removePartner(partnerId) {
  try {
    // 确认删除
    await ElMessageBox.confirm('确定要删除该合作伙伴吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    
    const response = await user.removePartner(currentUser.value.id, partnerId);
    if (response.status === 'success') {
      ElMessage.success('删除合作伙伴成功');
      // 更新搜索结果中的状态
      const index = searchResults.value.findIndex(item => item.id === partnerId);
      if (index !== -1) {
        searchResults.value[index].status = 'none';
      }
      // 重新加载合作伙伴列表
      await loadPartners();
    } else {
      ElMessage.error(response.message || '删除合作伙伴失败');
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除合作伙伴失败', error);
      ElMessage.error('删除合作伙伴失败，请稍后重试');
    }
  }
}
</script>

<style scoped>
.my-working-together {
  padding: 20px;
}

.search-section, .partners-section, .requests-section {
  margin-bottom: 30px;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.8rem;
  color: #333;
}

h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.4rem;
  color: #333;
}

.search-box {
  display: flex;
  margin-bottom: 20px;
}

.search-input {
  margin-right: 10px;
}

.search-results {
  margin-top: 20px;
}
</style>