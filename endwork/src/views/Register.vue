<template>
  <div class="register">
    <div class="register-container">
      <h2>用户注册</h2>
      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="rules" 
        label-width="80px"
        class="register-form"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名"></el-input>
        </el-form-item>

        <el-form-item label="账号" prop="account">
          <el-input v-model="form.account" placeholder="请输入账号"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            placeholder="请输入密码"
            show-password
          ></el-input>
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input 
            v-model="form.confirmPassword" 
            type="password" 
            placeholder="请再次输入密码"
            show-password
          ></el-input>
        </el-form-item>

        <el-form-item label="身份" prop="identity">
          <el-select v-model="form.identity" placeholder="请选择身份">
            <el-option label="消费者" value="消费者"></el-option>
            <el-option label="商户" value="商户"></el-option>
            <el-option label="农户" value="农户"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleRegister" :loading="loading">注册</el-button>
          <el-button @click="goToLogin">已有账号？去登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api/api'

const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

// 表单数据
const form = reactive({
  username: '',
  account: '',
  password: '',
  confirmPassword: '',
  identity: ''
})

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
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== form.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  identity: [
    { required: true, message: '请选择身份', trigger: 'change' }
  ]
}

// 注册处理
// 注册处理
const handleRegister = async () => {
  if (!formRef.value) return
  
  try {
    // 表单验证
    await formRef.value.validate()
    
    loading.value = true
    
    // 调用注册接口
    const res = await api.auth.register({
      username: form.username,
      account: form.account,
      password: form.password,
      identity: form.identity
    })
    
    if (res.status === 'success') {
      ElMessage.success('注册成功')
      router.push('/login')
    } else {
      // 根据错误消息显示不同提示
      if (res.message === '用户名已被使用') {
        ElMessage.error('用户名已被使用，请更换其他用户名')
      } else if (res.message === '账号不可使用') {
        ElMessage.error('账号已被使用，请更换其他账号')
      } else {
        ElMessage.error(res.message || '注册失败')
      }
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('注册失败，请检查表单信息')
  } finally {
    loading.value = false
  }
}

// 跳转到登录页
const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 70px);
  background-color: #f5f7fa;
}

.register-container {
  width: 100%;
  max-width: 500px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.register-container h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
}

.register-form {
  margin-top: 20px;
}

.el-form-item:last-child {
  margin-bottom: 0;
  text-align: center;
}

.el-form-item:last-child .el-button {
  margin: 0 10px;
  min-width: 120px;
}

.el-select {
  width: 100%;
}
</style>