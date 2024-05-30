<script setup>
import { reactive, ref, onMounted } from 'vue'
import axios from 'axios'

var API_port = '0.0.0.0:8000'

const drives = reactive([])
const speed = reactive({})
const getAllDrives = async () => {
  const dr = ref(null)
  try {
    const { data } = await axios({
      method: 'get',
      url: `http://` + API_port + `/api/drives`,
      headers: { Authorization: ' Bearer ' + localStorage.access_token }
    })
    dr.value = data
  } catch (err) {
    console.log(err)
  }
  for (let i = 0; i < dr.value.length; i++) {
    try {
      const { data } = await axios({
        method: 'get',
        url: `http://` + API_port + `/api/drives/${dr.value[i]}`,
        headers: { Authorization: ' Bearer ' + localStorage.access_token }
      })
      data['message'] = '-'
      drives.push(data)
      speed[data.name] = 0
    } catch (err) {
      console.log(err)
    }
  }
}

const start = async (drive_name) => {
  try {
    const { data } = await axios({
      method: 'post',
      url: `http://` + API_port + `/api/drives/${drive_name}/start?speed=${speed[drive_name]}`,
      headers: { Authorization: ' Bearer ' + localStorage.access_token }
    })
    for (let i = drives.length - 1; i >= 0; i--) {
      if (drives[i].name === drive_name) {
        drives[i].is_running = true
      }
    }
  } catch (err) {
    console.log(err)
  }
}

const stop = async (drive_name) => {
  try {
    const { data } = await axios({
      method: 'post',
      url: `http://` + API_port + `/api/drives/${drive_name}/stop`,
      headers: { Authorization: ' Bearer ' + localStorage.access_token }
    })
    for (let i = drives.length - 1; i >= 0; i--) {
      if (drives[i].name === drive_name) {
        drives[i].is_running = false
      }
    }
  } catch (err) {
    console.log(err)
  }
}

const del = async (drive_name) => {
  try {
    const { data } = await axios({
      method: 'delete',
      url: `http://` + API_port + `/api/drives/${drive_name}`,
      headers: { Authorization: ' Bearer ' + localStorage.access_token }
    })
    for (let i = drives.length - 1; i >= 0; i--) {
      if (drives[i].name === drive_name) {
        drives.splice(i, 1)
      }
    }
  } catch (err) {
    console.log(err)
  }
}

const socket = new WebSocket('ws://127.0.0.1:8000/api/info')
socket.onmessage = function (event) {
  const data = JSON.parse(event.data)
  const names = drives.map((item) => item.name)
  console.log(names)
  if (names.includes(data['name'])) {
    for (let i = drives.length - 1; i >= 0; i--) {
      if (drives[i].name === data['name']) {
        drives[i] = data
      }
    }
    console.log()
  } else {
    drives.push(data)
  }
}

onMounted(() => getAllDrives())
</script>

<template>
  <div class="main">
    <div class="main_box t">
      <div class="drives">
        <div class="col">
          <span>Название</span>
        </div>
        <div class="col">
          <span>Статус</span>
        </div>
        <div class="col">
          <span>Скорость</span>
        </div>
        <div class="col">
          <span>Сообщение</span>
        </div>
        <div class="action"><span>Действие/скорость</span></div>
        <div class="col"><span>Удалить</span></div>
      </div>
    </div>

    <div class="main_box header_main_box">
      <div class="drives" v-for="drive in drives" :key="drive.name">
        <div class="col">
          <span>{{ drive.name }}</span>
        </div>
        <div class="col">
          <span>{{ drive.is_running }}</span>
        </div>
        <div class="col">
          <span>{{ drive.speed }}</span>
        </div>
        <div class="col">
          <span>{{ drive.message }}</span>
        </div>
        <div v-if="!drive.is_running" class="action">
          <span @click="start(drive.name)">запустить</span>
          <input type="text" v-model="speed[drive.name]" />
        </div>
        <div v-else class="action" @click="stop(drive.name)"><span>остановить</span></div>
        <div class="action" @click="del(drive.name)"><span>удалить</span></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.drives {
  display: flex;
}

.main_box {
  margin: 0 auto;
  width: 60%;
  margin-bottom: 10px;
}

.drives {
  border-top: solid black 2px;
  border-left: solid black 2px;
  border-right: solid black 2px;
  display: flex;
}

.drives:last-child {
  border: solid black 2px;
}

.col {
  width: 15%;
  border-right: 2px solid black;
}

.col:last-child {
  border-right: none;
}

span {
  margin-left: 10px;
}
input {
  width: 100px;
}
.action {
  border-right: 2px solid black;
  width: 18%;
}
.action:last-child {
  border-right: none;
}

.action span {
  transition: 0.2s;
  cursor: pointer;
}

.action span:hover {
  color: rgb(199, 233, 62);
  transition: 0.2s;
}

.main_box {
  overflow: scroll;
  overflow-x: hidden;
}

.main_box:last-child {
  height: 750px;
}
</style>
