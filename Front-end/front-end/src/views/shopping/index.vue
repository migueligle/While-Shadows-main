<template>
<div class="content">
    <div>
      <el-page-header class="page-header" @back="goBack"  title="Volver" content="Cesta">
    </el-page-header>
    <div>
      <img style="width: 8%; margin-right:18px" src="@/assets/ISOTIPO.png" alt="">
      <h1 class="titulo">Cesta</h1>
      <el-divider></el-divider><br><br>
      <el-table ref="table" :data="shoppingCart.items" stripe style="width: 100%">
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
            <router-link class="link" :to="`/products/product/${scope.row.product.id}`" style="text-decoration:none;">
            {{scope.row.product.mark +' '+scope.row.product.name}}
          </router-link>
          </template>
        </el-table-column>
        <el-table-column>
          <template v-slot="scope">
         <el-image class="product_image" :src="'data:image/jpeg;base64,' + scope.row.product.image"></el-image>
          </template>
        </el-table-column>
        <el-table-column label="Cantidad">
  <template v-slot="scope">
    <div class="quantity-container">
      <el-button size="mini" style="display: inline;" type="danger" icon="el-icon-minus" @click="decrementProduct(scope.row)"></el-button>
      <el-input  :disabled="true" style="width:30% ;" size="mini" v-model="scope.row.quantity" @change="handleChange(scope.row)"></el-input>
      <el-button size="mini" style="display:inline" type="primary" icon="el-icon-plus" @click="incrementProduct(scope.row)"></el-button>
    </div>
  </template>
</el-table-column>
        <el-table-column label="Precio Unidad">
          <template v-slot="scope">
            <span>{{ scope.row.product.price}}€</span>
          </template>
        </el-table-column>
        <el-table-column label="Precio Total">
          <template v-slot="scope">
            <span>{{ scope.row.product_total}}€</span>
          </template>
        </el-table-column>
        <el-table-column style="min-width: 120px;" >
      <template v-slot="props">
        <el-button
          size="mini"
          type="danger"
          @click="DeleteProduct(props.row.product)"><i class="el-icon-delete"></i></el-button>
      </template>
    </el-table-column>
      </el-table>

    </div>
    <el-divider></el-divider>
    <div class="right" style="display:inline;">
      <el-button style="width: 20%;  font-size: medium;" type="primary" @click="goBack(),scrollToTop()">
        <i class="el-icon-back"></i> Continuar comprando
      </el-button>
    </div>
    <div class="el-card-container">

      <el-card class="box-card"  style="width: 35%; ">
        <div class="clearfix">
          <h1>Total del pedido</h1>
        </div>
        <div>
          <div class="left">
            <h4>Artículos:&nbsp;&nbsp;&nbsp; <span class="total"> {{shoppingCart.product_count}}</span></h4>
            <h4>Sub-Total:&nbsp;&nbsp;&nbsp; <span class="total">{{ shoppingCart.total }}€</span></h4>
            <h4>Gastos de envío:&nbsp;&nbsp;&nbsp; <span class="total">{{  shoppingCart.shipping_cost }}€</span></h4>
            <h2>Total:&nbsp;&nbsp;&nbsp;<span class="total">{{ shoppingCart.total+Number(shoppingCart.shipping_cost)}}€</span></h2>
          </div>
          <div class="center">
            <el-divider ></el-divider>
              <el-button   @click="scrollToTop(),goShow()" style="width: 100%; font-size: medium;" type="primary">
                Tramitar Pedido <i class="el-icon-shopping-bag-1"></i>
              </el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
  </div>
</template>

<script>
import { fetchShoppingCart, fetchIncrementProduct, fetchDecrementProduct, fetchDeleteProduct } from '@/api/shoppingCart.js'
import router from '@/router'
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'ShoppingCartIndex',
  data () {
    return {
      shoppingCart: [],
      columns: []
    }
  },
  mounted () {
    this.fetchData()
    this.$store.dispatch('fetchShopping')
  },
  computed: {
    ...mapGetters(['getShoppingCart']),
    productCount () {
      return this.getShoppingCart.product_count
    }
  },
  methods: {
    ...mapActions(['fetchShopping']),
    incrementProduct (row) {
      fetchIncrementProduct({ product_id: row.product.id })
        .then((response) => {
          row.quantity++
          this.fetchData()
        })
        .catch((error) => {
          this.$message.error('Error incrementando el producto:', error)
        })
    },
    DeleteProduct (product) {
      fetchDeleteProduct({ product_id: product.id })
        .then(() => {
        })
        .catch((error) => {
          this.$message.error('Error al borrar el producto:', error)
        }).finally(() => {
          this.fetchData()
        })
    },
    decrementProduct (row) {
      fetchDecrementProduct({ product_id: row.product.id })
        .then((response) => {
          if (row.quantity > 1) {
            row.quantity--
            this.fetchData()
          } else {
            this.$message.error('No se puede decrementar más la cantidad del producto')
          }
        })
        .catch((error) => {
          this.$message.error('Error decrementando el producto', error)
        })
    },
    fetchData () {
      fetchShoppingCart()
        .then((response) => {
          this.shoppingCart = response.data
        })
        .catch(() => {
          this.$message.error('Error al cargar el carrito')
        })
    },
    goBack () {
      router.push('/')
    },
    goShow () {
      if (localStorage.getItem('color') && this.shoppingCart.product_count > 0) {
        router.push('/shoppingCart/ProcessOrder')
      } else if (localStorage.getItem('color') && this.shoppingCart.product_count === 0) {
        this.$notify.error({
          title: 'Error',
          message: 'Debes de tener al menos un producto para tramitar tu pedido '
        })
      } else {
        this.$notify.error({
          title: 'Error',
          message: 'Debes de estar registrado e iniciado sesión para poder tramitar tu pedido '
        })
      }
    },
    scrollToTop () {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    }
  }
}
</script>
<style scoped>
.quantity-container {
  display: flex;
  align-items: center;
}

.quantity-container > * {
  margin-right: 5px;
}
@font-face {
  font-family: "Zeniq Nano";
  src: url('@/assets/fonts/Zeniq Nano.otf');
}
.titulo{
  font-family: "Zeniq Nano";
  color: #00BAB4;
}
.link{
  text-decoration: none;
  color: #76B9FF;
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
.product_image{
  width: 40%;
}
.left{
  text-align: center;
  margin-right: 5px;
}
.right{
  display: grid;
  justify-content:left;
  margin-bottom:120px ;
}
.el-card-container {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 20px;
}
.total{
  background:linear-gradient(#4657FD,#513AE6,#209b85,#17587b);
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
