<script setup>
import { ref, reactive, watch, inject } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

var API_port = '0.0.0.0:8000'

const username = ref('')
const password = ref('')
const page_flag = ref(true)
const error_messege = ref('')

const change_page = () => {
  page_flag.value = !page_flag.value
  error_messege.value = ''
}

const login = async () => {
  event.preventDefault()
  try {
    const { data } = await axios.post(
      `http://` + API_port + `/api/auth/login?username=${username.value}&password=${password.value}`
    )
    localStorage.access_token = data
    localStorage.username = username.value
    error_messege.value = ''
    router.push('/main')
  } catch (err) {
    console.log(err)
    error_messege.value = 'Неверное имя пользователя или пароль'
  }
}

const registration = async () => {
  event.preventDefault()
  try {
    const { data } = await axios.post(
      `http://` +
        API_port +
        `/api/auth/register?username=${username.value}&password=${password.value}`
    )
    console.log(data)
    localStorage.access_token = data
    localStorage.username = username.value
    error_messege.value = ''
    router.push('/main')
  } catch (err) {
    console.log(err)
  }
}
</script>

<template>
  <form action="">
    <h1 v-if="page_flag">Вход</h1>
    <h1 v-else>Регистрация</h1>

    <div class="input_box">
      <label class="label_name">Имя пользователя</label>
      <input class="text_input" type="text" v-model="username" />
    </div>

    <div class="input_box">
      <label class="label_name">Пароль</label>
      <input class="text_input" type="password" v-model="password" />
    </div>
    <div class="flag" v-if="page_flag" @click="change_page">Создать новый аккаунт</div>
    <div class="flag" v-else @click="change_page">Войти в существующий аккаунт</div>
    <div class="error">{{ error_messege }}</div>
    <button @click="login" type="button" v-if="page_flag">Войти</button>
    <button @click="registration" type="button" v-else>Зарегистрироваться</button>
  </form>
</template>

<style scoped>
.label_name {
  font-size: 20px;
}
.input_box {
  margin-bottom: 10px;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.text_input {
  border: 2px solid black;
  border-radius: 5px;
  padding: 4px 10px;
  width: 100%;
  height: 20px;
}
.error {
  color: red;
  font-size: 20px;
  height: 20px;
}
.text_input:hover {
  border: 2px solid rgb(62, 88, 233);
}

input:focus {
  outline: rgb(62, 88, 233);
  border-color: rgb(62, 88, 233);
}

form {
  margin: 0 auto;
  margin-top: 250px;
  display: flex;
  flex-direction: column;
  width: 25%;
  align-items: center;
  color: white;
}

button {
  margin-top: 50px;
  background-color: rgb(62, 88, 233);
  width: 200px;
}

button:hover {
  background-color: rgb(199, 233, 62);
  color: black;
}

.flag {
  transition: 0.2s;
  cursor: pointer;
}
.flag:hover {
  color: rgb(199, 233, 62);
  transition: 0.2s;
}
</style>
