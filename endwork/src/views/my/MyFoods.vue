<template>
  <div class="my-foods">
    <div class="header-section">
      <h2>我的食品列表</h2>
      <div class="header-actions">
        <FoodSearch 
          @search="handleSearch" 
          :placeholder="'搜索产品名称'"
        />
        <button class="add-btn" @click="showAddModal">添加新产品</button>
      </div>
    </div>
    
    <FoodList 
      :foods="filteredFoods" 
      :loading="loading"
      @edit="showEditModal"
      @delete="showDeleteConfirm"
    />
    
    <FoodForm 
      v-if="showModal" 
      :food="currentFood" 
      :ingredients="ingredients"
      :mode="formMode"
      @close="closeModal"
      @submit="handleFormSubmit"
      @add-ingredient="showIngredientModal = true"
    />
    
    <IngredientForm 
      v-if="showIngredientModal" 
      @close="showIngredientModal = false"
      @submit="addIngredient"
    />
    
    <!-- 删除确认对话框 -->
    <div class="modal" v-if="showDeleteModal">
      <div class="modal-content modal-sm">
        <div class="modal-header">
          <h3>确认删除</h3>
          <span class="close-btn" @click="showDeleteModal = false">&times;</span>
        </div>
        <div class="modal-body">
          <p>确定要删除产品 "{{ currentFood.name }}" 吗？此操作不可撤销。</p>
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="showDeleteModal = false">取消</button>
            <button type="button" class="delete-btn" @click="deleteFood">确认删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { food, ingredient } from '../../api/api';
import FoodSearch from './components/FoodSearch.vue';
import FoodList from './components/FoodList.vue';
import FoodForm from './components/FoodForm.vue';
import IngredientForm from './components/IngredientForm.vue';

// 用户信息
const userId = ref(null);

// 食品列表
const foods = ref([]);
const loading = ref(false);

// 搜索关键词
const searchKeyword = ref('');

// 过滤后的食品列表
const filteredFoods = computed(() => {
  if (!searchKeyword.value) return foods.value;
  
  return foods.value.filter(food => 
    food.name.toLowerCase().includes(searchKeyword.value.toLowerCase())
  );
});

// 原料列表
const ingredients = ref([]);

// 控制模态框显示
const showModal = ref(false);
const showIngredientModal = ref(false);
const showDeleteModal = ref(false);

// 表单模式：'add' 或 'edit'
const formMode = ref('add');

// 当前操作的食品
const currentFood = ref({
  id: null,
  name: '',
  prise: '',
  info: '',
  poundage: '',
  num: 0,
  category: '',
  cooking_time: '',
  user_id: null,
  ingredients: []
});

// 获取用户食品列表
const getUserFoods = async () => {
  loading.value = true;
  try {
    const response = await food.getUserFoods(userId.value);
    if (response.status === 'success') {
      foods.value = response.data;
    } else {
      console.error('获取食品列表失败:', response.message);
    }
  } catch (error) {
    console.error('获取食品列表错误:', error);
  } finally {
    loading.value = false;
  }
};

// 获取原料列表
// 获取原料列表
const getIngredients = async () => {
  try {
    const userInfo = JSON.parse(localStorage.getItem('currentUser'));
    let response;
    
    // 根据用户身份获取不同的原料列表
    if (userInfo.identity === '商户') {
      // 商户只能使用合作伙伴的原料
      response = await ingredient.getPartnerIngredients(userInfo.id);
    } else {
      // 农户可以使用所有原料
      response = await ingredient.getIngredients();
    }
    
    if (response.status === 'success') {
      ingredients.value = response.data;
    } else {
      console.error('获取原料列表失败:', response.message);
    }
  } catch (error) {
    console.error('获取原料列表错误:', error);
  }
};

// 添加原料
const addIngredient = async (newIngredient) => {
  try {
    const response = await ingredient.addIngredient(newIngredient);
    if (response.status === 'success') {
      // 添加成功，刷新列表
      ingredients.value.push(response.data);
      showIngredientModal.value = false;
      alert('添加原料成功！');
    } else {
      alert(`添加失败: ${response.message}`);
    }
  } catch (error) {
    console.error('添加原料错误:', error);
    alert('添加失败，请检查网络连接或联系管理员');
  }
};

// 显示添加模态框
const showAddModal = () => {
  formMode.value = 'add';
  currentFood.value = {
    id: null,
    name: '',
    prise: '',
    info: '',
    poundage: '',
    num: 0,
    category: '',
    cooking_time: '',
    user_id: userId.value,
    ingredients: []
  };
  showModal.value = true;
};

// 显示编辑模态框
const showEditModal = (foodItem) => {
  formMode.value = 'edit';
  currentFood.value = JSON.parse(JSON.stringify(foodItem)); // 深拷贝
  showModal.value = true;
};

// 显示删除确认框
const showDeleteConfirm = (foodItem) => {
  currentFood.value = foodItem;
  showDeleteModal.value = true;
};

// 关闭模态框
const closeModal = () => {
  showModal.value = false;
};

// 处理表单提交
const handleFormSubmit = async (formData) => {
  try {
    let response;
    
    if (formMode.value === 'add') {
      // 添加产品
      response = await food.addFood(formData);
      if (response.status === 'success') {
        foods.value.push(response.data);
        alert('添加产品成功！');
      }
    } else {
      // 修改产品
      response = await food.updateFood(formData.id, formData);
      if (response.status === 'success') {
        // 更新本地数据
        const index = foods.value.findIndex(item => item.id === formData.id);
        if (index !== -1) {
          foods.value[index] = response.data;
        }
        alert('修改产品成功！');
      }
    }
    
    if (response.status === 'success') {
      showModal.value = false;
    } else {
      alert(`操作失败: ${response.message}`);
    }
  } catch (error) {
    console.error('操作错误:', error);
    alert('操作失败，请检查网络连接或联系管理员');
  }
};

// 删除产品
const deleteFood = async () => {
  try {
    const response = await food.deleteFood(currentFood.value.id, userId.value);
    if (response.status === 'success') {
      // 从列表中移除
      foods.value = foods.value.filter(item => item.id !== currentFood.value.id);
      showDeleteModal.value = false;
      alert('删除产品成功！');
    } else {
      alert(`删除失败: ${response.message}`);
    }
  } catch (error) {
    console.error('删除产品错误:', error);
    alert('删除失败，请检查网络连接或联系管理员');
  }
};

// 处理搜索
const handleSearch = (keyword) => {
  searchKeyword.value = keyword;
};

// 组件挂载时获取用户信息和食品列表
onMounted(() => {
  const userInfo = localStorage.getItem('currentUser');
  if (userInfo) {
    try {
      const user = JSON.parse(userInfo);
      userId.value = user.id;
      
      // 获取食品列表
      getUserFoods();
      
      // 获取原料列表
      getIngredients();
    } catch (error) {
      console.error('解析用户信息失败', error);
    }
  }
});
</script>

<style scoped>
.my-foods {
  padding: 20px;
}

/* 头部区域样式 */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
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

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.modal-sm {
  max-width: 400px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.delete-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.cancel-btn:hover {
  background-color: #e0e0e0;
}

.delete-btn:hover {
  background-color: #d32f2f;
}
</style>