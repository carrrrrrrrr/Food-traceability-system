<template>
  <div>
    <!-- 加载中状态 -->
    <div v-if="loading" class="loading">
      <p>加载中...</p>
    </div>
    
    <!-- 无数据状态 -->
    <div v-else-if="ingredients.length === 0" class="no-data">
      <p>暂无原料数据，请添加新原料</p>
    </div>
    
    <!-- 原料卡片网格 -->
    <div v-else class="ingredient-grid">
      <IngredientCard 
        v-for="item in ingredients" 
        :key="item.id" 
        :ingredient="item"
        @show-image="$emit('show-image', $event)"
        @delete="$emit('delete', $event)"
        @edit="$emit('edit', $event)"
      />
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import IngredientCard from './IngredientCard.vue';

defineProps({
  ingredients: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
});

defineEmits(['show-image', 'delete', 'edit']);
</script>

<style scoped>
/* 原料卡片网格样式 */
.ingredient-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
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