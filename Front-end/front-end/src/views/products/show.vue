<template>
  <div class="content">
      <div>
        <el-page-header class="page-header" @back="goBack" title="Volver" :content="product && product.mark ? `${product.mark.name} ${product.name}` : ''">
        </el-page-header>
      </div>
    <div>
      <h1 class="product_name">{{`${product.mark ? product.mark.name:'' }  ${product ? product.name: '' }`}}</h1>
      <div class="wrapper">
        <el-carousel :interval="900000000" indicator-position="outside" :autoplay=false  style="width: 90%;height: 90%;">
        <el-carousel-item v-for="(image, index) in [product.image, product.image_two, product.image_three]" :key="index" >
          <img :src="'data:image/jpeg;base64,' + image" alt=""  @click="openDialog(image)" style="width: 40%;">
        </el-carousel-item>
      </el-carousel>
    <div class="description">
    <p>{{ product.description }}</p>
    <el-divider></el-divider>
  <h1 class="price">{{ product.price }}€</h1>
  <el-divider></el-divider>
  <br>
  <span v-if="product.is_stock==true">
    <i class="circle" style="background-color: rgb(0, 218, 0);"></i> Recíbelo en: 1-2 Días / Recógelo en tienda
  </span>
  <span v-else>
    <i class="circle" style="background-color: rgb(255, 120, 120);"></i> Sin Stock
  </span>
  <br><br><br>
  <el-input-number v-model="quantity" @change="handleChange" :min="1" ></el-input-number><br><br><br>
  <el-button type="primary" plain class="button-add-cart" icon="el-icon-shopping-cart-1"  @click="AddProdductToShoppingCart(product.id)">Añadir al carrito</el-button>
</div>
    </div>
    </div>
    <el-dialog class="dial" :visible="dialogVisible" @update:visible="updateDialogVisible" @before-close="dialogVisible = false" width="40%">
      <div class="img-dialog" >
        <img :src="'data:image/jpeg;base64,' + dialogImage" alt=""  style="width: 70%;">
      </div>
    </el-dialog>
<el-container>
    <el-main style="margin-top: 180px;">
      <h2>Características </h2>
     <pre style=" font-family: system-ui;font-size: 15px;">{{ product.characteristics}}</pre><br>
      <br><br>
      <div v-html="product.video"></div>
    </el-main>
  </el-container>
  </div>
</template>
<script>
import { fetchDateProductBase } from '@/api/products.js'
import { fetchAddShoppingCart } from '@/api/shoppingCart.js'
import router from '@/router'

export default {
  name: 'product_while',
  props: ['product_id'],
  data () {
    return {
      quantity: 1,
      dialogVisible: false,
      product: {},
      dialogImage: '',
      category: {
        name: 'nombre categoría'
      },
      productId: this.$route.params.productId ? this.$route.params.productId : null
    }
  },
  mounted () {
    this.fetchData()
  },
  methods: {
    AddProdductToShoppingCart (productId) {
      const product = productId
      fetchAddShoppingCart({ product_id: product, quantity: this.quantity }).then((response) => {
        const message = 'Producto agregado al carrito'
        this.$message.success(message)
      })
        .catch(() => {
          this.$message.error('Error al agregar el Producto, tienes que estar logueado')
        }).finally(() => {
          this.fetchData()
          this.$store.dispatch('fetchShopping')
          this.loading = false
        })
    },
    updateDialogVisible (value) {
      this.dialogVisible = value
    },
    goBack () {
      router.push('/products')
    },
    handleChange (value) {
    },
    openDialog (image) {
      this.dialogImage = image
      this.dialogVisible = true
    },
    fetchData () {
      const params = {
        productId: this.productId
      }
      fetchDateProductBase(params)
        .then((response) => {
          this.product = response
          this.loading = false
        })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
          router.push('/notFound')
          this.loading = false
        })
    }
  }
}
</script>
<style scoped>
.stock-red{
  pointer-events:none;
  width: 2%;
  background-color: red;
}
.stock-green{
  pointer-events:none;
  width: 2%;
  display: inline;
  background-color: green;
}
.description{
  width: 60%;
  justify-content: center;
}
.img-dialog{
  display: flex;
  justify-content: center;
}
.wrapper{
  display: flex;
  flex-direction: row;
  align-items: center;

}
.button-add-cart{
  width: 80%;
  height: 60px;
  font-size: 20px;
  border-radius: 20px;

}
.price{
  background:radial-gradient(#4657FD,#513AE6,#04E0B5,#2893CC);
  font-family: system-ui;
  font-size: 4rem;
  line-height: 115%;
  margin-top: 20px;
}
.product_name{

  margin-top: 90px;
  margin-right: 60%;
}
.el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }
  .el-carousel{
    margin-top: 80px;
    margin-right: 200px;
    width: 100%;
    height: 100%
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #ffffff;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #ffffff;
  }
.content {
  margin-top: 2px;
  padding-left: 200px;
  padding-right: 200px;
  margin-bottom: 200px;

}

h3 {
  list-style: none;
  display: inline-flex;
  text-decoration: none;
  color: black;
}
.time {
  font-size: 13px;
  color: #999;
}

.card-colum {
  margin: 0, 10px;
  padding: 0, 30px;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.button-filter {
  width: 5%;
  height: 5%;
  display: block;
}

.image {

  width: 100%;
  display: block;
}

.card-ad:hover {
  background-color: rgba(230, 230, 230, 0.6);
}

.content {
  margin-top: 2px;
  padding-left: 200px;
  padding-right: 200px;

}

.page-header {
  margin-left: 30px;
}

.img-filter {
  width: 100%;
  display: block;
}
.circle {
  display: inline-block;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  vertical-align: middle;
}

.el-icon-check::before,
.el-icon-close::before {
  display: none;
}
</style>
