<template>
  <div>
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Administración de Usuarios">
      </el-page-header>
    </div>
    <div class="content">
      <div>
        <el-col :sm="8" :md="6" :lg="4" :xl="2">
  <el-input
    placeholder="Email"
    v-model="email"
    clearable
    @input="debounceInput">
  </el-input>
</el-col>
<el-col :sm="8" :md="6" :lg="4" :xl="2">
  <el-select
    v-model="is_staff"
    placeholder="Administrador"
    clearable>
    <el-option label="Administrador" value="true"></el-option>
    <el-option label="No Administrador" value="false"></el-option>
  </el-select>
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
<el-col :sm="8" :md="6" :lg="4" :xl="2">
  <el-button type="primary" icon="el-icon-circle-plus" @click="dialogAddUser= true">Añadir Usuario</el-button>
</el-col>
      </div>
      <el-table ref="table" :data="users" stripe style="min-width: 100%;overflow:scroll">
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
        <el-table-column  style="min-width: 40px;" label="Administrador"  >
          <template v-slot="scope">
            <i
            :style="scope.row.is_staff === true ? ' border-radius:10px; background-color:rgb(0, 218, 0);,color: white;' : ' border-radius:10px;background-color: rgb(255, 120, 120);,color: white;'"
            :class="scope.row.is_staff === true ? 'el-icon-check' : 'el-icon-close'"></i>
          </template>
        </el-table-column>
        <el-table-column style="min-width: 600px;" label="Operaciones">
          <template v-slot="props">
            <div style="display:flex;">
              <el-button size="mini" @click="handleEdit(props.$index, props.row)"><i class="el-icon-edit"></i></el-button>
              <span v-if="props.row.is_active==true">
                <el-button size="mini" type="danger" @click="handleDelete(props.$index, props.row)"><i class="el-icon-delete"></i></el-button>
              </span>
              <span v-else >
                <el-button size="mini" type="success" @click="handleDelete(props.$index, props.row)"><i class="el-icon-refresh-left"></i></el-button>
              </span>
              <el-button size="mini" type="primary" @click="handleChangePass(props.$index, props.row)"><i class="el-icon-lock"></i></el-button>
              <el-button size="mini" type="warning" @click="handleEditDirection(props.$index, props.row)"><i class="fas fa-edit"></i></el-button>
              </div>
          </template>
        </el-table-column>
      </el-table>

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
    </div>
    <el-dialog
        :title="`Editar usuario`"
        :visible="dialogEditVisible"
        @before-close="dialogVisible = false"
        width="60%"
        :close-on-click-modal="true"
      >
       <div>
        <el-form :model="ruleForm" :rules="rulesEditUser" ref="ruleForm" label-width="120px" class="demo-ruleForm">
    <el-form-item label="Nombre:" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item label="Apellidos:" >
      <el-input v-model="ruleForm.last_name"></el-input>
    </el-form-item>
    <el-form-item label="Correo electrónico:" prop="email">
      <el-input v-model="ruleForm.email"></el-input>
    </el-form-item>
    <el-form-item label="DNI/NIE:"  prop="dni">
      <el-input v-model="ruleForm.dni"></el-input>
    </el-form-item>
    <el-form-item label="Teléfono:" prop="phone" >
      <el-input v-model="ruleForm.phone"></el-input>
    </el-form-item>
    <el-form-item label="Fecha de Nacimiento:" prop="birthdate">
      <el-col :span="11">
        <el-form-item >
          <el-date-picker type="date" placeholder="Fecha de Nacimiento" v-model="ruleForm.birthdate"
            style="width: 100%;"></el-date-picker>
        </el-form-item>
      </el-col>
    </el-form-item>
    <el-form-item label="Es Administrador">
      <el-switch v-model="ruleForm.is_staff"></el-switch>
      </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitFormEditUser('ruleForm')">Guardar</el-button>
      <el-button @click="dialogEditVisible = false,resetForm('ruleForm')">Cancelar</el-button>
    </el-form-item>
  </el-form>
       </div>
      </el-dialog>
      <el-dialog
      title="Cambiar contraseña"
      :visible="dialogChangePassVisible"
      @before-close="dialogChangePassVisible = false"
      width="40%"
      :close-on-click-modal="true"
    >
      <div>
        <el-form :model="changePasswordData" :rules="changePasswordRules" ref="changePassForm" label-width="180px" class="changePassForm">
          <el-form-item class="inputPass" label="Nueva Contraseña:">
            <el-input  :type="showPassword ? 'text' : 'password'" v-model="changePasswordData.pass" autocomplete="off">
              <template #append>
                <el-button class="buttonPass" icon="el-icon-view" @click="viePassword"></el-button>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item class="inputPass" label="Confirme la Contraseña:" >
            <el-input :type="showNewPassword ? 'text' : 'password'" v-model="changePasswordData.newPass" autocomplete="off">
              <template #append>
                <el-button class="buttonPass" icon="el-icon-view" @click="vieNewPassword"></el-button>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitChangePasswordForm('changePassForm')">Guardar</el-button>
            <el-button @click="dialogChangePassVisible = false">Cancelar</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>
      <el-dialog
        :visible="dialogdeleteVisible"
        @before-close="dialogVisible = false"
        width="40%"
        :close-on-click-modal="true"
      >
      <div v-if="this.ruleForm.is_active==true">
        <h3>¿Estas seguro de que quieres Desactivar el usuario?</h3>
      <el-button type="danger" @click="dialogdeleteVisible = false,DesactivateUser('ruleForm')">Desactivar</el-button>
      <el-button @click="dialogdeleteVisible = false,resetForm('ruleForm')">Cancelar</el-button>
      </div>
      <div v-else>
        <h3>¿Estas seguro de que quieres Activar el usuario?</h3>
      <el-button type="success" @click="dialogdeleteVisible = false,DesactivateUser('ruleForm')">Activar</el-button>
      <el-button @click="dialogdeleteVisible = false,resetForm('ruleForm')">Cancelar</el-button>
      </div>
    </el-dialog>
    <el-dialog
    :title="`Editar  dirección usuario`"
    :visible="dialogEditDirectionVisible"
    @before-close="dialogEditDirectionVisible = false"
    width="60%"
    :close-on-click-modal="true"
  >
   <div>
    <el-form :model="ruleForm" :rules="rulesEditDirection" ref="ruleForm" label-width="120px" class="demo-ruleForm">
      <el-form-item label="Provincia:" prop="province">
        <el-select v-model="ruleForm.province" placeholder="Provincia" clearable filterable @change="dirtyFilter = true">
          <el-option :value="provincia.id" :key="provincia.id" :label="provincia.name"  v-for="provincia in provincias"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Localidad:" prop="locality">
        <el-input v-model="ruleForm.locality"></el-input>
      </el-form-item>
      <el-form-item label="Dirección:" prop="direction">
        <el-input v-model="ruleForm.direction"></el-input>
      </el-form-item>
      <el-form-item label="Código Postal" prop="postal_code">
        <el-input v-model="ruleForm.postal_code"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitFormDirection('ruleForm')">Guardar</el-button>
        <el-button @click="dialogEditDirectionVisible = false">Cancelar</el-button>
      </el-form-item>
    </el-form>
   </div>
  </el-dialog>
  <el-dialog
  :title="`Añadir usuario`"
  :visible="dialogAddUser"
  @before-close="dialogAddUser = false"
  width="60%"
  :close-on-click-modal="true"
>
  <el-form :model="ruleForm" :rules="ruleSCreateUser" ref="ruleForm" label-width="120px" class="demo-ruleForm">
    <el-form-item label="Email:" prop="email">
      <el-input type="email" v-model="ruleForm.email"></el-input>
    </el-form-item>
    <el-form-item label="Nombre:" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item class="inputPass" label="Contraseña:" prop="pass">
      <el-input :type="showNewPassword ? 'text' : 'password'" v-model="ruleForm.pass" autocomplete="off">
        <template #append>
          <el-button class="buttonPass" icon="el-icon-view" @click="vieNewPassword()"></el-button>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item class="inputPass" label="Confirme la contraseña:" prop="confirmPass">
      <el-input :type="showPassword ? 'text' : 'password'" v-model="ruleForm.confirmPass" autocomplete="off">
        <template #append>
          <el-button class="buttonPass" icon="el-icon-view" @click="viewPassword()"></el-button>
        </template>
      </el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitFormCreatedUser">Crear Cuenta</el-button>
      <el-button @click="resetForm('ruleForm'),dialogAddUser = false">Cancelar</el-button>
    </el-form-item>
  </el-form>
</el-dialog>
  </div>
</template>

<script>
import router from '@/router'
import { fetchUserData, fetchChangePassword, fetchDesactiveUser, fetchUserEditDirection, fetchUserEdit, CreateUser } from '@/api/login'
import { fetchProvinces } from '@/api/province'
import moment from 'moment'

export default {
  data () {
    return {
      provincia: {},
      provincias: [],
      dialogAddUser: false,
      userDirectionData: {
        province: '',
        locality: '',
        direction: '',
        postal_code: ''
      },
      showPassword: false,
      dialogChangePassVisible: false,
      dialogEditVisible: false,
      dialogdeleteVisible: false,
      dialogEditDirectionVisible: false,
      changePasswordData: {
        pass: '',
        newPass: ''
      },
      changePasswordRules: {
        pass: [
          { required: true, message: 'Este campo es obligatorio', trigger: 'blur' }
        ],
        newPass: [
          { required: true, message: 'Este campo es obligatorio', trigger: 'blur' }
        ]
      },
      email: '',
      is_staff: '',
      is_active: '',
      users: [],
      ruleForm: {},
      showNewPassword: false,
      ruleFormCreateuser: {
        name: '',
        email: '',
        pass: '',
        confirmPass: ''
      },
      ruleSCreateUser: {
        name: [
          { required: true, message: 'Por favor debe rellenar el campo', trigger: 'blur' }
        ],
        email: [
          {
            required: true,
            message: 'Por favor, ingresa una dirección de correo electrónico',
            trigger: 'blur'
          },
          {
            type: 'email',
            message: 'Por favor,debes de indicar una dirección de correo electrónico válida',
            trigger: 'blur'
          }
        ],
        pass: [
          { required: true, message: 'Por favor debe rellenar el campo' }
        ],
        confirmPass: [
          { required: true, message: 'Por favor debe rellenar el campo' }
        ]
      },
      rulesEditDirection: {
        province: [
          { required: true, message: 'El campo es obligatorio', trigger: 'blur' }
        ],
        locality: [
          { required: true, message: 'El campo es obligatorio', trigger: 'blur' }
        ],
        direction: [
          { required: true, message: 'El campo es obligatorio', trigger: 'blur' }
        ],
        postal_code: [
          { required: true, message: 'El campo es obligatorio', trigger: 'blur' },
          { pattern: /^[0-9]{5}$/, message: 'Por favor, introduce un código postal válido', trigger: 'blur' }
        ]
      },
      rulesEditUser: {
        name: [
          { required: true, message: 'El campo de nombre es obligatorio', trigger: 'blur' }
        ],
        email: [
          {
            required: true,
            message: 'Por favor, ingresa una dirección de correo electrónico',
            trigger: 'blur'
          },
          {
            type: 'email',
            message: 'Por favor,debes de indicar una dirección de correo electrónico válida',
            trigger: 'blur'
          }
        ],
        birthdate: [
          { required: true, message: 'Por favor, se debe de indicar una fecha', trigger: 'change' }
        ],
        dni: [
          { required: true, message: 'El campo del DNI es obligatorio', trigger: 'blur' },
          { pattern: /^[XYZ]?\d{5,8}[A-Z]$/, message: 'Formato del DNI inválido', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: 'El campo de teléfono es obligatorio', trigger: 'blur' },
          { pattern: /^\d{9}$/, message: 'El teléfono debe tener 9 dígitos', trigger: 'blur' }
        ]
      },
      columns: [
        {
          prop: 'id',
          label: 'ID',
          minWidth: '20px',
          sortable: true,
          formatter: (row) => row.id
        },
        {
          prop: 'name',
          label: 'Nombre',
          minWidth: '60px',
          sortable: true,
          formatter: (row) => `${row.name} ${row.last_name || ''}`
        },
        {
          prop: 'email',
          label: 'Email',
          minWidth: '90px',
          sortable: true,
          formatter: (row) => row.email || ''
        },
        {
          prop: 'create_at',
          label: 'Creado',
          minWidth: '60px',
          sortable: true,
          formatter: (row) => moment(row.create_at).format('DD/MM/YYYY HH:mm') || ''
        },
        {
          prop: 'phone',
          label: 'Teléfono',
          minWidth: '50px',
          sortable: true,
          formatter: (row) => row.phone || ''
        },
        {
          prop: 'dni',
          label: 'DNI',
          minWidth: '60px',
          sortable: true,
          formatter: (row) => row.dni || ''
        }
      ],
      pagination: {
        page: 1,
        total: 0,
        pageSizes: [25, 50, 100],
        pageSize: 25
      }
    }
  },
  methods: {
    async submitFormCreatedUser () {
      this.$refs.ruleForm.validate(async valid => {
        if (valid) {
          if (this.ruleForm.pass !== this.ruleForm.confirmPass) {
            this.$notify.error({
              title: 'Error',
              message: 'Las contraseñas no coinciden'
            })
            return
          }
          try {
            const post = {
              email: this.ruleForm.email,
              name: this.ruleForm.name,
              password: this.ruleForm.pass
            }
            const response = await CreateUser(post)
            if (response && response.password) {
              this.$notify({
                title: 'Success',
                message: 'Usuario creado con éxito',
                type: 'success'
              })
              this.dialogAddUser = false
              this.fetchData()
            }
          } catch (error) {
            if (error.response && error.response.data.password) {
              this.$notify.error({
                title: 'Error',
                message: error.response.data.password[0]
              })
            } else if (error.response && error.response.data.email) {
              this.$notify.error({
                title: 'Error',
                message: error.response.data.email[0]
              })
            } else {
              this.$notify.error({
                title: 'Error',
                message: 'Ocurrió un error inesperado'
              })
            }
          }
        } else {
          this.$message.error('Por favor, completa correctamente el formulario.')
        }
      })
    },
    submitFormEditUser (form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          fetchUserEdit(this.ruleForm)
            .then(() => {
              this.$message.success('Cambios guardados correctamente')
              this.fetchData()
              this.dialogEditVisible = false
              this.loading = false
            })
            .catch(() => {
              this.$message.error('Error al guardar los cambios. Por favor, inténtalo de nuevo.')
            })
        } else {
          this.$message.error('Por favor, completa correctamente el formulario.')
          return false
        }
      })
    },
    resetForm (form) {
      this.$refs[form].resetFields()
    },
    submitFormDirection (form, userId = null) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          userId = this.ruleForm.id
          fetchUserEditDirection(this.ruleForm, userId)
            .then(() => {
              this.$message.success('Cambios guardados correctamente')
              this.dialogEditDirectionVisible = false
              this.fetchData()
              this.loading = false
            })
            .catch(() => {
              this.$message.error('Error al guardar los cambios. Por favor, inténtalo de nuevo.')
            })
        } else {
          this.$message.error('Por favor, completa correctamente el formulario.')
          return false
        }
      })
    },
    DesactivateUser () {
      const userId = this.ruleForm.id
      fetchDesactiveUser(userId)
        .then(() => {
          this.$message.success('Usuario desactivado correctamente')
        })
        .catch((error) => {
          console.error('Error al desactivar el usuario:', error)
          this.$message.error('Error al desactivar el usuario. Por favor, inténtalo de nuevo.')
        }).finally(() => {
          this.fetchData()
          this.loading = false
        })
    },
    submitChangePasswordForm (form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          if (this.changePasswordData.pass !== this.changePasswordData.newPass) {
            this.$message.error('Error las contraseñas no son coinciden')
            return
          }
          const data = {
            password: this.changePasswordData.pass,
            newPassword: this.changePasswordData.newPass
          }
          const userId = this.ruleForm.id || null
          fetchChangePassword(userId, data)
            .then(() => {
              this.$message.success('Contraseña cambiada correctamente')
              this.dialogChangePassVisible = false
            })
            .catch(() => {
              this.$message.error('Error al cambiar la contraseña. Por favor, inténtalo de nuevo.')
            }).finally(() => {
              this.fetchData()
              this.loading = false
            })
        } else {
          this.$message.error('Por favor, completa correctamente el formulario.')
        }
      })
    },
    fetchDataProvinces () {
      fetchProvinces()
        .then((response) => {
          this.provincias = response.data
        })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
        })
    },
    viePassword () {
      this.showPassword = !this.showPassword
    },
    ChangePassword () {
      this.dialogChangePassVisible = true
    },
    handleSizeChange (pageSize) {
      this.pagination.pageSize = pageSize
      this.fetchData()
    },
    handleCurrentChange (page) {
      this.pagination.page = page
      this.fetchData(page)
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
        this.searchByEmail()
      }, 500)
    },
    fetchData () {
      fetchUserData({
        page: this.pagination.page,
        pageSize: this.pagination.pageSize,
        email: this.email.trim(),
        is_staff: this.is_staff,
        is_active: this.is_active
      })
        .then((response) => {
          const users = response.data.results
          this.$set(this, 'users', users)
          this.pagination.total = response.data.count
        })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
        })
    },
    handleEdit (index, row) {
      this.dialogEditVisible = true
      this.$set(this, 'ruleForm', { ...row })
    },
    handleEditDirection (index, row) {
      this.dialogEditDirectionVisible = true
      this.fetchDataProvinces()
      this.$set(this, 'ruleForm', { ...row })
    },
    handleDelete (index, row) {
      this.dialogdeleteVisible = true
      this.$set(this, 'ruleForm', { ...row })
    },
    handleChangePass (index, row) {
      this.dialogChangePassVisible = true
      this.$set(this, 'ruleForm', { ...row })
    },
    searchByEmail () {
      if (this.email.trim() !== '') {
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
    viewPassword () {
      if (this.showPassword === false) {
        this.showPassword = true
      } else {
        this.showPassword = false
      }
    }
  },
  mounted () {
    this.fetchData()
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
.operation-buttons {
  display: flex;
  overflow-x: scroll;
}
.operation-buttons .el-button {
  margin-right: 5px;
  flex-shrink: 0;
  white-space: nowrap;
}
</style>
