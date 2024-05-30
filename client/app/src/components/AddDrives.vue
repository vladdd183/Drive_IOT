<script setup>
import { ref } from 'vue'
import axios from 'axios'

var API_port = '0.0.0.0:8000'

const drive_name = ref('')

const add = async () => {
  try {
    const { data } = await axios({
      method: 'post',
      url: `http://` + API_port + `/api/drives?drive_name=${drive_name.value}`,
      headers: { Authorization: ' Bearer ' + localStorage.access_token }
    })
  } catch (err) {
    console.log(err)
  }
}
</script>

<template>
  <div class="input_box">
    <div class="inp">
      <span class="label_name">Создание нового устройства:</span>
      <input class="text_input" type="text" v-model="drive_name" />
    </div>
    <button :disabled="!drive_name" @click="add">Добавить</button>
  </div>
</template>

<style scoped>
.label_name {
  color: white;
  margin-right: 10px;
}
.input_box {
  width: 50%;
  margin: 0 auto;
  display: flex;
  align-items: center;
  margin-top: 20px;
  margin-bottom: 20px;
}

.text_input {
  border: 2px solid black;
  border-radius: 5px;
  padding: 4px 10px;
  width: 300px;
}

button {
  background-color: rgb(62, 88, 233);
  height: 40px;
  display: flex;
  align-items: center;
  margin-left: 20px;
}

button:hover {
  background-color: rgb(199, 233, 62);
  color: black;
}

button:disabled {
  background: #5f6164;
  transition: 0.2s;
}
</style>
