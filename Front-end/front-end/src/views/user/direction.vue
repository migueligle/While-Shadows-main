<template>
  <div class="content">
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Mi Dirección">
      </el-page-header>
    </div>
    <h1>Mi Dirección</h1>
    <el-divider></el-divider>
    <el-form :model="userDirectionData" :rules="rulesDirection" ref="ruleForm" label-width="120px" class="demo-ruleForm">
      <el-form-item label="Provincia:" prop="province">
        <el-select v-model="userDirectionData.province" placeholder="Provincia" clearable filterable @change="dirtyFilter = true">
          <el-option :value="provincia.id" :key="provincia.id" :label="provincia.name"  v-for="provincia in provincias"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Localidad:" prop="locality">
        <el-input v-model="userDirectionData.locality"></el-input>
      </el-form-item>
      <el-form-item label="Dirección:" prop="direction">
        <el-input v-model="userDirectionData.direction"></el-input>
      </el-form-item>
      <el-form-item label="Código Postal" prop="postal_code">
        <el-input v-model="userDirectionData.postal_code"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('ruleForm')">Guardar</el-button>
        <el-button @click="resetForm('ruleForm')">Cancelar</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import router from '@/router'
import { fetchUserEditDirection, fetchDateUserAddress } from '@/api/login'
import { fetchProvinces } from '@/api/province'
import { jwtDecode } from 'jwt-decode'

export default {
  name: 'directionWhile',
  data () {
    return {
      provincia: {},
      id: null,
      provincias: [],
      showNewPassword: false,
      showPassword: false,
      imageUrl: '',
      userDirectionData: {
        province: '',
        locality: '',
        direction: '',
        postal_code: ''
      },
      rulesDirection: {
        postal_code: [
          { required: true, message: 'El código postal es obligatorio', trigger: 'blur' },
          { max: 5, message: 'El código postal debe tener un máximo de 5 caracteres', trigger: 'blur' },
          { pattern: /^\d{5}$/, message: 'El código postal debe ser numérico y tener 5 dígitos', trigger: 'blur' }
        ],
        locality: [{ required: true, message: 'Por favor rellena este campo', trigger: 'blur' }],
        province: [{ required: true, message: 'Por favor rellena este campo', trigger: 'blur' }],
        direction: [{ required: true, message: 'Por favor rellena este campo', trigger: 'blur' }]
      }
    }
  },
  mounted () {
    this.fetchData()
    this.fetchDataUserDirection2()
    if (localStorage.getItem('color')) {
      const decodedToken = jwtDecode(localStorage.getItem('color'))
      this.id = decodedToken.id
    }
    if (localStorage.getItem('color')) {
      this.token = localStorage.getItem('color')
    }
  },
  methods: {
    submitForm (form) {
      this.$refs[form].validate((valid) => {
        if (valid) {
          fetchUserEditDirection(this.userDirectionData)
            .then(() => {
              this.$message.success('Cambios guardados correctamente')
            })
            .catch(() => {
              this.$message.error('Error al guardar los cambios')
            })
        } else {
          this.$message.error('Por favor, completa correctamente el formulario.')
          return false
        }
      })
    },
    fetchData () {
      fetchProvinces()
        .then((response) => {
          this.provincias = response.data
        })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
        })
    },
    fetchDataUserDirection2 () {
      fetchDateUserAddress().then((response) => {
        this.userDirectionData = response.data
      })
        .catch((error) => {
          console.error('Error al recuperar datos', error)
        })
    },
    goBack () {
      router.push('/user')
    },
    resetForm (form) {
      this.$refs[form].resetFields()
    },
    viePassword () {
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
    },
    handleAvatarSuccess (res, file) {
      this.imageUrl = URL.createObjectURL(file.raw)
    },
    beforeAvatarUpload (file) {
      const isJPG = file.type === 'image/jpeg'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        this.$message.error('La imagen debe estar en formato JPG!')
      }
      if (!isLt2M) {
        this.$message.error('La imagen excede los 2MB!')
      }
      return isJPG && isLt2M
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

.buttonPass {
  background-color: white !important;

  border-left: none !important;
}

.inputPass {
  border-right: none !important;
}
</style>
