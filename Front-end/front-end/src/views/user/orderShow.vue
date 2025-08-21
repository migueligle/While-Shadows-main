<template>
  <div class="content">
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content=" Ver pedido">
      </el-page-header>
       <div>

        <img   style="width: 8%; margin-right:18px" src="@/assets/ISOTIPO.png"  alt="">
        <h1 class="titulo">{{ `Nº de pedido: ${order.id}` }}</h1>
        <el-divider></el-divider><br><br>
        <div v-if="![4, 5, 6].includes(order.status.id)">
          <el-steps :active="order.status.id" finish-status="success" align-center>
            <el-step title="Procesando el pago" icon="el-icon-loading"></el-step>
            <el-step title="En preparación" icon="el-icon-box"></el-step>
            <el-step title="Enviado"  icon="el-icon-truck"></el-step>
          </el-steps>
        </div>
        <div v-else-if="order.status.id===4">
          <h1  class="titulo" >Pedido cancelado</h1>

        </div>
        <div v-else-if="order.status.id===5">
          <h1  class="titulo" >Solicitado devolución pedido</h1>

        </div>
        <div  v-else-if="order.status.id===6">
          <h1 class="titulo"> Devolución de pedido,completado</h1>

        </div>

        <el-divider></el-divider><br><br>
        <el-table ref="table" :data="products" stripe style="width: 100%">
          <el-table-column
            v-for="column in columns"
            :key="column.label"
            :prop="column.prop"
            :label="column.label"
            :formatter="typeof column.formatter === 'function' ? column.formatter : null"
            :min-width="column.minWidth"
            :sortable="column.sortable"
          >
          </el-table-column>
          <el-table-column label="Producto">
             <template v-slot="scope">
              <router-link class="link" :to="`/products/product/${scope.row.id}`" style="text-decoration:none;">
            {{scope.row.mark +' '+scope.row.name}}
          </router-link>
            </template>
          </el-table-column>
          <el-table-column>
            <template v-slot="scope">
              <el-image class="product_image" :src=" 'data:image/jpeg;base64,' + scope.row.image "></el-image>
            </template>
          </el-table-column>
          <el-table-column label="Cantidad">
            <template v-slot="scope">
              <span>{{ scope.row.quantity }} </span>
            </template>
          </el-table-column>
          <el-table-column label="Precio Unidad">
            <template v-slot="scope">
              <span>{{ scope.row.price}}€</span>
            </template>
          </el-table-column>
          <el-table-column label="Precio Total">
            <template v-slot="scope">
              <span>{{ scope.row.total}}€</span>
            </template>
          </el-table-column>
        </el-table>
        </div>
        <el-divider></el-divider>
        <div class="el-card-container" style="width:100%;">

          <el-card class="box-card" style="width:100%; ">
            <div class="clearfix">
              <h1>Total del pedido</h1>
            </div>
            <div>
              <div class="left">
                <h4>Artículos:&nbsp;&nbsp;&nbsp; <span class="total"> {{ order.products.length }}</span></h4>
                <h4>Sub-Total:&nbsp;&nbsp;&nbsp; <span class="total">{{ order.total_amount }}€</span></h4>
                <h4>Gastos de envío:&nbsp;&nbsp;&nbsp; <span class="total">{{ order.shipping_cost }}€</span></h4>
                <h2>Total:&nbsp;&nbsp;&nbsp;<span class="total">{{parseFloat(order.total_amount) + parseFloat(Number(order.shipping_cost)).toFixed(2)}}€</span></h2>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
</template>
<script>
import router from '@/router'
export default {
  name: 'orderShow',
  data () {
    return {
      order: null,
      id: 12233,
      shoppingCart: [],
      products: null,
      subtotal: 5000,
      total: 5000,
      articulos: 4,
      gastosEnvio: 6.50,
      columns: [],
      tableData: []
    }
  },
  created () {
    this.order = null
    if (this.$route.params.order) {
      this.order = this.$route.params.order
      this.products = this.$route.params.order.items
    } else {
      const cachedOrder = localStorage.getItem('order')
      if (cachedOrder) {
        this.order = JSON.parse(cachedOrder)
        this.products = this.order.items
      }
    }
  },
  mounted () {
  },
  methods: {
    goBack () {
      router.push('/user/orders')
    },
    next () {
      if (this.active === 3) {
        this.active = 0
      } else if (this.active === 2) {
        this.active += 1
      } else {
        this.active++
      }
    }
  }
}
</script>
<style scoped>
.link{
  text-decoration: none;
  color: #76B9FF;
}
@font-face {
  font-family: "Zeniq Nano";
  src: url('@/assets/fonts/Zeniq Nano.otf');
}
.titulo{
  font-family: "Zeniq Nano";
  color: #00BAB4;
}
.content {
  margin-top: 12%;
  margin-bottom: 12%;
  padding-left: 50px;
  padding-right: 50px;
}

.page-header {
  margin-left: 30px;
}

.product_image {
  width: 40%;
}

.left {
  text-align: center;
  margin-right: 5px;
}

.right {
  display: grid;
  justify-content: left;
  margin-bottom: 120px;
}

.el-card-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.total {
  background: linear-gradient(#4657FD, #513AE6, #209b85, #17587b);
  font-family: system-ui;
  line-height: 115%;

  -webkit-text-fill-color: transparent;
  -webkit-background-clip: text;
  margin-top: 20px;
}

.center {
  text-align: center;
}
</style>
