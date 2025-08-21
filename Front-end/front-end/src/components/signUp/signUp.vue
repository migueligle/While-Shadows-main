<template>
  <div class="content">
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Crear Cuenta">
      </el-page-header>
    </div><br><br><br><br>
    <el-divider></el-divider>
    <h1>Crea Tu Cuenta</h1>
    <h3>Rellena este formulario para darte de alta</h3>
    <el-card class="card">

      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
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
          <el-button type="primary" @click="submitForm">Crear Cuenta</el-button>
          <el-button @click="resetForm('ruleForm')">Cancelar</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { CreateUser } from '@/api/login.js'
import router from '@/router'
export default {
  name: 'SingUpView',
  data      () {
    return {
      name: '',
      showNewPassword: false,
      showPassword: false,
      confirmPass: '',
      ruleForm: {
        name: '',
        email: '',
        pass: '',
        confirmPass: ''
      },
      rules: {
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
          { required: true, message: 'Este campo es obligatorio', trigger: 'blur' },
          { min: 8, message: 'La contraseña debe tener al menos 8 caracteres', trigger: 'blur' },
          { pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/, message: 'La contraseña debe contener al menos una letra mayúscula , minúscula y un número', trigger: 'blur' }
        ],
        confirmPass: [
          { required: true, message: 'Este campo es obligatorio', trigger: 'blur' },
          { min: 8, message: 'La contraseña debe tener al menos 8 caracteres', trigger: 'blur' },
          { pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/, message: 'La contraseña debe contener al menos una letra mayúscula , minúscula y un número', trigger: 'blur' }
        ]
      }

    }
  },
  methods: {
    async submitForm () {
      if (this.ruleForm.pass !== this.ruleForm.confirmPass) {
        this.$notify.error({
          title: 'Error',
          message: 'Las contraseñas no coinciden'
        })
        return false
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
          router.push('/')
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
    },
    goBack () {
      router.push('/')
    },
    viewPassword () {
      if (this.showPassword === false) {
        this.showPassword = true
      } else {
        this.showPassword = false
      }
    },
    vieNewPassword () {
      if (this.showNewPassword === false) {
        this.showNewPassword = true
      } else {
        this.showNewPassword = false
      }
    }
  }
}
</script>

<style scoped>
.content {
  margin-top: 2px;
  padding-left: 100px;
  padding-right: 100px;
  margin-bottom: 200px;
}

.card {
  width: 50%;
  border-radius: 15px;
  text-align: center;
  padding: 20px;
  margin: auto;
}
</style>
