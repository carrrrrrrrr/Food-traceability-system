<template>
  <div class="ingredient-card">
    <h3>{{ ingredient.name }}</h3>
    <div class="ingredient-type" v-if="ingredient.type">种类: {{ ingredient.type }}</div>
    <div class="ingredient-info">{{ ingredient.description || '暂无描述' }}</div>
    
    <div class="ingredient-times">
      <div v-if="ingredient.farming_time">养殖时间: {{ formatDateTime(ingredient.farming_time) }}</div>
      <div v-if="ingredient.production_time">出产时间: {{ formatDateTime(ingredient.production_time) }}</div>
    </div>
    
    <div class="ingredient-images">
      <div v-if="ingredient.planting_image" class="image-item">
        <div class="image-label">种植图片:</div>
        <img :src="getImageUrl(ingredient.planting_image)" alt="种植图片" class="thumbnail" @click="showImage(getImageUrl(ingredient.planting_image))">
      </div>
      
      <div v-if="ingredient.growing_image" class="image-item">
        <div class="image-label">生长图片:</div>
        <img :src="getImageUrl(ingredient.growing_image)" alt="生长图片" class="thumbnail" @click="showImage(getImageUrl(ingredient.growing_image))">
      </div>
      
      <div v-if="ingredient.production_image" class="image-item">
        <div class="image-label">出产图片:</div>
        <img :src="getImageUrl(ingredient.production_image)" alt="出产图片" class="thumbnail" @click="showImage(getImageUrl(ingredient.production_image))">
      </div>
      
      <div v-if="ingredient.quality_report_image" class="image-item">
        <div class="image-label">质检报告:</div>
        <img :src="getImageUrl(ingredient.quality_report_image)" alt="质检报告" class="thumbnail" @click="showImage(getImageUrl(ingredient.quality_report_image))">
      </div>
    </div>
    
    <!-- 添加操作按钮 -->
    <div class="ingredient-actions">
      <button class="edit-btn" @click="$emit('edit', ingredient)">编辑</button>
      <button class="delete-btn" @click="confirmDelete">删除</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  ingredient: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['show-image', 'delete', 'edit']);

// 获取图片URL
const getImageUrl = (path) => {
  if (!path) return '';
  return `http://localhost:5000/${path}`;
};

// 显示大图
const showImage = (url) => {
  emit('show-image', url);
};

// 确认删除
const confirmDelete = () => {
  if (confirm(`确定要删除原料 "${props.ingredient.name}" 吗？`)) {
    emit('delete', props.ingredient.id);
  }
};

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '';
  const date = new Date(dateTimeStr);
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
};
</script>

<style scoped>
.ingredient-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 15px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.ingredient-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.ingredient-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
}

.ingredient-type {
  color: #666;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.ingredient-info {
  color: #555;
  margin-bottom: 15px;
  font-size: 0.95rem;
}

.ingredient-times {
  color: #666;
  margin-bottom: 15px;
  font-size: 0.9rem;
}

.ingredient-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 10px;
  margin-bottom: 15px;
}

.image-item {
  margin-bottom: 10px;
}

.image-label {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 5px;
}

.thumbnail {
  width: 100%;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.2s;
}

.thumbnail:hover {
  transform: scale(1.05);
}

/* 添加操作按钮样式 */
.ingredient-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.edit-btn {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.edit-btn:hover {
  background-color: #0b7dda;
}

.delete-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.delete-btn:hover {
  background-color: #d32f2f;
}
</style>