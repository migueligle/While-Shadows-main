<template>
  <div>
    <div class="content">
      <div>
  <el-col :sm="8" :md="6" :lg="4" :xl="2">
  <el-input
    placeholder="Nombre"
    v-model="name"
    clearable
    @input="debounceInput">
  </el-input>
</el-col>
<el-col :sm="8" :md="6" :lg="4" :xl="2">
  <el-select
    v-model="is_active"
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
  <el-button type="primary" icon="el-icon-circle-plus" @click="dialogCreateVisible= true">Añadir Marca</el-button>
</el-col>
      </div>
      <el-table ref="table" :data="marks" stripe style="width: 100%">
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
            :style="scope.row.is_active === true ? ' border-radius:10px; background-color:rgb(0, 218, 0);,color: white;' : ' border-radius:10px;background-color: rgb(255, 120, 120);,color: white;'"
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
            <el-button size="mini" type="danger" @click="DesactivateMark(props.$index, props.row)"><i class="el-icon-delete"></i></el-button>
          </span>
          <span v-else >
            <el-button size="mini" type="success" @click="DesactivateMark(props.$index, props.row)"><i class="el-icon-refresh-left"></i></el-button>
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
        :title="`Editar marca`"
        :visible="dialogEditVisible"
        @before-close="dialogEditVisible = false"
        width="40%"
        :close-on-click-modal="true"
      >
       <div>
        <el-form :model="FromEditMark" :rules="rules" ref="FromEditMark" label-width="120px" class="demo-ruleForm">
    <el-form-item label="Nombre:" prop="name">
      <el-input v-model="FromEditMark.name"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitEditMark('FromEditMark')">Guardar</el-button>
      <el-button @click="dialogEditVisible = false,resetForm('FromEditMark')">Cancelar</el-button>
    </el-form-item>
  </el-form>
       </div>
      </el-dialog>
    <el-dialog
        :title="`Crear marca`"
        :visible="dialogCreateVisible"
        @before-close="dialogCreateVisible = false"
        width="40%"
        :close-on-click-modal="true"
      >
       <div>
        <el-form :model="FromCreateMark" :rules="rules" ref="FromCreateMark" label-width="120px" class="demo-ruleForm">
    <el-form-item label="Nombre:" prop="name">
      <el-input v-model="FromCreateMark.name"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitCreateMark('FromCreateMark')">Guardar</el-button>
      <el-button @click="dialogCreateVisible = false,resetForm('FromCreateMark')">Cancelar</el-button>
    </el-form-item>
  </el-form>
       </div>
      </el-dialog>
  </div>
</template>
<script>
import router from '@/router'
import { fetchMarks, fetchCreateMark, fetchEditMark, fetchDesactiveMark } from '@/api/marks.js'

export default {
  name: 'maker-Show',
  data () {
    return {
      dialogDesactiveVisible: false,
      dialogEditVisible: false,
      dialogCreateVisible: false,
      dialogdeleteVisible: false,
      FromCreateMark: {},
      FromEditMark: {},
      name: '',
      is_active: '',
      marks: [],
      id: '',
      showNewPassword: false,
      ruleForm: {},
      rules: {
        name: [
          { required: true, message: 'El campo de nombre es obligatorio', trigger: 'blur' }
        ]
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
      }
    }
  },
  methods: {
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    submitEditMark (form) {
      if (this.$refs[form]) {
        this.$refs[form].validate(valid => {
          if (valid) {
            fetchEditMark(this.FromEditMark)
              .then(() => {
                this.$message.success('Marca actualizada correctamente')
                this.dialogCreateVisible = false
              })
              .catch(() => {
                this.$message.error('Error al actualizar la marca')
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
    submitCreateMark (form) {
      if (this.$refs[form]) {
        this.$refs[form].validate(valid => {
          if (valid) {
            fetchCreateMark(this.FromCreateMark)
              .then(() => {
                this.$message.success('Marca añadida correctamente')
                this.dialogCreateVisible = false
              })
              .catch(() => {
                this.$message.error('Error al crear la marca')
              })
              .finally(() => {
                this.fetchData()
                this.loading = false
              })
          } else {
            this.$message.error('Por favor, completa correctamente el formulario.')
          }
        })
        console.error('Referencia al formulario no encontrada:', form)
      }
    },
    DesactivateMark (index, row) {
      const markId = row.id
      fetchDesactiveMark(markId)
        .then((response) => {
          const message = response.data.message
          this.$message.success(message)
        })
        .catch((error) => {
          console.error('Error al desactivar la marca:', error)
          this.$message.error('Error al desactivar a marca. Por favor, inténtalo de nuevo.')
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
    fetchData (page) {
      this.loading = true
      const params = {
        page: page || this.pagination.page,
        page_size: this.pagination.pageSize
      }
      if (this.name != null && this.name !== '') {
        params.name = this.name
      }
      if (this.is_active != null && this.is_active !== '') {
        params.is_active = this.is_active
      }
      fetchMarks(params)
        .then((response) => {
          this.marks = response.data.results
          this.pagination.total = response.data.count
          this.loading = false
        })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
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
      this.$set(this, 'FromEditMark', { ...row })
    },
    handleDelete (index, row) {
      this.dialogdeleteVisible = true
      this.$set(this, 'ruleForm', { ...row })
    },
    searchByName () {
      if (this.name.trim() !== '') {
        this.fetchData()
      }
    }
  },
  mounted () {
    this.fetchData()
  }
}
</script>

<style scoped>

</style>
