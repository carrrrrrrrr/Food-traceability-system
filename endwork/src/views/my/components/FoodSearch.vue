<template>
  <div class="search-container">
    <input 
      type="text" 
      v-model="keyword" 
      :placeholder="placeholder" 
      class="search-input"
      @input="handleInput"
    >
    <button class="search-btn" @click="handleSearch">
      <span class="search-icon">🔍</span>
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  placeholder: {
    type: String,
    default: '搜索...'
  }
});

const emit = defineEmits(['search']);

const keyword = ref('');

// 处理输入
const handleInput = () => {
  emit('search', keyword.value);
};

// 处理搜索按钮点击
const handleSearch = () => {
  emit('search', keyword.value);
};
</script>

<style scoped>
.search-container {
  display: flex;
  align-items: center;
  width: 250px;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 16px;
  outline: none;
}

.search-input:focus {
  border-color: #4CAF50;
}

.search-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-btn:hover {
  background-color: #45a049;
}

.search-icon {
  font-size: 16px;
}
</style>