<template>
  <div class="content" >
    <div>
      <el-page-header class="page-header" @back="goBack"  title="Volver" content="Mi Cuenta">
    </el-page-header>
    </div>
    <h2>Mi Cuenta</h2>
    <el-button class="LoGout ml-auto" @click="logout">Cerrar sesión</el-button>
    <el-divider></el-divider>
    <el-row class="card-container">
  <el-col :span="4"  class="card-column">
    <el-card  :body-style="{ padding: '0px' }"  class="card-ad"  style="border-radius: 15%;" >
        <router-link :to="{ name: 'dateUserWhile' }">
      <img src="../../assets/icons/avatar.png" class="image">
      <div style="padding: 14px;">
        <h3> Mis datos</h3>
      </div>
    </router-link>
    </el-card>
  </el-col>
  <div></div>&nbsp;&nbsp;&nbsp;
  <el-col :span="4"  class="card-column">
    <el-card  :body-style="{ padding: '0px' }"  class="card-ad"  style="border-radius: 15%;">
      <router-link :to="{ name: 'directionWhile' }">
      <img src="../../assets/icons/location.png" class="image">
      <div style="padding: 14px;">
        <h3>Mi Dirección</h3>
      </div>
      </router-link>
    </el-card>
  </el-col>
  <div></div>&nbsp;&nbsp;&nbsp;
  <el-col :span="4" class="card-column" >
    <el-card :body-style="{ padding: '0px' }" class="card-ad"  style="border-radius: 15%;" >
      <router-link :to="{ name: 'ordersWhile' }">
      <img src="../../assets/icons/calendar.png" class="image">
      <div style="padding: 14px;">
        <h3>Pedidos</h3>
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
  name: 'userWhile',
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
h3{
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
.LoGout{
  background-color: #00BAB4;
  display: flex;
margin-left: 90%;
  opacity: 0.8;
  border-radius:15px ;
  color: black;
}
.LoGout:hover{
  background-color: #07e1da;
  color: black;
}
</style>
