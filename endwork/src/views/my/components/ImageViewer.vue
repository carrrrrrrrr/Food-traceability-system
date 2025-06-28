<template>
  <div class="image-viewer" @click="$emit('close')">
    <div class="image-container">
      <img :src="imageUrl" alt="查看图片">
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

defineProps({
  imageUrl: {
    type: String,
    required: true
  }
});

defineEmits(['close']);
</script>

<style scoped>
.image-viewer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  cursor: pointer;
}

.image-container {
  max-width: 90%;
  max-height: 90%;
}

.image-container img {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
}
</style>