<template>
  <div class="content">
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Contacto">
      </el-page-header>
    </div>
    <h2>Quienes somos</h2>
    <el-divider></el-divider>
    <div>
      <h4>While Shadows es una empresa  especializada en la venta de productos para DJ y Producción musical.
        Nuestro principal objetivo es dar una atención excelente y hacer felices a nuestros clientes.
        El trato personalizado es la clave de nuestro éxito, no queremos venderte, queremos asesorarte, para que compres el equipo que mejor se adapte a tus necesidades.
        Todo nuestro equipo esta formado por DJS y Productores de música electrónica, los cuales te podrán asesorar de manera personal y profesional.
        No dudes en contactar con nosotros!
        Te ayudaremos a tomar la decisión correcta! </h4>
    </div>
    <h2>Ubicación</h2>
    <el-divider></el-divider>
    <div class="wrapper">
      <div class="description">
        <pre style="font-family: system-ui;"><b>
          Nos ubicamos en:
          Urb Virgen del milagro,21
          30190 villamuriel de cerrato(Palencia)
          España
        </b></pre>
      </div>
      <div class="map-container">
        <MapVue/>
      </div>
    </div>
  <el-divider></el-divider>
  <h2>Formulario de contacto</h2>
  <div class="card_form">
    <el-card>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
        <el-form-item label="Nombre:" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
            </el-form-item>
          <el-form-item label="Email:" prop="email">
            <el-input v-model="ruleForm.email"></el-input>
          </el-form-item>
          <el-form-item label="Teléfono:" prop="phone">
            <el-input v-model="ruleForm.phone"></el-input>
          </el-form-item>
          <el-form-item label="Asunto:" prop="subject">
            <el-input type="textarea" v-model="ruleForm.subject"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')">Enviar <i class="el-icon-s-promotion"></i></el-button>
            <el-button @click="resetForm('ruleForm')">Cancelar</el-button>
          </el-form-item>
        </el-form>
    </el-card>
  </div>
  <el-divider></el-divider>
  <p>También, pueden llamarnos a atención al cliente, de lunes a viernes ,de 10:00 hasta 20:30, al siguiente teléfono:</p>
  <i class="el-icon-phone"> +34 603 133 177</i>

  </div>
</template>

<script>
import MapVue from '../../components/map.vue'
import { ContactToAdmin } from '@/api/login.js'
import router from '@/router'
export default {
  name: 'ContactIndex',
  components: {
    MapVue
  },
  data () {
    return {
      ruleForm: {},
      rules: {
        name: [
          { required: true, message: 'El nombre es requerido', trigger: 'blur' }
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
        phone: [
          { required: true, message: 'El campo de teléfono es requerido', trigger: 'blur' },
          { pattern: /^\d+$/, message: 'El campo de teléfono solo puede contener números', trigger: 'blur' }
        ],
        subject: [
          { required: true, message: 'Este campo es requerido', trigger: 'blur' }
        ]
      }

    }
  },
  methods: {
    async submitForm () {
      try {
        this.$refs.ruleForm.validate(async (valid) => {
          if (valid) {
            try {
              const response = await ContactToAdmin(this.ruleForm)
              if (response) {
                this.$notify({
                  title: 'Enviado',
                  message: 'Correo electrónico enviado con éxito',
                  type: 'success'
                })
                this.$refs.ruleForm.resetFields()
              }
            } catch (error) {
              this.$notify.error({
                title: 'Error',
                message: 'Ocurrió un error inesperado'
              })
            }
          } else {
            this.$notify.error({
              title: 'Error',
              message: 'Por favor, completa el formulario'
            })
          }
        })
      } catch (error) {
        this.$notify.error({
          title: 'Error inesperado',
          message: 'Ocurrió un error inesperado'
        })
      }
    },
    goBack () {
      router.push('/')
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
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

.wrapper {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
}

.description {
  flex: 1;
  margin-right: 10px;
  margin-top: 10%
}

.map-container {
  flex: 1;
}
</style>
