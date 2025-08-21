<template>
  <div class="content" v-loading="loading">
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Productos">
      </el-page-header>
    </div>
    <h2>Productos</h2>
    <el-divider></el-divider>
    <el-col>
      <el-tooltip class="item" content="Filtrar" placement="bottom" effect="dark">
        <el-button class="button-filter" style="border-radius: 10px;" @click="dialogVisible = true">
          <img class="img-filter" src="../../assets/icons/toggle-button_8727934.png" alt="" >
        </el-button>
      </el-tooltip>
    </el-col>
    <div  v-if="products.length<=0">
      <el-col style="margin-top: 20px;">
        <el-empty description="No hay datos"></el-empty>
      </el-col>
    </div>
    <div v-else>
      <el-col :span="8" v-for="product in products" :key="product.id" style="margin-top: 20px;">
        <el-card class="body-style" shadow="hover">
          <div style="padding: 14px;">
            <router-link :to="`/products/product/${product.id}`">
              <img :src="'data:image/jpeg;base64,' + product.image" class="image">
              <h3>{{ product.mark.name + ' ' + product.name }}</h3><br>
            </router-link><br><br>
            <span v-if="product.is_stock==true">
              <i class="circle" style="background-color: rgb(0, 218, 0);"></i> Recíbelo en: 1-2 Días / Recógelo en tienda
            </span>
            <span v-else>
              <i class="circle" style="background-color: rgb(255, 120, 120);"></i> Sin Stock
            </span><br><br>
            <span class="price" style="font-size: 25px;"><b>{{ product.price }}€</b></span><br><br>
            <div class="bottom clearfix">
              <el-tooltip class="item" content="Añadir al carrito" placement="bottom" effect="dark">
                <el-button icon="el-icon-shopping-cart-2"  type="primary" plain  @click="AddProdductToShoppingCart(product.id)" circle></el-button>
              </el-tooltip>
            </div>
          </div>
        </el-card>
      </el-col>
    </div>
      <el-dialog class="dial" title="Filtrar.." :visible="dialogVisible" @update:visible="updateDialogVisible" @before-close="dialogVisible = false" width="40%">
      <div>
        <el-select v-model="filter.mark" placeholder="marca" clearable filterable @change="dirtyFilter = true">
          <el-option :value="mark.id" :key="mark.id" :label="mark.name" v-for="mark in marks"></el-option>
        </el-select><br><br>
        <el-select v-model="filter.category" placeholder="Categoría" clearable filterable @change="dirtyFilter = true">
          <el-option :value="category.id" :key="category.id" :label="category.name" v-for="category in categories"></el-option>
        </el-select><br><br>
        <div class="block">
          <h3>Precio:</h3>
          <el-slider v-model="sliderValues" range show-stops :max="4000" :marks="marcas">
          </el-slider>
        </div>
        <br><br>
        <el-button type="primary" name="applyFilters" @click="fetchData()" :disabled="loading">Aplicar Filtros</el-button>
        <el-button type="danger" @click="clearFilters" v-if="isFilter"><i class="el-icon-delete"></i></el-button>
      </div>
    </el-dialog>
    <el-col style="margin-top: 20px;">
      <el-pagination
      :current-page="pagination.page"
      :page-sizes="pagination.pageSizes"
      :page-size="pagination.pageSize"
      :total="pagination.total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
     layout="total, sizes, prev, pager, next"
      background
    >
  </el-pagination>
    </el-col>
  </div>
</template>

<script>
import router from '@/router'
import { fetchProductsBase } from '@/api/products.js'
import { fetchMarksBase } from '@/api/marks.js'
import { fetchCategoriesBase } from '@/api/categories.js'
import { fetchAddShoppingCart } from '@/api/shoppingCart.js'

export default {
  name: 'ProductsList',
  props: ['CategoryId'],
  data () {
    return {
      dialogVisible: false,
      sliderValues: [0, 4000],
      loading: false,
      marks: [],
      mark: {},
      products: [],
      categories: [],
      filter: {
        min_price: null,
        max_price: null,
        mark: null,
        category: this.$route.params.CategoryId ? this.$route.params.CategoryId : null,
        name: null,
        is_stock: null
      },
      pagination: {
        page: 1,
        total: 0,
        pageSizes: [25, 50, 100],
        pageSize: 25
      },
      marcas: {
        0: '0',
        100: '100',
        500: '500',
        1000: '1000',
        1500: '1500',
        2000: '2000',
        2500: '2500',
        3000: '3000',
        3500: '3500'
      }
    }
  },
  async mounted () {
    await this.fetchDataCategories()
    this.fetchDataMarks()
    await this.fetchData()
  },
  methods: {
    AddProdductToShoppingCart (productId) {
      const product = productId
      fetchAddShoppingCart({ product_id: product, quantity: 1 }).then((response) => {
        const message = 'Producto agregado al carrito'
        this.$message.success(message)
      })
        .catch(() => {
          this.$message.error('Error al agregar el Producto, inténtalo de nuevo.')
        }).finally(() => {
          this.fetchData()
          this.$store.dispatch('fetchShopping')
          this.loading = false
        })
    },
    handleSizeChange (pageSize) {
      this.pagination.pageSize = pageSize
      this.fetchData()
    },
    handleCurrentChange (page) {
      this.pagination.page = page
      this.fetchData(page)
    },
    updateDialogVisible (value) {
      this.dialogVisible = value
    },
    fetchDataMarks () {
      const params = {
        page_size: 100
      }
      fetchMarksBase(params)
        .then((response) => {
          this.marks = response.data.results
        })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
        })
    },
    clearFilters () {
      this.filter.min_price = null
      this.filter.max_price = null
      this.filter.mark = null
      this.filter.category = null
      this.filter.name = null
      this.filter.is_stock = null
      this.sliderValues = [0, 4000]
      this.fetchData()
    },
    goBack () {
      router.push('/')
    },
    async fetchData (page = 1) {
      this.loading = true
      const params = {
        page: page,
        page_size: this.pagination.pageSize,
        mark: this.filter.mark,
        category: this.filter.category,
        min_price: this.sliderValues[0],
        max_price: this.sliderValues[1]
      }
      try {
        const response = await fetchProductsBase(params)
        this.products = response.data.results
        this.pagination.total = response.data.count
        this.loading = false
      } catch (error) {
        console.error('Error al recuperar datos', error)
        this.loading = false
      }
    },
    fetchDataCategories () {
      const params = {
        page_size: 100
      }
      fetchCategoriesBase(params)
        .then((response) => {
          this.categories = response.data.results
        })
        .catch((error) => {
          console.error('Error fetching categories:', error)
        })
    }
  },
  computed: {
    isFilter () {
      return (
        this.filter.min_price !== null ||
        this.filter.max_price !== null ||
        this.filter.mark !== null ||
        this.filter.category !== null ||
        this.sliderValues[0] !== 0 ||
        this.sliderValues[1] !== 4000
      )
    },
    filteredProducts () {
      return this.products.filter(filter => filter.category === this.$route.params.category)
    }
  }
}
</script>
<style scoped>
.image {
  width: 100%;
  display: block;
  max-width: 150px;
  display: block;
  margin: 0 auto;
}

.content {
  margin-top: 2px;
  padding-left: 200px;
  padding-right: 200px;
}

h3 {
  list-style: none;
  display: inline-flex;
  text-decoration: none;
  color: black;
}

.card-container {
  text-align: center;
  margin-top: 20px;
}

.body-style {
  height: 570px;
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

.card-ad {
  border-radius: 15%;
  width: 100%;
}

.time {
  font-size: 13px;
  color: #999;
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

.card-ad:hover {
  background-color: rgba(230, 230, 230, 0.6);
}

.content {
  margin-top: 107.5px;
  margin-bottom: 107.5px;
}

.page-header {
  margin-left: 30px;
}

.img-filter {
  width: 80%;
  display: block;
}

.price {
  background: radial-gradient(#4657FD, #513AE6, #04c09a, #227fb0);
  font-family: system-ui;
  font-size: 4rem;
  line-height: 115%;
  -webkit-text-fill-color: transparent;
  -webkit-background-clip: text;
  margin-top: 20px;
}

.stock-red {
  pointer-events: none;
  width: 2%;
  background-color: red;
}

.stock-green {
  pointer-events: none;
  width: 2%;
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
