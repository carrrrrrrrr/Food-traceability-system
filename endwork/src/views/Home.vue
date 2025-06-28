<template>
  <div class="home">
    <!-- 顶部横幅 -->
    <div class="banner">
      <el-carousel height="500px">
        <el-carousel-item v-for="(item, index) in bannerItems" :key="index">
          <div class="banner-content" :style="{ backgroundImage: `url(${item.image})` }">
            <div class="banner-text">
              <h1>{{ item.title }}</h1>
              <p>{{ item.description }}</p>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>

    <!-- 项目功能介绍区域 -->
    <div class="features">
      <h2 class="section-title">项目功能介绍</h2>
      <el-row :gutter="30">
        <el-col :span="8" v-for="(feature, index) in features" :key="index">
          <el-card class="feature-card" :body-style="{ padding: '20px' }">
            <el-icon class="feature-icon" :size="50">
              <component :is="feature.icon" />
            </el-icon>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 产品展示区 -->
    <div class="products">
      <h2 class="section-title">优质产品</h2>
      <el-row :gutter="20">
        <el-col :span="6" v-for="(product, index) in products" :key="index">
          <el-card class="product-card" :body-style="{ padding: '0px' }">
            <img :src="product.image" class="product-image">
            <div class="product-info">
              <h3>{{ product.name }}</h3>
              <p>{{ product.description }}</p>
              <el-button type="primary" plain>了解更多</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Location, Phone, Message, ShoppingCart, Box, Van } from '@element-plus/icons-vue'
// 导入 home.js 中的数据
import { bannerItems, features, products } from '../info/home.js'

// 合作伙伴
const partners = Array.from({ length: 6 }, (_, index) => ({
  logo: `https://picsum.photos/100/100?random=${index + 1}`,
  name: `合作伙伴 ${index + 1}`
}))

// 联系表单
const contactForm = reactive({
  name: '',
  email: '',
  message: ''
})
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.banner {
  margin-bottom: 60px;
}

.banner-content {
  height: 100%;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  padding: 0 100px;
}

.banner-text {
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.banner-text h1 {
  font-size: 48px;
  margin-bottom: 20px;
}

.banner-text p {
  font-size: 24px;
}

.section-title {
  text-align: center;
  margin: 60px 0 40px;
  font-size: 36px;
  color: #303133;
}

.features, .products, .partners, .contact {
  padding: 0 50px;
  margin-bottom: 80px;
}

.feature-card {
  text-align: center;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-10px);
}

.feature-icon {
  color: #409EFF;
  margin-bottom: 20px;
}

.product-card {
  overflow: hidden;
  transition: transform 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.product-info {
  padding: 20px;
  text-align: center;
}

.partner-logo {
  text-align: center;
  padding: 20px;
}

.partner-logo img {
  max-width: 100%;
  height: auto;
  transition: transform 0.3s;
}

.partner-logo img:hover {
  transform: scale(1.1);
}

.contact-info {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.contact-info h3 {
  margin-bottom: 20px;
}

.contact-info p {
  margin: 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.el-icon {
  vertical-align: middle;
}
</style>