<template>
  <div class="content" >
    <div>
      <el-page-header class="page-header" @back="goBack"  title="Volver" content="Administración">
    </el-page-header>
    </div>
    <h1>Administración</h1>
    <el-divider></el-divider>
    <el-row class="card-container">
  <el-col :span="5"  class="card-column">
    <el-card  :body-style="{ padding: '0px' }"  class="card-ad"  style="border-radius: 15%;" >
        <router-link :to="{ name: 'othersSettings' }">
      <img src="../../assets/icons/settings-gear-icon.png" class="image">
      <div style="padding: 14px;">
        <h3> Otros Ajustes</h3>
      </div>
    </router-link>
    </el-card>
  </el-col>
  <div></div>&nbsp;&nbsp;&nbsp;
  <el-col :span="5"  class="card-column">
    <el-card  :body-style="{ padding: '0px' }"  class="card-ad"  style="border-radius: 15%;">
      <router-link :to="{ name: 'settingsUsers' }">
      <img src="../../assets/icons/users.png" class="image">
      <div style="padding: 14px;">
        <h3>Usuarios</h3>
      </div>
      </router-link>
    </el-card>
  </el-col>
  <div></div>&nbsp;&nbsp;&nbsp;
  <el-col :span="5" class="card-column" >
    <el-card :body-style="{ padding: '0px' }" class="card-ad"  style="border-radius: 15%;" >
      <router-link :to="{ name: 'settingsProducts' }">
      <img src="../../assets/icons/small-business.png" class="image">
      <div style="padding: 14px;">
        <h3>Productos</h3>
      </div>
     </router-link>
    </el-card>
  </el-col>
  <el-col :span="5" class="card-column" >
    <el-card :body-style="{ padding: '0px' }" class="card-ad"  style="border-radius: 15%;" >
      <router-link :to="{ name: 'settingsOrders' }">
      <img src="../../assets/icons/checklist_5132297.png" class="image">
      <div style="padding: 14px;">
        <h3>Pedidos</h3>
      </div>
     </router-link>
    </el-card>
  </el-col>
  <el-col :span="4" class="card-column" >
    <el-card :body-style="{ padding: '0px' }" class="card-ad"  style="border-radius: 15%;" >
      <router-link :to="{ name: 'settingsCategories' }">
      <img src="../../assets/icons/categories_maker.png"  class="image">
      <div style="padding: 14px;">
        <h3>Categorías y Marcas</h3>
      </div>
     </router-link>
    </el-card>
  </el-col>
</el-row>
</div>
</template>
<script>
import router from '@/router'

export default {
  name: 'adminWhile',
  data () {
    return {
      currentDate: new Date()
    }
  },
  methods: {
    goBack () {
      router.push('/')
    }
  }
}
</script>
<style scoped>
.content {
  margin-top: 2px;
  padding-left: 200px;
  padding-right: 200px;
  margin-bottom: 200px;

}
h3,h4{
  list-style: none;
  display: inline-flex;
  text-decoration: none;
  color: black;
}
.card-column{
  margin-right: 100px;
}
.card-container{
text-align: center;
display: flex;
justify-content: center;
margin: 0,10px;
margin-top:40px ;
}
.card-ad{
  border-radius:15% ;
  width: 100%;
}
  .time {
    font-size: 13px;
    color: #999;
  }
  .card-colum{
    margin: 0, 10px;
    padding: 0,10px;
  }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
  width: 70%;
  padding-top: 40px;
  height: auto;
  display: block;
  margin: 0 auto;
}
  .card-ad:hover{
    background-color: rgba(230, 230, 230, 0.6);
  }
.page-header{
  margin-left: 30px;
}
</style>
