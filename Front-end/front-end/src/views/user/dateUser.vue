<template>
  <div class="content">
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Mis Datos">
      </el-page-header>
    </div>
    <h1>Mis Datos Personales</h1>
    <el-button @click="ChangePassword">Cambiar Contraseña</el-button>
    <el-divider></el-divider>
    <el-form :model="userData" :rules="rul" ref="userForm" label-width="120px" class="ruleForm">
      <el-form-item>
        <el-upload
          :action="`http://127.0.0.1:8000/api/users/${id}/avatar/`"
          enctype="multipart/form-data"
          method="post"
          class="upload-demo"
          :show-file-list="false"
          :before-upload="handleBeforeUpload"
          :on-success="handleAvatarSuccess"
          :headers="{ Authorization: 'Bearer ' + this.token }"
        >
          <img v-if="imageUrl" :src="imageUrl" class="avatar" style="border-radius:50%">
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
      </el-form-item>
      <el-form-item label="Nombre:" prop="name">
        <el-input v-model="userData.name"></el-input>
      </el-form-item>
      <el-form-item label="Apellidos:" prop="last_name">
        <el-input v-model="userData.last_name"></el-input>
      </el-form-item>
      <el-form-item label="DNI:" prop="dni">
        <el-input v-model="userData.dni"></el-input>
      </el-form-item>
      <el-form-item label="Teléfono:" prop="phone">
        <el-input v-model="userData.phone"></el-input>
      </el-form-item>
      <el-form-item label="Correo electrónico:" prop="email">
        <el-input v-model="userData.email"></el-input>
      </el-form-item>
      <el-form-item label="Fecha de Nacimiento:" required>
        <el-col :span="11">
          <el-form-item prop="birthdate">
            <el-date-picker type="date" placeholder="Fecha de Nacimiento" v-model="userData.birthdate"   style="width: 100%;"></el-date-picker>
          </el-form-item>
        </el-col>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('userForm')">Guardar</el-button>
        <el-button @click="fetchData">Cancelar</el-button>
      </el-form-item>
    </el-form>
    <el-dialog
      title="Cambiar contraseña"
      :visible="dialogChangePassVisible"
      @before-close="dialogChangePassVisible = false"
      width="40%"
      :close-on-click-modal="true"
    >
      <div>
        <el-form :model="changePasswordData" :rules="changePasswordRules" ref="changePassForm" label-width="180px" class="changePassForm">
          <el-form-item class="inputPass" label="Nueva Contraseña:" prop="pass">
            <el-input  :type="showPassword ? 'text' : 'password'" v-model="changePasswordData.pass" autocomplete="off">
              <template #append>
                <el-button class="buttonPass" icon="el-icon-view" @click="viePassword"></el-button>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item class="inputPass" label="Confirme la Contraseña:" prop="newPass">
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
    title="Eliminar Cuenta"
    :visible="dialogdeleteVisible"
    @before-close="dialogdeleteVisible = false"
    width="40%"
    :close-on-click-modal="true"
  >
    <div>
      <h3>¿Estás seguro de que quieres eliminar tu cuenta?</h3>
      <h4>Esta acción será irreversible</h4>
      <el-button type="danger" @click="DesactivateUser(),dialogdeleteVisible = false">Eliminar</el-button>
      <el-button @click="dialogdeleteVisible = false">Cancelar</el-button>
    </div>
  </el-dialog>
  <el-button class="deleteUser" type="danger" @click="deleteUser()">Eliminar Cuenta</el-button>
</div>
</template>

<script>
import router from '@/router'
import { fetchDateUserData, fetchUserEdit, fetchChangePassword, fetchDesactiveUser } from '@/api/login'
import { jwtDecode } from 'jwt-decode'

export default {
  name: 'dateUserWhile',
  data () {
    return {
      id: '',
      showNewPassword: false,
      showPassword: false,
      dialogdeleteVisible: false,
      dialogChangePassVisible: false,
      token: localStorage.getItem('color') ? localStorage.getItem('color') : '',
      imageUrl: '',
      userData: {
        avatar: '',
        name: '',
        last_name: '',
        email: '',
        dni: '',
        phone: '',
        birthdate: ''
      },
      rul: {
        avatar: [
          { required: true, message: 'Por favor, selecciona una imagen', trigger: 'change' }
        ],
        name: [
          { required: true, message: 'El campo de nombre es obligatorio', trigger: 'blur' }
        ],
        birthdate: [
          { required: true, message: 'Por favor, se debe de indicar una fecha', trigger: 'change' }
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
        dni: [
          { required: true, message: 'El campo del DNI es obligatorio', trigger: 'blur' },
          { pattern: /^[XYZ]?\d{5,8}[A-Z]$/, message: 'Formato del DNI inválido', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: 'El campo de teléfono es obligatorio', trigger: 'blur' },
          { pattern: /^\d{9}$/, message: 'El teléfono debe tener 9 dígitos', trigger: 'blur' }
        ]
      },
      changePasswordData: {
        pass: '',
        newPass: ''
      },
      changePasswordRules: {
        pass: [
          { required: true, message: 'Este campo es obligatorio', trigger: 'blur' },
          { min: 8, message: 'La contraseña debe tener al menos 8 caracteres', trigger: 'blur' },
          { pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/, message: 'La contraseña debe contener al menos una letra mayúscula , minúscula y un número', trigger: 'blur' }
        ],
        newPass: [
          { required: true, message: 'Este campo es obligatorio', trigger: 'blur' },
          { min: 8, message: 'La contraseña debe tener al menos 8 caracteres', trigger: 'blur' },
          { pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/, message: 'La contraseña debe contener al menos una letra mayúscula , minúscula y un número', trigger: 'blur' }
        ]
      }
    }
  },
  mounted () {
    this.fetchData()
    if (localStorage.getItem('color')) {
      const decodedToken = jwtDecode(localStorage.getItem('color'))
      this.id = decodedToken.id
    }
    if (localStorage.getItem('color')) {
      this.token = localStorage.getItem('color')
    }
  },
  methods: {
    ChangePassword () {
      this.dialogChangePassVisible = true
    },
    deleteUser () {
      this.dialogdeleteVisible = true
    },
    DesactivateUser () {
      fetchDesactiveUser(this.userData.id).then(() => {
        this.$message.success('Usuario desactivado correctamente')
        setTimeout(() => {
          this.logout()
        }, 1000)
      }).catch((error) => {
        console.error('Error al desactivar el usuario:', error)
        this.$message.error('Error al desactivar el usuario. Por favor, inténtalo de nuevo.')
      })
    },
    submitChangePasswordForm (form) {
      if (this.changePasswordData.pass !== this.changePasswordData.newPass) {
        this.$notify.error({
          title: 'Error',
          message: 'Las contraseñas no coinciden'
        })
        return false
      }
      this.$refs[form].validate(valid => {
        if (valid) {
          const data = {
            password: this.changePasswordData.pass,
            newPassword: this.changePasswordData.newPass
          }
          const userId = this.userData.id || null
          fetchChangePassword(userId, data)
            .then(() => {
              this.$message.success('Contraseña cambiada correctamente')
              this.dialogChangePassVisible = false
            })
            .catch(() => {
              this.$message.error('Error al cambiar la contraseña. Por favor, inténtalo de nuevo.')
            })
        } else {
          this.$message.error('Por favor, completa correctamente el formulario.')
        }
      })
    },
    handleAvatarSuccess (res, file) {
      this.imageUrl = URL.createObjectURL(file.raw)
    },
    fetchData () {
      fetchDateUserData()
        .then((response) => {
          this.userData = response.data
          this.imageUrl = 'data:image/jpeg;base64,' + this.userData.avatar
        })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
        })
    },
    goBack () {
      router.push('/user')
    },
    submitForm (form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          fetchUserEdit(this.userData)
            .then(() => {
              this.$message.success('Cambios guardados correctamente')
              this.fetchData()
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
    viePassword () {
      this.showPassword = !this.showPassword
    },
    vieNewPassword () {
      this.showNewPassword = !this.showNewPassword
    },
    handleBeforeUpload (file) {
      const isJPG = file.type === 'image/jpeg'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        this.$message.error('La imagen debe estar en formato JPG!')
      }
      if (!isLt2M) {
        this.$message.error('La imagen debe tener un tamaño menor a 2MB!')
      }
      return isJPG && isLt2M
    },
    logout () {
      localStorage.clear()
      router.push('/')
      window.location.reload()
    }
  }
}
</script>

<style >
avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
.content {
  margin-top: 2px;
  padding-left: 200px;
  padding-right: 200px;
  margin-bottom: 200px;

}
.buttonPass{
  background-color: white !important;

  border-left:none !important;
}
.inputPass{
  border-right:none !important;
}

.deleteUser {
  display: inline-block;
  margin-bottom: 10px;
  margin-left: 90%;
}
</style>
