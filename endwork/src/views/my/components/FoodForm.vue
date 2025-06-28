<template>
  <div class="modal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>{{ mode === 'add' ? '添加新产品' : '修改产品' }}</h3>
        <span class="close-btn" @click="$emit('close')">&times;</span>
      </div>
      <div class="modal-body">
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="name">食品名称</label>
            <input type="text" id="name" v-model="formData.name" required>
          </div>
          
          <div class="form-group">
            <label for="category">食品种类</label>
            <input type="text" id="category" v-model="formData.category" placeholder="多个种类用中文逗号分隔，如：甜点，糕点">
          </div>
          
          <div class="form-group">
            <label for="prise">单价</label>
            <input type="number" id="prise" v-model="formData.prise" step="0.01" min="0.01" required>
          </div>
          
          <div class="form-group">
            <label for="poundage">计数单位</label>
            <input type="text" id="poundage" v-model="formData.poundage" required placeholder="例如：元/斤、元/个">
          </div>
          
          <div class="form-group">
            <label for="info">食品描述</label>
            <textarea id="info" v-model="formData.info" rows="3"></textarea>
          </div>
          
          <div class="form-group">
            <label for="cooking_time">制作时间</label>
            <input type="datetime-local" id="cooking_time" v-model="formData.cooking_time">
          </div>
          
          <div class="form-group">
            <label for="num">库存数量</label>
            <input type="number" id="num" v-model="formData.num" min="0" required>
          </div>
          
          <div class="form-group">
            <label>原料</label>
            <div class="ingredients-container">
              <div v-if="ingredients.length === 0" class="no-ingredients">暂无原料数据</div>
              <div v-else class="ingredients-selection">
                <div v-for="ingredient in ingredients" :key="ingredient.id" class="ingredient-item">
                  <input type="checkbox" :id="'ingredient-' + ingredient.id" v-model="selectedIngredients[ingredient.id]">
                  <label :for="'ingredient-' + ingredient.id">
                    {{ ingredient.name }}
                    <span v-if="ingredient.farmer_name" class="farmer-name">({{ ingredient.farmer_name }})</span>
                  </label>
                  <input 
                    type="text" 
                    v-if="selectedIngredients[ingredient.id]" 
                    v-model="ingredientAmounts[ingredient.id]" 
                    placeholder="用量"
                    class="amount-input"
                  >
                </div>
              </div>
              <div v-if="isUserMerchant && ingredients.length === 0" class="partner-tip">
                您需要先添加农户合作伙伴才能看到可用的原料
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="$emit('close')">取消</button>
            <button type="submit" class="submit-btn">{{ mode === 'add' ? '添加产品' : '保存修改' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';

const props = defineProps({
  food: {
    type: Object,
    required: true
  },
  ingredients: {
    type: Array,
    required: true
  },
  mode: {
    type: String,
    default: 'add',
    validator: (value) => ['add', 'edit'].includes(value)
  }
});

const emit = defineEmits(['close', 'submit', 'add-ingredient']);

// 表单数据
const formData = ref({
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

// 选中的原料和用量
const selectedIngredients = ref({});
const ingredientAmounts = ref({});

// 初始化表单数据
const initFormData = () => {
  // 复制食品数据到表单
  formData.value = { ...props.food };
  
  // 初始化选中的原料和用量
  selectedIngredients.value = {};
  ingredientAmounts.value = {};
  
  if (props.food.ingredients && props.food.ingredients.length > 0) {
    props.food.ingredients.forEach(ing => {
      selectedIngredients.value[ing.id] = true;
      ingredientAmounts.value[ing.id] = ing.amount || '';
    });
  }
};

// 处理表单提交
const handleSubmit = () => {
  // 处理选中的原料
  const ingredients = [];
  for (const [id, selected] of Object.entries(selectedIngredients.value)) {
    if (selected) {
      ingredients.push({
        id: parseInt(id),
        amount: ingredientAmounts.value[id] || ''
      });
    }
  }
  
  // 准备提交的数据
  const submitData = {
    ...formData.value,
    ingredients
  };
  
  emit('submit', submitData);
};

// 监听食品数据变化
watch(() => props.food, () => {
  initFormData();
}, { deep: true });

// 组件挂载时初始化表单数据
onMounted(() => {
  initFormData();
});

// 判断当前用户是否为商户
const isUserMerchant = computed(() => {
  const userInfo = localStorage.getItem('currentUser');
  if (userInfo) {
    try {
      const user = JSON.parse(userInfo);
      return user.identity === '商户';
    } catch (error) {
      return false;
    }
  }
  return false;
});
</script>

<style scoped>
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

/* 表单样式 */
.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

input[type="text"],
input[type="number"],
input[type="datetime-local"],
textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

textarea {
  resize: vertical;
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

.submit-btn {
  background-color: #4CAF50;
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

.submit-btn:hover {
  background-color: #45a049;
}

/* 原料选择样式 */
.ingredients-container {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  max-height: 200px;
  overflow-y: auto;
}

.no-ingredients {
  color: #999;
  text-align: center;
  padding: 10px;
}

.ingredients-selection {
  margin-bottom: 10px;
}

.ingredient-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.ingredient-item label {
  margin: 0 10px 0 5px;
  font-weight: normal;
}

.amount-input {
  width: 100px;
  padding: 4px 8px;
  font-size: 14px;
}

.add-ingredient-btn {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-top: 10px;
}

.add-ingredient-btn:hover {
  background-color: #0b7dda;
}
.farmer-name {
  font-size: 0.85em;
  color: #666;
  margin-left: 5px;
}

.partner-tip {
  margin-top: 10px;
  color: #ff6b6b;
  font-size: 0.9em;
  font-style: italic;
}
</style>