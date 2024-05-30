<script setup>
import { ref } from 'vue'
import axios from 'axios'

import AddDrives from '../components/AddDrives.vue'
import Header from '../components/Header.vue'
import DrivesList from '../components/DrivesList.vue'

var API_port = '0.0.0.0:8000'
</script>

<template>
  <Header />
  <AddDrives />
  <DrivesList />
</template>

<style scoped></style>
