<template>
  <div class="food-card">
    <div class="card-actions">
      <button class="edit-btn" @click.stop="$emit('edit', food)">
        ✏️
      </button>
      <button class="delete-btn" @click.stop="$emit('delete', food)">
        🗑️
      </button>
    </div>
    
    <h3>{{ food.name }}</h3>
    <div class="food-category" v-if="food.category">分类: {{ food.category }}</div>
    <div class="food-price">¥{{ food.prise }} <span class="unit">{{ food.poundage }}</span></div>
    <div class="food-info">{{ food.info || '暂无描述' }}</div>
    <div class="food-stock">库存: {{ food.num }}</div>
    <div class="food-cooking-time" v-if="food.cooking_time">制作时间: {{ formatDateTime(food.cooking_time) }}</div>
    <div class="food-ingredients" v-if="food.ingredients && food.ingredients.length > 0">
      <div class="ingredients-title">原料:</div>
      <ul class="ingredients-list">
        <li v-for="ingredient in food.ingredients" :key="ingredient.id">
          {{ ingredient.name }} {{ ingredient.amount }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
defineProps({
  food: {
    type: Object,
    required: true
  }
});

defineEmits(['edit', 'delete']);

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '';
  const date = new Date(dateTimeStr);
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
};
</script>

<style scoped>
.food-card {
  position: relative;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 15px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.food-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.card-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 5px;
  opacity: 0;
  transition: opacity 0.3s;
}

.food-card:hover .card-actions {
  opacity: 1;
}

.edit-btn, .delete-btn {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-btn:hover {
  background-color: #e3f2fd;
}

.delete-btn:hover {
  background-color: #ffebee;
}

.food-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  padding-right: 60px; /* 为按钮留出空间 */
}

.food-category {
  color: #666;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.food-price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #e53935;
  margin-bottom: 10px;
}

.unit {
  font-size: 0.8rem;
  color: #666;
  font-weight: normal;
}

.food-info {
  color: #666;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.food-stock {
  color: #333;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.food-cooking-time {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 8px;
}

.food-ingredients {
  margin-top: 10px;
}

.ingredients-title {
  font-weight: bold;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.ingredients-list {
  padding-left: 20px;
  margin: 0;
  font-size: 0.85rem;
  color: #666;
}

.ingredients-list li {
  margin-bottom: 3px;
}
</style>