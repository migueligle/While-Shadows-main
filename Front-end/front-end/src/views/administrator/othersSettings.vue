<template>
  <div class="content">
    <el-page-header class="page-header" @back="goBack" title="Volver" content="Otras Administraciones">
    </el-page-header>
    <div style="margin-top:20px">
      <el-tabs type="border-card" style="margin-top:10%;margin-bottom:10%;">
        <el-tab-pane label="Banners" style="width: 100%;">
          <banner-Show></banner-Show>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import router from '@/router'
import bannerShow from './components/banners.vue'
export default {
  name: 'userWhile',
  components: { bannerShow },
  data () {
    return {
      currentDate: new Date()
    }
  },
  methods: {
    logout () {
      localStorage.clear()
      router.push('/')
      window.location.reload()
    },
    goBack () {
      router.push('/admin')
    }
  }
}
</script>

<style scoped>
.content {
  margin-top: 150px;
  padding-left: 200px;
  padding-right: 200px;

}
</style>
