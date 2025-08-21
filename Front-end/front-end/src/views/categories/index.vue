<template>
  <div class="content" v-loading="loading">
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Categorías">
      </el-page-header>
    </div>
    <el-row class="card-container">
      <el-col :span="4" v-for="category in categories" :key="category.id" class="card-col">
        <el-card class="body-style" shadow="hover" style="border-radius:30px; border:none;">
          <div class="card-content">
          <router-link :to="{ name: 'categoryProductWhile', params:{ CategoryId : category.id}}"  style="text-decoration: none;color: #76B9FF;">
            <img
              :src="'data:image/jpeg;base64,' + category.image"
              class="image"
            />
            <h3 style="color: #76B9FF;">{{ category.name }}</h3><br />
          </router-link>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import router from '@/router'
import { fetchCategoriesBase } from '@/api/categories'

export default {
  name: 'categoryWhile',
  data () {
    return {
      category: {
        name: '',
        id: '',
        image: ''
      },
      categories: [],
      loading: false
    }
  },
  mounted () {
    this.fetchData()
  },
  methods: {
    goBack () {
      router.push('/')
    },
    fetchData () {
      this.loading = true
      const params = {
        page_size: 100
      }
      fetchCategoriesBase(params)
        .then((response) => {
          this.categories = response.data.results
        })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
        }).finally(() => {
          this.loading = false
        })
    }
  }
}
</script>

<style scoped>
.body-style {
  text-align: center;

  height: 400px;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image {
  width: auto;
  max-width: 100%;
  height: auto;
  max-height: 100%;
  margin-bottom: 10px;
}

.content {
  margin-top: 2px;
  padding-left: 200px;
  padding-right: 200px;
  margin-bottom: 200px;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  text-align: center;
  margin-top: 20px;
}

.card-col {
  margin-bottom: 20px;
}

.page-header {

  margin-left: 30px;
}
</style>
