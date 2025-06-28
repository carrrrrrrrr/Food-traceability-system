<template>
  <div>
    <!-- 加载中提示 -->
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    
    <!-- 无数据提示 -->
    <div v-else-if="foods.length === 0" class="no-data">
      <p>暂无产品数据，请添加新产品</p>
    </div>
    
    <!-- 产品卡片网格 -->
    <div v-else class="food-grid">
      <!-- 现有产品卡片 -->
      <FoodCard 
        v-for="food in foods" 
        :key="food.id" 
        :food="food"
        @edit="$emit('edit', food)"
        @delete="$emit('delete', food)"
      />
      
      <!-- 添加新产品卡片 -->
      <div class="food-card add-card" @click="$emit('edit', {})">
        <div class="add-icon">+</div>
        <div class="add-text">添加新产品</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import FoodCard from './FoodCard.vue';

defineProps({
  foods: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
});

defineEmits(['edit', 'delete']);
</script>

<style scoped>
/* 产品卡片网格样式 */
.food-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

/* 添加卡片样式 */
.add-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  background-color: #f5f5f5;
  border: 2px dashed #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 15px;
  transition: transform 0.3s, box-shadow 0.3s;
  height: 200px;
}

.add-card:hover {
  background-color: #e8f5e9;
  border-color: #4CAF50;
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.add-icon {
  font-size: 2rem;
  color: #4CAF50;
  margin-bottom: 10px;
}

.add-text {
  color: #4CAF50;
  font-weight: bold;
}

/* 无数据提示 */
.no-data {
  text-align: center;
  padding: 40px 0;
  color: #666;
}

/* 加载中提示 */
.loading {
  text-align: center;
  padding: 40px 0;
  color: #666;
}
</style>