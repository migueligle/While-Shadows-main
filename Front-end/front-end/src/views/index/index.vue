<template>
  <div class="content" v-loading="loading">
    <el-carousel class="carrusel" indicator-position="outside" :autoplay="true">
      <el-carousel-item v-for="banner in banners" :key="banner.id">
        <img :src="'data:image/jpeg;base64,' + banner.image" alt="banner" class="banner-image" style="height:100%;">
      </el-carousel-item>
    </el-carousel>
    <h2>Novedades</h2>
    <el-divider></el-divider>
    <el-row justify="center">
      <el-col :span="8" v-for="product in products" :key="product.id" style="margin-top: 20px;">
        <div class="card-container">
          <el-card class="body-style" shadow="hover">
            <div class="card-content">
              <a :href="`/products/product/${product.id}`"  class="product">
                <img :src="'data:image/jpeg;base64,' + product.image" class="image" />
                <h4>{{ product.mark.name + ' ' + product.name }}</h4>
              </a>
              <span v-if="product.is_stock==true">
                <i class="circle" style="background-color: rgb(0, 218, 0);"></i> Recíbelo en: 1-2 Días / Recógelo en tienda
              </span>
              <span v-else>
                <i class="circle" style="background-color: rgb(255, 120, 120);"></i> Sin Stock
              </span>
              <br>
              <span class="price"><b>{{ product.price }}€</b></span>
              <br>
              <div class="bottom clearfix">
                <el-button icon="el-icon-shopping-cart-2"  type="primary" plain  @click="AddProdductToShoppingCart(product.id)" circle></el-button>
              </div>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { fetchProductsBase } from '@/api/products.js'
import { fetchBannersBase } from '@/api/banners.js'
import { fetchAddShoppingCart } from '@/api/shoppingCart.js'
export default {
  name: 'Index-vue',
  data () {
    return {
      products: [],
      product: {},
      banners: [],
      banner: {},
      loading: false
    }
  },
  mounted () {
    this.loading = true
    this.fetchData()
    this.fetchDataBanners()
  },
  methods: {
    AddProdductToShoppingCart (productId) {
      const product = productId
      fetchAddShoppingCart({ product_id: product, quantity: 1 }).then((response) => {
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
    fetchData () {
      fetchProductsBase()
        .then((response) => {
          this.products = response.data.results.slice(0, -1)
        })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
        })
    },
    fetchDataBanners () {
      fetchBannersBase()
        .then((response) => {
          this.banners = response.data.results
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
.content {
  margin-top: 2px;
  padding-left: 200px;
  padding-right: 200px;
}

.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}

.card-container {
  text-align: center;
  margin-top: 20px;
}

.body-style {
  height: 590px;
}

.card-content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  padding: 14px;
}

.image {
  width: 50%;
  display: block;
  margin: 0 auto;
}

.banner-image {
  width: 100%;
  height: auto;
}

a {
  text-decoration: none;
  color: black;
}

.text {
  text-align: center;
}

@media screen and (max-width: 768px) {
  .content {
    padding: 10px;
  }

  .carrusel {
    margin-top: 60px;
  }
}

a {
  color: #fff;
}

.product {
  color: black;
}

.price {
  background: radial-gradient(#4657FD, #513AE6, #00b38f, #1d658c);
  font-family: system-ui;
  font-size: 25px;
  line-height: 115%;
  -webkit-text-fill-color: transparent;
  -webkit-background-clip: text;
  margin-top: 20px;
}

.stock-red {
  pointer-events: none;
  width: 1%;
  background-color: red;
}

.stock-green {
  border-radius: 90px;
  pointer-events: none;
  position: sticky;
  width: 0%;
  height: 2%;
  display: inline;
  background-color: green;
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
