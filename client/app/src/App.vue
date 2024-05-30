<script setup>
import { ref, onMounted, provide, onUnmounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import axios from 'axios'
</script>

<template>
  <RouterView />
</template>

<style scoped></style>
