<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref(localStorage.username)
const router = useRouter()

const exit = async () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('username')
  router.push('/')
}
</script>

<template>
  <div class="header">
    <div class="user">{{ username }}</div>
    <div @click="exit" class="exit">Выход</div>
  </div>
</template>

<style scoped>
.header {
  background-color: rgb(157, 0, 255);
  height: 50px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  font-size: 20px;
}

.exit {
  transition: 0.2s;
  cursor: pointer;
}

.exit:hover {
  color: rgb(199, 233, 62);
  transition: 0.2s;
}
</style>
