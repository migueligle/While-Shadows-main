<template>
  <div class="content">
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Recuperar contraseña">
      </el-page-header>
    </div>
    <h1>Recuperar Contraseña</h1>
    <el-divider></el-divider>
    <div v-if="send == null">
      <el-card class="card">
        <h3>Ingresa el correo electrónico que utilizaste al registrarte para recuperar tu cuenta</h3>
        <el-divider></el-divider>
        <el-form ref="ruleForm" :model="formData" :rules="rules" label-width="120px" class="demo-ruleForm">
          <el-form-item label="Email" prop="email">
            <el-input v-model="formData.email"></el-input>
          </el-form-item>
          <el-form-item style="text-align: center;">
            <el-button style="margin-right:10%" type="primary" @click="submitForm('ruleForm')">Recuperar Cuenta</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    <div v-else>
      <el-card class="card">
        <el-result :icon="resultIcon" :title="resultTitle" :sub-title="resultSubtitle"></el-result>
        <el-button v-if="result == false && send != null" style="margin-top: 12px;" @click="goEmail"><i
          class="el-icon-back"></i> Atrás </el-button>
        <el-button v-if="result !== null && send==true " type="primary" style="margin-top: 12px;" @click="next">Volver a Inicio <i
            class="el-icon-right"></i></el-button>
      </el-card>
    </div>
  </div>
</template>

<script>
import router from '@/router'
import { fetchrecoverAccount } from '@/api/login.js'

export default {
  name: 'RecoverPasswordView',
  data () {
    return {
      send: null,
      result: null,
      formData: {
        email: ''
      },
      rules: {
        email: [
          { required: true, message: 'El correo electrónico es requerido', trigger: 'blur' },
          { type: 'email', message: 'Ingrese un correo electrónico válido', trigger: ['blur', 'change'] }
        ]
      }
    }
  },
  computed: {
    resultIcon () {
      return this.result === true ? 'success' : 'error'
    },
    resultTitle () {
      return this.result === true ? 'Correo electrónico enviado' : 'Ha ocurrido algún error'
    },
    resultSubtitle () {
      return this.result === true ? 'Por favor, dirígete a tu correo para obtener tu nueva contraseña' : ''
    }
  },
  methods: {
    goEmail () {
      this.send = null
    },
    goBack () {
      router.push('/')
    },
    async submitForm (formName) {
      if (!this.formData.email) {
        this.$message.error('El campo de correo electrónico no puede estar vacío')
        return
      }
      try {
        await this.$refs[formName].validate()
        await fetchrecoverAccount({ email: this.formData.email })
        this.result = true
        this.send = true
      } catch (error) {
        console.error('Error:', error)
        this.result = false
        this.send = true
      }
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
      this.result = null
      this.send = false
    },
    next () {
      router.push('/')
    }
  }
}
</script>

<style scoped>
.content {
  margin-top: 200px;
  padding-left: 100px;
  padding-right: 100px;
  margin-bottom: 220px;
}

.card {
  width: 60%;
  border-radius: 15px;
  text-align: center;
  padding: 20px;
  margin: auto;
}
</style>
