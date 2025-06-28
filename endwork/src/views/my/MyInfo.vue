<template>
  <div class="my-info">
    <h2>个人信息</h2>
    <el-form :model="userForm" :rules="rules" ref="formRef" label-width="100px" v-if="userLoaded">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="userForm.username" placeholder="请输入用户名"></el-input>
      </el-form-item>
      
      <el-form-item label="账号" prop="account">
        <el-input v-model="userForm.account" placeholder="请输入账号"></el-input>
        <div class="form-tip">修改账号后需要重新登录</div>
      </el-form-item>
      
      <el-form-item label="身份">
        <el-input v-model="userForm.identity" disabled></el-input>
      </el-form-item>
      
      <el-form-item label="修改密码" prop="password">
        <el-input 
          v-model="userForm.password" 
          type="password" 
          placeholder="不修改请留空" 
          show-password
        ></el-input>
      </el-form-item>
      
      <el-form-item label="确认密码" prop="confirmPassword" v-if="userForm.password">
        <el-input 
          v-model="userForm.confirmPassword" 
          type="password" 
          placeholder="请再次输入密码" 
          show-password
        ></el-input>
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="saveUserInfo" :loading="loading">保存修改</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
    <div v-else class="loading">加载中...</div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { user } from '../../api/api';

const router = useRouter();
const formRef = ref(null);
const userLoaded = ref(false);
const loading = ref(false);
const originalAccount = ref('');

// 表单数据
const userForm = reactive({
  id: '',
  username: '',
  account: '',
  identity: '',
  password: '',
  confirmPassword: ''
});

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  account: [
    { required: true, message: '请输入账号', trigger: 'blur' },
    { min: 4, max: 20, message: '长度在 4 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    {
      validator: (rule, value, callback) => {
        if (userForm.password && value !== userForm.password) {
          callback(new Error('两次输入密码不一致'));
        } else {
          callback();
        }
      },
      trigger: 'blur'
    }
  ]
};

onMounted(() => {
  loadUserInfo();
});

// 加载用户信息
const loadUserInfo = () => {
  const userInfo = localStorage.getItem('currentUser');
  if (userInfo) {
    try {
      const userData = JSON.parse(userInfo);
      userForm.id = userData.id;
      userForm.username = userData.username;
      userForm.account = userData.account;
      userForm.identity = userData.identity;
      originalAccount.value = userData.account; // 保存原始账号用于比较
      userLoaded.value = true;
    } catch (error) {
      console.error('解析用户信息失败', error);
      ElMessage.error('获取用户信息失败');
    }
  }
};

// 保存用户信息
const saveUserInfo = async () => {
  if (!formRef.value) return;
  
  try {
    await formRef.value.validate();
    
    loading.value = true;
    
    // 准备要更新的数据
    const updateData = {
      id: userForm.id,
      username: userForm.username,
      account: userForm.account
    };
    
    // 如果修改了密码，添加到更新数据中
    if (userForm.password) {
      updateData.password = userForm.password;
    }
    
    // 调用更新接口
    const res = await user.updateInfo(updateData);
    
    if (res.status === 'success') {
      ElMessage.success('保存成功');
      
      // 检查是否修改了账号
      if (userForm.account !== originalAccount.value) {
        ElMessage.warning('账号已修改，请重新登录');
        // 清除本地存储的用户信息
        localStorage.removeItem('currentUser');
        // 延迟跳转到登录页
        setTimeout(() => {
          router.push('/login');
        }, 1500);
      } else {
        // 更新本地存储的用户信息
        const userInfo = JSON.parse(localStorage.getItem('currentUser'));
        userInfo.username = userForm.username;
        userInfo.account = userForm.account;
        localStorage.setItem('currentUser', JSON.stringify(userInfo));
      }
    } else {
      // 处理错误情况
      if (res.message.includes('账号不可使用') || res.message.includes('已存在')) {
        ElMessage.error('账号已被使用，请更换其他账号');
      } else {
        ElMessage.error(res.message || '保存失败');
      }
    }
  } catch (error) {
    console.error(error);
    ElMessage.error('表单验证失败，请检查输入');
  } finally {
    loading.value = false;
  }
};

// 重置表单
const resetForm = () => {
  if (formRef.value) {
    formRef.value.resetFields();
    loadUserInfo(); // 重新加载用户信息
  }
};
</script>

<style scoped>
.my-info {
  max-width: 600px;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #999;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style>