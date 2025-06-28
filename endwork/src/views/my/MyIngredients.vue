<template>
  <div class="my-ingredients">
    <div class="header-section">
      <h2>我的原料列表</h2>
      <button class="add-btn" @click="showAddModal = true">添加新原料</button>
    </div>
    
    <!-- 原料列表组件 -->
    <IngredientList 
      :ingredients="ingredients" 
      :loading="loading"
      @show-image="showImage"
      @delete="deleteIngredient"
      @edit="editIngredient"
    />
    
    <!-- 添加/编辑原料表单组件 -->
    <IngredientForm 
      v-if="showAddModal || showEditModal" 
      :ingredient="currentIngredient"
      :is-edit="showEditModal"
      @close="closeModal"
      @submit="submitIngredient"
    />
    
    <!-- 图片查看器组件 -->
    <ImageViewer 
      v-if="showImageViewer" 
      :image-url="currentImage"
      @close="showImageViewer = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ingredient } from '../../api/api';
import IngredientList from './components/IngredientList.vue';
import IngredientForm from './components/IngredientForm.vue';
import ImageViewer from './components/ImageViewer.vue';

// 用户信息
const userId = ref(null);

// 原料列表
const ingredients = ref([]);
const loading = ref(false);

// 控制模态框显示
const showAddModal = ref(false);
const showEditModal = ref(false);
const currentIngredient = ref(null);

// 图片查看器
const showImageViewer = ref(false);
const currentImage = ref('');

// 获取用户的原料列表
const getUserIngredients = async () => {
  loading.value = true;
  try {
    const response = await ingredient.getUserIngredients(userId.value);
    if (response.status === 'success') {
      ingredients.value = response.data;
    } else {
      console.error('获取原料列表失败:', response.message);
    }
  } catch (error) {
    console.error('获取原料列表错误:', error);
  } finally {
    loading.value = false;
  }
};

// 添加或更新原料
const submitIngredient = async (formData, ingredientId) => {
  try {
    let response;
    
    if (ingredientId) {
      // 更新原料
      response = await ingredient.updateIngredient(ingredientId, formData);
      if (response.status === 'success') {
        // 更新本地列表
        const index = ingredients.value.findIndex(item => item.id === ingredientId);
        if (index !== -1) {
          ingredients.value[index] = response.data;
        }
        showEditModal.value = false;
        alert('修改原料成功！');
      } else {
        alert(`修改失败: ${response.message}`);
      }
    } else {
      // 添加原料
      response = await ingredient.addIngredient(formData);
      if (response.status === 'success') {
        // 添加到本地列表
        ingredients.value.push(response.data);
        showAddModal.value = false;
        alert('添加原料成功！');
      } else {
        alert(`添加失败: ${response.message}`);
      }
    }
  } catch (error) {
    console.error('操作原料错误:', error);
    alert('操作失败，请检查网络连接或联系管理员');
  }
};

// 删除原料
const deleteIngredient = async (ingredientId) => {
  try {
    const response = await ingredient.deleteIngredient(ingredientId, userId.value);
    
    if (response.status === 'success') {
      // 从列表中移除
      ingredients.value = ingredients.value.filter(item => item.id !== ingredientId);
      alert('删除原料成功！');
    } else {
      alert(`删除失败: ${response.message}`);
    }
  } catch (error) {
    console.error('删除原料错误:', error);
    alert('删除失败，请检查网络连接或联系管理员');
  }
};

// 编辑原料
const editIngredient = (ingredient) => {
  currentIngredient.value = ingredient;
  showEditModal.value = true;
};

// 关闭模态框
const closeModal = () => {
  showAddModal.value = false;
  showEditModal.value = false;
  currentIngredient.value = null;
};

// 显示大图
const showImage = (url) => {
  currentImage.value = url;
  showImageViewer.value = true;
};

// 组件挂载时获取用户信息和原料列表
onMounted(() => {
  const userInfo = localStorage.getItem('currentUser');
  if (userInfo) {
    try {
      const user = JSON.parse(userInfo);
      userId.value = user.id;
      
      // 获取原料列表
      getUserIngredients();
    } catch (error) {
      console.error('解析用户信息失败', error);
    }
  }
});
</script>

<style scoped>
.my-ingredients {
  padding: 20px;
}

/* 头部区域样式 */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.add-btn:hover {
  background-color: #45a049;
}
</style>