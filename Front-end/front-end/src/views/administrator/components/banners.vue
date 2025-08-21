<template>
  <div>
    <div class="content">
      <div>
        <el-col :sm="8" :md="6" :lg="4" :xl="2">
          <el-input
            placeholder="Nombre"
            v-model="bannerName"
            clearable
            @input="debounceInput">
          </el-input>
        </el-col>
        <el-col :sm="8" :md="6" :lg="4" :xl="2">
          <el-select
            v-model="isActive"
            placeholder="Activo"
            clearable>
            <el-option label="Activos" value="true"></el-option>
            <el-option label="No Activos" value="false"></el-option>
          </el-select>
        </el-col>
        <el-col :sm="8" :md="6" :lg="4" :xl="2">
          <el-button icon="el-icon-search" @click="search">Buscar</el-button>
        </el-col>
        <el-col :sm="6" :md="4" :lg="2" :xl="1">
          <el-button type="primary" icon="el-icon-circle-plus" @click="dialogCreateVisible = true">Añadir Banner</el-button>
        </el-col>
      </div>
      <el-table ref="table" :data="filteredBanners" stripe style="width: 100%">
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
        <el-table-column label="Activo">
          <template v-slot="scope">
            <i
              :style="scope.row.is_active === true ? 'border-radius:10px; background-color:rgb(0, 218, 0); color: white;' : 'border-radius:10px; background-color: rgb(255, 120, 120); color: white;'"
              :class="scope.row.is_active === true ? 'el-icon-check' : 'el-icon-close'"></i>
          </template>
        </el-table-column>
        <el-table-column style="min-width: 120px;"
          label="Operaciones" >
          <template v-slot="props" >
            <el-button
              size="mini"
              @click="handleEdit(props.$index, props.row)"><i class="el-icon-edit"></i></el-button>
              <span v-if="props.row.is_active==true">
                <el-button size="mini" type="danger" @click="handleDesactive(props.$index, props.row)"><i class="el-icon-delete"></i></el-button>
              </span>
              <span v-else >
                <el-button size="mini" type="success" @click="handleActivate(props.$index, props.row)"><i class="el-icon-refresh-left"></i></el-button>
              </span>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        name="BannerList"
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
      :title="`Crear Banner`"
      :visible="dialogCreateVisible"
      @before-close="dialogCreateVisible = false"
      width="40%"
      :close-on-click-modal="true"
    >
      <div>
        <el-form :model="formCreateBanner" :rules="rules.create" ref="formCreateBanner" label-width="120px" class="demo-ruleForm">
          <el-form-item label="Nombre:" prop="name">
            <el-input v-model="formCreateBanner.name"></el-input>
          </el-form-item>
          <el-form-item label="Imagen" required>
            <el-upload
              class="upload-demo"
              action="#"
              :limit="1"
              :on-change="handleChangeCreate"
              :file-list="fileList"
              :auto-upload="false"
              :multiple="true"
              list-type="picture-card">
              <i class="el-icon-plus"></i>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitCreateBanner('formCreateBanner')">Guardar</el-button>
            <el-button @click="dialogCreateVisible = false, resetForm('formCreateBanner')">Cancelar</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>
    <el-dialog
      :title="`Editar Banner`"
      :visible="dialogEditVisible"
      @before-close="dialogVisible = false"
      width="40%"
      :close-on-click-modal="true"
    >
      <div>
        <el-form :model="formEditBanner" :rules="rules.edit" ref="formEditBanner" label-width="120px" class="demo-ruleForm">
          <el-form-item label="Nombre:" prop="name">
            <el-input v-model="formEditBanner.name"></el-input>
          </el-form-item>
          <el-form-item label="Imagen"  prop="image" required>
            <el-upload
              class="upload-demo"
              action="#"
              :limit="1"
              :on-change="handleChangeEdit"
              :file-list="fileListEdit"
              :auto-upload="false"
              :multiple="false"
              list-type="picture-card">
              <i v-if="fileListEdit.length === 0" class="el-icon-plus"></i>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="dialogEditVisible = false, submitEditBanner('formEditBanner')">Guardar</el-button>
            <el-button @click="dialogEditVisible = false, resetForm('formEditBanner')">Cancelar</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>
    <el-dialog
      title="Desactivar Banner"
      :visible="dialogDesactiveVisible"
      @before-close="dialogDesactiveVisible = false"
      width="40%"
      :close-on-click-modal="true"
    >
      <div>
        <h3>¿Estás seguro de que quieres desactivar el banner?</h3>
        <el-button type="danger" @click="dialogDesactiveVisible = false, desactivateBanner('formEditBanner')">Desactivar</el-button>
        <el-button @click="dialogDesactiveVisible = false">Cancelar</el-button>
      </div>
    </el-dialog>
    <el-dialog
      title="Activar Banner"
      :visible="dialogActivateVisible"
      @before-close="dialogActivateVisible = false"
      width="40%"
      :close-on-click-modal="true"
    >
      <div>
        <h3>¿Estás seguro de que quieres activar el banner?</h3>
        <el-button type="success" @click="dialogActivateVisible = false, desactivateBanner('formEditBanner')">Activar</el-button>
        <el-button @click="dialogActivateVisible = false">Cancelar</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import router from '@/router'
import { fetchBanners, fetchEditBanner, fetchCreateBanner, fetchDesactiveBanner } from '@/api/banners'

export default {
  name: 'BannerShow',
  data () {
    return {
      banners: [],
      dialogActivateVisible: false,
      filteredBanners: [],
      dialogEditVisible: false,
      dialogDesactiveVisible: false,
      bannerName: '',
      dialogCreateVisible: false,
      formCreateBanner: {},
      formEditBanner: {},
      isActive: null,
      fileList: [],
      fileListEdit: [],
      rules: {
        create: {
          name: [
            { required: true, message: 'El nombre es requerido', trigger: 'blur' }
          ],
          image: [
            { required: true, message: 'La imagen es requerida', trigger: 'change' }
          ]
        },
        edit: {
          name: [
            { required: true, message: 'El nombre es requerido', trigger: 'blur' }
          ],
          image: [
            { required: true }
          ]
        }
      },
      columns: [
        {
          prop: 'id',
          label: 'ID',
          minWidth: '40px',
          sortable: true,
          formatter: (row) => row.id
        },
        {
          prop: 'name',
          label: 'Nombre',
          minWidth: '80px',
          sortable: true,
          formatter: (row) => row.name ? row.name : ''
        }
      ],
      pagination: {
        page: 1,
        total: 0,
        pageSizes: [10, 25, 50, 100],
        pageSize: 25
      },
      loading: false,
      debouncedInput: null,
      ruleForm: {}
    }
  },
  methods: {
    convertToBase64 (file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result.split(',')[1])
        reader.onerror = error => reject(error)
      })
    },
    handleChangeCreate (file, fileList) {
      this.fileList = fileList
      if (fileList.length > 0) {
        const fileReader = new FileReader()
        fileReader.onload = (event) => {
          this.formCreateBanner.image = event.target.result
        }
        fileReader.readAsDataURL(file.raw)
      } else {
        this.formCreateBanner.image = ''
      }
    },
    handleChangeEdit (file, fileList) {
      this.fileListEdit = fileList
      if (fileList.length > 0) {
        const fileReader = new FileReader()
        fileReader.onload = (event) => {
          this.formEditBanner.image = event.target.result
        }
        fileReader.readAsDataURL(file.raw)
      } else {
        this.formEditBanner.image = ''
      }
    },
    submitEditBanner (form) {
      if (this.$refs[form]) {
        this.$refs[form].validate(valid => {
          if (valid) {
            fetchEditBanner(this.formEditBanner)
              .then(() => {
                this.$message.success('Banner editado correctamente')
                this.dialogCreateVisible = false
              })
              .catch(() => {
                this.$message.error('Error al editar el banner')
              })
              .finally(() => {
                this.fetchData()
                this.loading = false
              })
          } else {
            this.$message.error('Por favor, completa correctamente el formulario.')
          }
        })
      } else {
        console.error('Error en el formulario', form)
      }
    },
    submitCreateBanner (form) {
      if (this.$refs[form]) {
        this.$refs[form].validate(valid => {
          if (valid) {
            if (this.fileList.length === 0) {
              this.$message.error('Por favor, carga una imagen antes de enviar el formulario.')
              return
            }
            fetchCreateBanner(this.formCreateBanner)
              .then(() => {
                this.$message.success('Banner añadido correctamente')
                this.dialogCreateVisible = false
              })
              .catch(() => {
                this.$message.error('Error al crear el banner')
              })
              .finally(() => {
                this.fetchData()
                this.loading = false
              })
          } else {
            this.$message.error('Por favor, completa correctamente el formulario.')
          }
        })
      } else {
        console.error('Referencia al formulario no encontrada:', form)
      }
    },
    desactivateBanner () {
      const bannerId = this.ruleForm.id
      fetchDesactiveBanner(bannerId)
        .then((response) => {
          const message = response.data.message
          this.$message.success(message)
        })
        .catch((error) => {
          console.error('Error al desactivar el banner:', error)
          this.$message.error('Error al desactivar el banner. Por favor, inténtalo de nuevo.')
        }).finally(() => {
          this.fetchData()
          this.loading = false
        })
    },
    goBack () {
      router.push('/admin')
    },
    search () {
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
    fetchData (page, pageSize) {
      this.loading = true
      const params = {
        page: page || this.pagination.page,
        page_size: pageSize || this.pagination.pageSize
      }
      if (this.bannerName != null && this.bannerName !== '') {
        params.name = this.bannerName
      }
      if (this.isActive != null && this.isActive !== '') {
        params.is_active = this.isActive
      }
      fetchBanners(params)
        .then((response) => {
          this.banners = response.data.results
          this.pagination.total = response.data.count
          this.filteredBanners = this.banners
        })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
        }).finally(() => {
          this.loading = false
        })
    },
    handleCurrentChange (newPage) {
      this.pagination.page = newPage
      this.fetchData()
    },
    handleEdit (index, row) {
      this.dialogEditVisible = true
      this.$set(this, 'formEditBanner', { ...row })
      const fileListEdit = [
        { name: 'image', url: 'data:image/jpeg;base64,' + this.formEditBanner.image }]
      this.fileListEdit = fileListEdit
    },
    handleDesactive (index, row) {
      this.dialogDesactiveVisible = true
      this.$set(this, 'ruleForm', { ...row })
    },
    handleActivate (index, row) {
      this.dialogActivateVisible = true
      this.$set(this, 'ruleForm', { ...row })
    },
    searchByName () {
      if (this.bannerName.trim() !== '') {
        this.filteredBanners = this.banners.filter(banner => banner.name.toLowerCase().includes(this.bannerName.toLowerCase()))
      } else {
        this.filteredBanners = this.banners
      }
    },
    resetForm (formName) {
      if (this.$refs[formName]) {
        this.$refs[formName].resetFields()
      }
    },
    handleSizeChange (pageSize) {
      this.pagination.pageSize = pageSize
      this.fetchData()
    }
  },
  mounted () {
    this.fetchData()
  }
}
</script>

<style scoped>
.content {
  padding-left: 50px;
  padding-right: 50px;
}
.page-header {
  margin-left: 30px;
}
</style>
