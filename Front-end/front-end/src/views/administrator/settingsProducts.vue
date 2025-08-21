<template>
  <div>
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Administración de Productos">
      </el-page-header>
    </div>
    <div class="content">
      <div>
  <el-col :sm="6" :md="4" :lg="2" :xl="1" >
  <el-input style="width:100%;"
    placeholder="Nombre"
    v-model="name"
    clearable
    @input="debounceInput">
  </el-input>
</el-col>
<el-col :sm="6" :md="6" :lg="4" :xl="2">
  <el-select
    placeholder="Stock"
    clearable
    v-model="is_stock"
    >
    <el-option label="Hay stock" value="true"></el-option>
    <el-option label="No hay stock" value="false"></el-option>
  </el-select>
</el-col>
<el-col :sm="6" :md="4.5" :lg="4" :xl="2" >
  <el-select
    v-model="is_active"
    placeholder="Activo"
    clearable>
    <el-option label="Todos" value="null"></el-option>
    <el-option label="Activo" value="true"></el-option>
    <el-option label="Inactivo" value="false"></el-option>
  </el-select>
</el-col>
<el-col :sm="6" :md="6" :lg="4" :xl="2">
  <el-select v-model="mar" placeholder="Marca" clearable filterable @change="dirtyFilter = true">
    <el-option :value="mark.id" :key="mark.id" :label="mark.name" v-for="mark in marks"></el-option>
  </el-select><br><br>
</el-col>
<el-col :sm="6" :md="6" :lg="4" :xl="2" >
  <el-select v-model="category" placeholder="Categoría" clearable filterable @change="dirtyFilter = true">
    <el-option :value="categorie.id" :key="categorie.id" :label="categorie.name" v-for="categorie in categories"></el-option>
  </el-select><br><br>
</el-col>
<el-col :sm="6" :md="4" :lg="2" :xl="2">
  <el-button icon="el-icon-search" @click="search">Buscar</el-button>
</el-col>
<el-col :sm="6" :md="4" :lg="2" :xl="1">
  <el-button type="primary" icon="el-icon-circle-plus" @click="dialogCreateVisible= true">Añadir Producto</el-button>
</el-col>
      </div>
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
        <el-table-column label="Stock">
          <template v-slot="scope">
            <i
            :style="scope.row.is_stock === true ? ' border-radius:10px; background-color:rgb(0, 218, 0);,color: white;' : ' border-radius:10px;background-color: rgb(255, 120, 120);,color: white;'"
            :class="scope.row.is_stock === true ? 'el-icon-check' : 'el-icon-close'"></i>
          </template>
        </el-table-column>
        <el-table-column label="Activo">
          <template v-slot="scope">
            <i
            :style="scope.row.is_active === true ? ' border-radius:10px; background-color:rgb(0, 218, 0);,color: white;' : ' border-radius:10px;background-color: rgb(255, 120, 120);,color: white;'"
            :class="scope.row.is_active === true ? 'el-icon-check' : 'el-icon-close'"></i>
          </template>
        </el-table-column>
        <el-table-column style="min-width: 120px;"
      label="Operaciones" >
      <template v-slot="props"  >
        <el-button
          size="mini"
          @click="handleEdit(props.$index, props.row)">Editar</el-button>
          <span v-if="props.row.is_active==true">
            <el-button size="mini" type="danger" @click="DesactivateProduct(props.$index, props.row)"><i class="el-icon-delete"></i></el-button>
          </span>
          <span v-else >
            <el-button size="mini" type="success" @click="DesactivateProduct(props.$index, props.row)"><i class="el-icon-refresh-left"></i></el-button>
          </span>
      </template>
    </el-table-column>

      </el-table>

      <el-pagination
        name="UsersList"
        layout="total, sizes, prev, pager, next"
        :total="pagination.total"
        :page-sizes="pagination.pageSizes"
        :page-size="pagination.pageSize"
        :current-page="pagination.page"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        background
      >
      </el-pagination>
    </div>
    <el-dialog
        :title="`Editar Producto`"
        :visible="dialogEditVisible"
        @before-close="dialogVisible = false"
        width="40%"
        :close-on-click-modal="true"
      >
       <div>
        <el-form :model="FromProduct" :rules="rules.FromProduct" ref="FromProduct" label-width="120px" class="demo-ruleForm">
    <el-form-item label="Nombre:" prop="name">
      <el-input v-model="FromProduct.name"></el-input>
    </el-form-item>
    <el-form-item label="Marca:" prop="mark">
      <el-select v-model="FromProduct.mark.id" placeholder="Marca" clearable filterable @change="dirtyFilter = true">
        <el-option :value="selectMark.id" :key="selectMark.id" :label="selectMark.name"  v-for="selectMark in selectMarks "></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Categoría:" prop="category">
      <el-select v-model="FromProduct.category.id" placeholder="Categoría" clearable filterable @change="dirtyFilter = true">
        <el-option :value="selectCategorie.id" :key="selectCategorie.id" :label="selectCategorie.name"  v-for="selectCategorie in selectCategories "></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Precio:" prop="price">
      <el-input-number v-model="FromProduct.price" :precision="2" :step="0.1" ></el-input-number>
    </el-form-item>
    <el-form-item label="Precio anterior" prop="before_price">
      <el-input-number v-model="FromProduct.before_price" :precision="2" :step="0.1" disabled></el-input-number>
    </el-form-item>
    <el-form-item label="Imágenes" required>
    <el-upload
    class="upload-demo"
    action="#"
    :on-change="handleChangeEdit"
    :file-list="fileListEdit"
    :auto-upload="false"
    :multiple="true"
    :limit=3
    list-type="picture-card">
    <i class="el-icon-plus"></i>
    </el-upload>
    </el-form-item>
    <el-form-item label="Descripción" prop="description">
      <el-input  type="textarea"  v-model="FromProduct.description"></el-input>
    </el-form-item>
    <el-form-item   label="Características:" prop="characteristics">
      <el-input  type="textarea" v-model="FromProduct.characteristics"></el-input>
    </el-form-item>
    <el-form-item   label="Video:" prop="video">
      <el-input  type="textarea" v-model="FromProduct.video"></el-input>
    </el-form-item>
    <el-form-item label="Stock" required>
      <el-switch v-model="FromProduct.is_stock"></el-switch>
      </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitEditProduct('FromProduct')">Guardar</el-button>
      <el-button @click="dialogEditVisible = false,resetForm('FromProduct')">Cancelar</el-button>
    </el-form-item>
  </el-form>
       </div>
      </el-dialog>
    <el-dialog
    :title="`Añadir Producto`"
    :visible="dialogCreateVisible"
    @before-close="dialogCreateVisible = false"
    width="40%"
    :close-on-click-modal="true"
  >
   <div>
    <el-form :model="FromCreateProduct" :rules="rules.FromCreateProduct" ref="FromCreateProduct" label-width="120px" class="demo-ruleForm">
<el-form-item label="Nombre:" prop="name">
  <el-input v-model="FromCreateProduct.name"></el-input>
</el-form-item>
<el-form-item label="Marca:" prop="mark">
  <el-select v-model="FromCreateProduct.mark" placeholder="Marca" clearable filterable @change="dirtyFilter = true">
    <el-option :value="selectMark.id" :key="selectMark.id" :label="selectMark.name"  v-for="selectMark in selectMarks "></el-option>
  </el-select>
</el-form-item>
<el-form-item label="Categoría:" prop="category">
  <el-select v-model="FromCreateProduct.category" placeholder="Categoría" clearable filterable @change="dirtyFilter = true">
    <el-option :value="selectCategorie.id" :key="selectCategorie.id" :label="selectCategorie.name"  v-for="selectCategorie in selectCategories "></el-option>
  </el-select>
</el-form-item>
<el-form-item label="precio:" prop="price">
  <el-input-number v-model="FromCreateProduct.price" :precision="2" :step="0.1" ></el-input-number>
</el-form-item>
<el-form-item label="precio anterior" prop="before_price">
  <el-input-number v-model="FromCreateProduct.before_price" :precision="2" :step="0.1" disabled></el-input-number>
</el-form-item>
<el-form-item label="Descripción" prop="description">
  <el-input  type="textarea"  v-model="FromCreateProduct.description"></el-input>
</el-form-item>
<el-form-item label="Imágenes" required>
  <el-upload
    class="upload-demo"
    action="#"
    :limit=3
    :on-change="handleChangeCreate"
    :file-list="fileList"
    :auto-upload="false"
    :multiple="true"
    list-type="picture-card">
    <i class="el-icon-plus"></i>
  </el-upload>
</el-form-item>

<el-form-item   label="Características:" prop="characteristics">
  <el-input  type="textarea" v-model="FromCreateProduct.characteristics"></el-input>
</el-form-item>
<el-form-item   label="Video:" prop="video">
  <el-input  type="textarea" v-model="FromCreateProduct.video"></el-input>
</el-form-item>
<el-form-item label="Stock" required>
  <el-switch v-model="FromCreateProduct.is_stock"></el-switch>
  </el-form-item>
<el-form-item>
  <el-button type="primary" @click="submitCreateProduct('FromCreateProduct')">Guardar</el-button>
  <el-button @click="dialogCreateVisible = false,resetForm('FromCreateProduct')">Cancelar</el-button>
</el-form-item>
</el-form>
   </div>
  </el-dialog>
  </div>
</template>

<script>
import router from '@/router'
import { fetchProducts, fetchCreateProduct, fetchDesactiveProduct, fetchEditProduct } from '@/api/products.js'
import { fetchMarks } from '@/api/marks.js'
import { fetchCategories } from '@/api/categories.js'

export default {
  data () {
    return {
      id: 0,
      num: 0,
      marks: [],
      category: '',
      mar: '',
      selectMark: '',
      selectCategorie: '',
      selectMarks: [],
      selectCategories: [],
      categories: [],
      is_stock: '',
      fileList: [],
      fileListEdit: [],
      dialogEditVisible: false,
      dialogdeleteVisible: false,
      dialogCreateVisible: false,
      name: '',
      is_active: '',
      showNewPassword: false,
      FromProduct: {
        images: [],
        mark: {
          id: '',
          name: ''
        },
        category: {
          id: '',
          name: ''
        }
      },
      FromCreateProduct: {
        images: [],
        image: null,
        image_two: null,
        image_three: null
      },
      rules: {
        FromProduct: {
          name: [
            { required: true, message: 'El nombre es requerido', trigger: 'blur' }
          ],
          mark: [
            { required: true, message: 'La marca es requerida', trigger: 'change' }
          ],
          category: [
            { required: true, message: 'La categoría es requerida', trigger: 'change' }
          ],
          price: [
            { required: true, message: 'El precio es requerido', trigger: 'blur' },
            { type: 'number', message: 'El precio debe ser un número', trigger: 'blur' }
          ],
          description: [
            { required: true, message: 'La descripción es requerida', trigger: 'blur' }
          ],
          characteristics: [
            { required: true, message: 'Las características son requeridas', trigger: 'blur' }
          ],
          video: [
            { required: false }
          ]
        },
        FromCreateProduct: {
          name: [
            { required: true, message: 'El nombre es requerido', trigger: 'blur' }
          ],
          mark: [
            { required: true, message: 'La marca es requerida', trigger: 'change' }
          ],
          category: [
            { required: true, message: 'La categoría es requerida', trigger: 'change' }
          ],
          price: [
            { required: true, message: 'El precio es requerido', trigger: 'blur' },
            { type: 'number', message: 'El precio debe ser un número', trigger: 'blur' }
          ],
          description: [
            { required: true, message: 'La descripción es requerida', trigger: 'blur' }
          ],
          characteristics: [
            { required: true, message: 'Las características son requeridas', trigger: 'blur' }
          ],
          video: [
            { required: false }
          ]
        }
      },
      columns: [
        {
          prop: 'id',
          label: 'ID',
          minWidth: '40px',
          sortable: true,
          formatter: row => row.id || '-'
        },
        {
          prop: 'name',
          label: 'Nombre',
          minWidth: '80px',
          sortable: true,
          formatter: row => row.name || '-'
        },
        {
          prop: 'price',
          label: 'Precio',
          minWidth: '120px',
          sortable: true,
          formatter: row => row.price + '€' || '-'
        },
        {
          prop: 'before_price',
          label: 'Precio Anterior',
          minWidth: '80px',
          sortable: true,
          formatter: row => row.before_price || '-'
        },
        {
          prop: 'mark',
          label: 'Marca',
          minWidth: '80px',
          sortable: true,
          formatter: row => row.mark.name || '-'
        }
      ],
      pagination: {
        page: 1,
        total: 0,
        pageSizes: [10, 25, 50, 100],
        pageSize: 25
      },
      products: []
    }
  },
  async mounted () {
    this.fetchDataCategories()
    this.fetchDataMarks()
    this.fetchData()
  },
  methods: {
    DesactivateProduct (index, row) {
      const ProductId = row.id
      fetchDesactiveProduct(ProductId)
        .then((response) => {
          const message = response.data.message
          this.$message.success(message)
        })
        .catch((error) => {
          console.error('Error al desactivar el Producto:', error)
          this.$message.error('Error al desactivar el producto. Por favor, inténtalo de nuevo.')
        }).finally(() => {
          this.fetchData()
          this.loading = false
        })
    },
    resetForm (formName) {
      if (this.$refs[formName]) {
        this.$refs[formName].resetFields()
      } else {
        console.error('Formulario no encontrado:', formName)
      }
    },
    handleChangeEdit (file, fileListEdit) {
      const validFiles = fileListEdit.filter(file => file.raw instanceof Blob)
      const filesToConvert = validFiles.map(file => file.raw)
      Promise.all(filesToConvert.map(this.convertToBase64))
        .then(base64Images => {
          const imageUrls = ['image', 'image_two', 'image_three']
          imageUrls.forEach((url, index) => {
            if (this.FromProduct[url]) {
              this.FromProduct[url] = 'data:image/jpeg;base64,' + base64Images[index]
            }
          })

          this.fileListEdit = fileListEdit
        })
        .catch(error => {
          console.error('Error convirtiendo las imágenes a base64:', error)
          this.$message.error('Error al cargar las imágenes')
        })
    },
    handleChangeCreate (file, fileList) {
      this.fileList = fileList
      const rawImages = fileList.map(file => file.raw)
      this.FromCreateProduct.images = rawImages
    },
    convertToBase64 (file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result.split(',')[1])
        reader.onerror = error => reject(error)
      })
    },
    fetchDataMarks () {
      const params = {
        page_size: 100
      }
      fetchMarks(params)
        .then(response => {
          this.marks = response.data.results
          this.selectMarks = response.data.results
        })
        .catch(error => {
          console.error('Error al recuperar datos', error)
        })
    },
    fetchDataCategories () {
      const params = {
        page_size: 100
      }
      fetchCategories(params)
        .then(response => {
          this.categories = response.data.results
          this.selectCategories = response.data.results
        })
        .catch(error => {
          console.error('Error al recuperar datos', error)
        })
    },
    goBack () {
      router.push('/admin')
    },
    search () {
      this.pagination.page = 1
      this.fetchData()
    },
    debounceInput: function () {
      if (this.debouncedInput) {
        clearTimeout(this.debouncedInput)
      }
      this.debouncedInput = setTimeout(() => {
        this.searchByName()
      }, 500)
    },
    fetchData (page) {
      this.loading = true
      const params = {
        page: page || this.pagination.page,
        page_size: this.pagination.pageSize
      }
      if (this.mar != null && this.mar !== '') {
        params.mark = this.mar
      }
      if (this.name != null && this.name !== '') {
        params.name = this.name
      }
      if (this.category != null && this.category !== '') {
        params.category = this.category
      }
      if (this.category != null && this.category !== '') {
        params.category = this.category
      }
      if (this.is_stock != null && this.is_stock !== '') {
        params.is_stock = this.is_stock
      }
      if (this.is_active != null && this.is_active !== '') {
        params.is_active = this.is_active
      }
      fetchProducts(params)
        .then(response => {
          this.products = response.data.results
          this.pagination.total = response.data.count
          this.loading = false
        })
        .catch(error => {
          console.error('Error al recuperar datos', error)
          this.loading = false
        })
    },
    handleCurrentChange (newPage) {
      this.pagination.page = newPage
      this.fetchData(newPage)
    },
    handleSizeChange (pageSize) {
      this.pagination.pageSize = pageSize
      this.fetchData()
    },
    handleEdit (index, row) {
      this.dialogEditVisible = true
      this.FromProduct = { ...row }
      const fileListEdit = [
        { name: 'image', url: 'data:image/jpeg;base64,' + this.FromProduct.image },
        { name: 'image_two', url: 'data:image/jpeg;base64,' + this.FromProduct.image_two },
        { name: 'image_three', url: 'data:image/jpeg;base64,' + this.FromProduct.image_three }
      ].filter(image => image.url)
      this.fileListEdit = fileListEdit
    },
    handleDelete (index, row) {
      this.dialogdeleteVisible = true
      this.$set(this, 'ruleForm', { ...row })
    },
    searchByName () {
      if (this.name.trim() !== '') {
        this.fetchData()
      }
    },
    vieNewPassword () {
      if (this.showNewPassword === false) {
        this.showNewPassword = true
      } else {
        this.showNewPassword = false
      }
    },
    submitCreateProduct (form) {
      if (this.$refs[form]) {
        this.$refs[form].validate(valid => {
          if (valid) {
            if (this.fileList.length < 3) {
              this.$message.error('Por favor, carga las  imagen antes de enviar el formulario.')
              return
            }
            const imagesBase64 = this.fileList.map(file => this.convertToBase64(file.raw))
            Promise.all(imagesBase64).then(base64Images => {
              this.FromCreateProduct.image = base64Images[0]
              this.FromCreateProduct.image_two = base64Images[1]
              this.FromCreateProduct.image_three = base64Images[2]
              fetchCreateProduct(this.FromCreateProduct)
                .then(() => {
                  this.$message.success('Producto añadido correctamente')
                  this.dialogCreateVisible = false
                })
                .catch(() => {
                  this.$message.error('Error al crear el producto')
                })
                .finally(() => {
                  this.fetchData()
                  this.loading = false
                })
            }).catch(error => {
              console.error('Error convirtiendo las imágenes a base64:', error)
              this.$message.error('Error al cargar las imágenes')
            })
          } else {
            this.$message.error('Por favor, completa correctamente el formulario.')
          }
        })
      } else {
        console.error('Referencia al formulario no encontrada:', form)
      }
    },
    submitEditProduct (form) {
      if (this.$refs[form]) {
        this.$refs[form].validate(valid => {
          if (valid) {
            const imagesBase64 = this.fileListEdit.map(file => {
              if (file.url && file.url.startsWith('data:image/jpeg;base64,')) {
                return Promise.resolve(file.url.split(',')[1])
              } else {
                return this.convertToBase64(file.raw)
              }
            })

            Promise.all(imagesBase64)
              .then(base64Images => {
                const imageUrls = ['image', 'image_two', 'image_three']
                imageUrls.forEach((url, index) => {
                  if (this.FromProduct[url]) {
                    this.FromProduct[url] = 'data:image/jpeg;base64,' + base64Images[index]
                  }
                })
                this.FromProduct.mark = this.FromProduct.mark.id
                this.FromProduct.category = this.FromProduct.category.id
                fetchEditProduct(this.FromProduct)
                  .then(() => {
                    this.$message.success('Producto editado correctamente')
                    this.dialogEditVisible = false
                  })
                  .catch(() => {
                    this.$message.error('Error al editar el producto')
                  })
                  .finally(() => {
                    this.fetchData()
                    this.loading = false
                  })
              })
              .catch(error => {
                console.error('Error convirtiendo las imágenes a base64:', error)
                this.$message.error('Error al cargar las imágenes')
              })
          } else {
            this.$message.error('Por favor, completa correctamente el formulario.')
          }
        })
      } else {
        console.error('Referencia al formulario no encontrada:', form)
      }
    }
  }
}
</script>

<style scoped>
.content {
  margin-top: 12%;
  margin-bottom: 12%;
  padding-left: 50px;
  padding-right: 50px;
}
.page-header {
  margin-left: 30px;
}
</style>
