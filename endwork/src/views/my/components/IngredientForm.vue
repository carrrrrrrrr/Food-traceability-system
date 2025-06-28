<template>
  <div class="modal">
    <div class="modal-content">
      <div class="modal-header">
        <h3>{{ isEdit ? '编辑原料' : '添加新原料' }}</h3>
        <span class="close-btn" @click="$emit('close')">&times;</span>
      </div>
      <div class="modal-body">
        <form @submit.prevent="submitForm" enctype="multipart/form-data">
          <div class="form-group">
            <label for="ingredient-name">原料名称</label>
            <input type="text" id="ingredient-name" v-model="formData.name" required>
          </div>
          
          <div class="form-group">
            <label for="ingredient-type">原料种类</label>
            <div class="type-checkboxes">
              <div v-for="(type, index) in typeOptions" :key="index" class="type-checkbox">
                <input type="checkbox" :id="'type-' + index" v-model="selectedTypes[index]">
                <label :for="'type-' + index">{{ type }}</label>
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label for="ingredient-description">原料描述</label>
            <textarea id="ingredient-description" v-model="formData.description" rows="3"></textarea>
          </div>
          
          <div class="form-group">
            <label for="farming-time">养殖/种植时间</label>
            <input type="datetime-local" id="farming-time" v-model="formData.farming_time">
          </div>
          
          <div class="form-group">
            <label for="production-time">出产时间</label>
            <input type="datetime-local" id="production-time" v-model="formData.production_time">
          </div>
          
          <div class="form-group">
            <label for="planting-image">种植图片</label>
            <input type="file" id="planting-image" @change="handleFileUpload($event, 'planting_image')" accept="image/*">
            <div class="preview" v-if="previews.planting_image">
              <img :src="previews.planting_image" alt="种植图片预览" class="preview-image">
            </div>
            <div class="preview" v-else-if="isEdit && ingredient.planting_image">
              <img :src="getImageUrl(ingredient.planting_image)" alt="当前种植图片" class="preview-image">
              <div class="current-image-label">当前图片</div>
            </div>
          </div>
          
          <div class="form-group">
            <label for="growing-image">生长图片</label>
            <input type="file" id="growing-image" @change="handleFileUpload($event, 'growing_image')" accept="image/*">
            <div class="preview" v-if="previews.growing_image">
              <img :src="previews.growing_image" alt="生长图片预览" class="preview-image">
            </div>
            <div class="preview" v-else-if="isEdit && ingredient.growing_image">
              <img :src="getImageUrl(ingredient.growing_image)" alt="当前生长图片" class="preview-image">
              <div class="current-image-label">当前图片</div>
            </div>
          </div>
          
          <div class="form-group">
            <label for="production-image">出产图片</label>
            <input type="file" id="production-image" @change="handleFileUpload($event, 'production_image')" accept="image/*">
            <div class="preview" v-if="previews.production_image">
              <img :src="previews.production_image" alt="出产图片预览" class="preview-image">
            </div>
            <div class="preview" v-else-if="isEdit && ingredient.production_image">
              <img :src="getImageUrl(ingredient.production_image)" alt="当前出产图片" class="preview-image">
              <div class="current-image-label">当前图片</div>
            </div>
          </div>
          
          <div class="form-group">
            <label for="quality-report-image">质检报告图片</label>
            <input type="file" id="quality-report-image" @change="handleFileUpload($event, 'quality_report_image')" accept="image/*">
            <div class="preview" v-if="previews.quality_report_image">
              <img :src="previews.quality_report_image" alt="质检报告预览" class="preview-image">
            </div>
            <div class="preview" v-else-if="isEdit && ingredient.quality_report_image">
              <img :src="getImageUrl(ingredient.quality_report_image)" alt="当前质检报告" class="preview-image">
              <div class="current-image-label">当前图片</div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="$emit('close')">取消</button>
            <button type="submit" class="submit-btn" :disabled="isSubmitting">
              {{ isSubmitting ? '提交中...' : (isEdit ? '保存修改' : '添加原料') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineProps, defineEmits, watch } from 'vue';

const props = defineProps({
  ingredient: {
    type: Object,
    default: () => ({})
  },
  isEdit: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'submit']);

// 原料种类选项
const typeOptions = ['肉类', '蔬菜类', '水产类', '粮食类', '乳产品', '蛋产品', '调料类'];
const selectedTypes = ref(typeOptions.map(() => false));

// 表单数据
const formData = ref({
  name: '',
  description: '',
  farming_time: '',
  production_time: ''
});

// 文件对象
const files = ref({
  planting_image: null,
  growing_image: null,
  production_image: null,
  quality_report_image: null
});

// 图片预览
const previews = ref({
  planting_image: '',
  growing_image: '',
  production_image: '',
  quality_report_image: ''
});

// 提交状态
const isSubmitting = ref(false);

// 计算选中的类型
const selectedTypeString = computed(() => {
  return typeOptions
    .filter((_, index) => selectedTypes.value[index])
    .join('，');
});

// 获取图片URL
const getImageUrl = (path) => {
  if (!path) return '';
  return `http://localhost:5000/${path}`;
};

// 处理文件上传
const handleFileUpload = (event, fieldName) => {
  const file = event.target.files[0];
  if (file) {
    files.value[fieldName] = file;
    
    // 创建预览
    const reader = new FileReader();
    reader.onload = (e) => {
      previews.value[fieldName] = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

// 提交表单
const submitForm = async () => {
  if (!formData.value.name) {
    alert('请输入原料名称');
    return;
  }
  
  isSubmitting.value = true;
  
  try {
    // 获取用户ID
    const userInfo = localStorage.getItem('currentUser');
    const userId = userInfo ? JSON.parse(userInfo).id : null;
    
    if (!userId) {
      alert('未找到用户信息，请重新登录');
      isSubmitting.value = false;
      return;
    }
    
    // 创建FormData对象
    const formDataObj = new FormData();
    formDataObj.append('name', formData.value.name);
    formDataObj.append('description', formData.value.description || '');
    formDataObj.append('type', selectedTypeString.value);
    formDataObj.append('user_id', userId);
    
    if (formData.value.farming_time) {
      formDataObj.append('farming_time', formData.value.farming_time);
    }
    
    if (formData.value.production_time) {
      formDataObj.append('production_time', formData.value.production_time);
    }
    
    // 添加文件
    for (const [key, file] of Object.entries(files.value)) {
      if (file) {
        formDataObj.append(key, file);
      }
    }
    
    // 如果是编辑模式，添加原料ID
    if (props.isEdit) {
      formDataObj.append('id', props.ingredient.id);
    }
    
    // 提交表单
    emit('submit', formDataObj, props.isEdit ? props.ingredient.id : null);
    
    // 重置表单
    if (!props.isEdit) {
      resetForm();
    }
  } catch (error) {
    console.error('提交表单错误:', error);
    alert('提交失败，请检查表单数据');
  } finally {
    isSubmitting.value = false;
  }
};

// 重置表单
const resetForm = () => {
  formData.value = {
    name: '',
    description: '',
    farming_time: '',
    production_time: ''
  };
  
  selectedTypes.value = typeOptions.map(() => false);
  
  files.value = {
    planting_image: null,
    growing_image: null,
    production_image: null,
    quality_report_image: null
  };
  
  previews.value = {
    planting_image: '',
    growing_image: '',
    production_image: '',
    quality_report_image: ''
  };
};

// 当编辑模式下，初始化表单数据
watch(() => props.ingredient, (newVal) => {
  if (props.isEdit && newVal && newVal.id) {
    formData.value.name = newVal.name || '';
    formData.value.description = newVal.description || '';
    formData.value.farming_time = newVal.farming_time ? new Date(newVal.farming_time).toISOString().slice(0, 16) : '';
    formData.value.production_time = newVal.production_time ? new Date(newVal.production_time).toISOString().slice(0, 16) : '';
    
    // 设置选中的类型
    const types = newVal.type ? newVal.type.split('，') : [];
    selectedTypes.value = typeOptions.map(type => types.includes(type));
  }
}, { immediate: true });
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
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

input[type="text"],
input[type="datetime-local"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

input[type="file"] {
  width: 100%;
  padding: 8px 0;
}

.type-checkboxes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 10px;
}

.type-checkbox {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.type-checkbox input {
  margin-right: 8px;
}

.preview {
  margin-top: 10px;
}

.preview-image {
  max-width: 100%;
  max-height: 150px;
  border-radius: 4px;
}

.current-image-label {
  font-size: 0.8rem;
  color: #666;
  margin-top: 5px;
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
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-btn:hover {
  background-color: #45a049;
}

.submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>