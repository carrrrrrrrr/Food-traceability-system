<template>
  <div class="foods">
    <h1>食品列表</h1>
    
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="foods.length === 0" class="no-data">
      <p>暂无食品数据</p>
    </div>
    
    <div v-else class="food-list">
      <div v-for="food in foods" :key="food.id" class="food-item">
        <div class="food-header">
          <h2>{{ food.name }}</h2>
          <div class="food-merchant">制作商户: {{ food.merchant_name }}</div>
        </div>
        
        <div class="food-details">
          <div class="food-info-section">
            <div class="food-category" v-if="food.category">分类: {{ food.category }}</div>
            <div class="food-price">价格: ¥{{ food.prise }} <span class="unit">{{ food.poundage }}</span></div>
            <div class="food-description">{{ food.info || '暂无描述' }}</div>
            <div class="food-stock">库存: {{ food.num }}</div>
            <div class="food-cooking-time" v-if="food.cooking_time">制作时间: {{ formatDateTime(food.cooking_time) }}</div>
          </div>
          
          <div class="food-ingredients" v-if="food.ingredients && food.ingredients.length > 0">
            <h3>原材料:</h3>
            <ul class="ingredients-list">
              <li v-for="ingredient in food.ingredients" :key="ingredient.id" @click="showIngredientDetail(ingredient)" class="ingredient-item">
                {{ ingredient.name }} {{ ingredient.amount }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 原料详情弹窗 -->
    <div v-if="showIngredientModal" class="modal-overlay" @click="closeIngredientModal">
      <div class="modal-content" @click.stop>
        <button class="close-btn" @click="closeIngredientModal">×</button>
        
        <div v-if="selectedIngredient" class="ingredient-detail">
          <h2>{{ selectedIngredient.name }} 详情</h2>
          <div class="farmer-info">农户: {{ selectedIngredient.farmer_name }}</div>
          
          <div class="ingredient-info">
            <div v-if="selectedIngredient.type" class="info-item">种类: {{ selectedIngredient.type }}</div>
            <div class="info-item">描述: {{ selectedIngredient.description || '暂无描述' }}</div>
            <div v-if="selectedIngredient.farming_time" class="info-item">养殖/种植时间: {{ formatDateTime(selectedIngredient.farming_time) }}</div>
            <div v-if="selectedIngredient.production_time" class="info-item">出产时间: {{ formatDateTime(selectedIngredient.production_time) }}</div>
          </div>
          
          <div class="ingredient-images">
            <div v-if="selectedIngredient.planting_image" class="image-container">
              <h3>种植图片</h3>
              <img :src="getImageUrl(selectedIngredient.planting_image)" alt="种植图片" @click="showFullImage(getImageUrl(selectedIngredient.planting_image))">
            </div>
            
            <div v-if="selectedIngredient.growing_image" class="image-container">
              <h3>生长图片</h3>
              <img :src="getImageUrl(selectedIngredient.growing_image)" alt="生长图片" @click="showFullImage(getImageUrl(selectedIngredient.growing_image))">
            </div>
            
            <div v-if="selectedIngredient.production_image" class="image-container">
              <h3>出产图片</h3>
              <img :src="getImageUrl(selectedIngredient.production_image)" alt="出产图片" @click="showFullImage(getImageUrl(selectedIngredient.production_image))">
            </div>
            
            <div v-if="selectedIngredient.quality_report_image" class="image-container">
              <h3>质检报告</h3>
              <img :src="getImageUrl(selectedIngredient.quality_report_image)" alt="质检报告" @click="showFullImage(getImageUrl(selectedIngredient.quality_report_image))">
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 全屏图片查看 -->
    <div v-if="showFullImageModal" class="fullimage-overlay" @click="closeFullImage">
      <div class="fullimage-container">
        <img :src="fullImageUrl" alt="查看大图">
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { food } from '../api/api';

const foods = ref([]);
const loading = ref(true);
const showIngredientModal = ref(false);
const selectedIngredient = ref(null);
const showFullImageModal = ref(false);
const fullImageUrl = ref('');

// 获取所有食品
const getAllFoods = async () => {
  try {
    loading.value = true;
    const response = await food.getAllFoods();
    foods.value = response.data;
  } catch (error) {
    console.error('获取食品列表失败:', error);
  } finally {
    loading.value = false;
  }
};

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '';
  const date = new Date(dateTimeStr);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
};

// 获取图片URL
const getImageUrl = (path) => {
  if (!path) return '';
  return `http://localhost:5000/${path}`;
};

// 显示原料详情
const showIngredientDetail = (ingredient) => {
  selectedIngredient.value = ingredient;
  showIngredientModal.value = true;
};

// 关闭原料详情弹窗
const closeIngredientModal = () => {
  showIngredientModal.value = false;
  selectedIngredient.value = null;
};

// 显示全屏图片
const showFullImage = (url) => {
  fullImageUrl.value = url;
  showFullImageModal.value = true;
};

// 关闭全屏图片
const closeFullImage = () => {
  showFullImageModal.value = false;
};

// 页面加载时获取食品列表
onMounted(() => {
  getAllFoods();
});
</script>

<style scoped>
.foods {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.loading, .no-data {
  text-align: center;
  padding: 40px 0;
  color: #666;
}

.food-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.food-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.food-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.food-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.food-header h2 {
  margin: 0 0 5px 0;
  color: #333;
}

.food-merchant {
  font-size: 14px;
  color: #666;
}

.food-details {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.food-info-section > div {
  margin-bottom: 8px;
}

.food-category, .food-price, .food-stock, .food-cooking-time {
  font-size: 14px;
  color: #555;
}

.food-description {
  font-size: 14px;
  color: #666;
  margin: 10px 0;
}

.unit {
  font-size: 12px;
  color: #888;
}

.food-ingredients h3 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #333;
}

.ingredients-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ingredient-item {
  background-color: #f0f8ff;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.ingredient-item:hover {
  background-color: #d0e8ff;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.ingredient-detail h2 {
  margin-top: 0;
  color: #333;
}

.farmer-info {
  font-size: 16px;
  color: #555;
  margin-bottom: 15px;
}

.ingredient-info {
  margin-bottom: 20px;
}

.info-item {
  margin-bottom: 8px;
  font-size: 14px;
  color: #555;
}

.ingredient-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.image-container {
  text-align: center;
}

.image-container h3 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #555;
}

.image-container img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.2s;
}

.image-container img:hover {
  transform: scale(1.05);
}

/* 全屏图片查看 */
.fullimage-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1100;
}

.fullimage-container img {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
}
</style>