<template>
  <div class="content">
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Proceso de Compra">
      </el-page-header>
    </div>
    <el-divider></el-divider>
    <div v-loading="loading">
      <el-steps :active="active" finish-status="success" align-center>
        <el-step title="Paso 1" description="Actualiza o añade tu dirección" icon="el-icon-edit"></el-step>
        <el-step title="Paso 2" description="Añade tu medio de pago" icon="el-icon-bank-card"></el-step>
        <el-step title="Paso 3" description="Finaliza tu compra" icon="el-icon-sell"></el-step>
      </el-steps>
      <div v-if="active == 0">
        <el-card>
          <el-form :model="userDirectionData" :rules="rulesDirection" ref="ruleFormDirection" label-width="120px" class="demo-ruleForm">
            <el-form-item label="Provincia:" prop="province">
              <el-select v-model="userDirectionData.province" placeholder="Provincia" clareable filterable
                @change="dirtyFilter = true">
                <el-option :name="provincia.id" :key="provincia.id" :label="provincia.name" :value="provincia.id"
                  v-for="provincia in provincias"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="Dirección:" prop="direction">
              <el-input v-model="userDirectionData.direction"></el-input>
            </el-form-item>
            <el-form-item label="Localidad" prop="locality">
              <el-input v-model="userDirectionData.locality"></el-input>
            </el-form-item>
            <el-form-item label="Código Postal" prop="postal_code">
              <el-input v-model="userDirectionData.postal_code"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary"  plain style="margin-top: 12px;" @click="submitFormDirection('ruleFormDirection')">Guardar y siguiente <i class="el-icon-right"></i></el-button>
            </el-form-item>
          </el-form>

        </el-card>
      </div>
      <div v-if="active == 1">
        <el-card  class="tarjeta">
          <h2>Añade tu medio de pago</h2>
          <el-divider></el-divider>
          <div class="stripe-element-card-container">
            <StripeElementCard
              ref="elementRef"
              :pk="publishableKey"
              :hidePostalCode="false"
              options="cardOptions"
              @change="updateCardData($event)"
              @token="tokenCreated"
              class="stripe-element-card"
              />
            <el-button type="primary" @click="submit" class="pay-button">Pagar</el-button>
          </div>
        </el-card>
      </div>
      <div v-if="active == 2">
        <el-result v-if="paymentStatus===true" icon="success" title="Pedido confirmado" subTitle="Por favor siga las instrucciones">
        </el-result>
        <el-result v-if="paymentStatus===false" icon="error" title="Ha ocurrido algún error" subTitle="Por favor siga las instrucciones">
        </el-result>
        <el-button type="primary"  style="margin-top: 12px;" @click="next"  >Siguiente  <i class="el-icon-right"></i></el-button>
      </div>
    </div>
    <div v-if="active == 3">
    <el-button   type="success" style="margin-top: 12px;" @click="goBackIndex"  icon="el-icon-goods" > Ver Pedido </el-button>
    </div>
  </div>
</template>
<script>
import router from '@/router'
import { fetchUserEditDirection, fetchDateUserAddress } from '@/api/login'
import { fetchProvinces } from '@/api/province'
import { StripeElementCard } from '@vue-stripe/vue-stripe'
import { fetchPaymentProcess } from '@/api/payments.js'
import { fetchShoppingCart } from '@/api/shoppingCart.js'
import { fetchCreateOrders } from '@/api/orders.js'
import { mapActions, mapGetters } from 'vuex'
export default {
  name: 'ProcessOrderWhile',
  components: {
    StripeElementCard
  },
  computed: {
    ...mapGetters(['getShoppingCart']),
    productCount () {
      return this.getShoppingCart.product_count
    }
  },
  data () {
    return {
      card: {},
      loading: false,
      shoppingCart: {},
      paymentStatus: '',
      cardNumber: '',
      stripe: null,
      publishableKey: process.env.VUE_APP_SECRET_KEY,
      cardElement: null,
      active: 0,
      showCCV: false,
      result: true,
      showNewPassword: false,
      showPassword: false,
      imageUrl: '',
      provincia: {},
      provincias: [],
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
      },
      user: {},
      submittingPayment: false
    }
  },
  mounted () {
    this.methodShoppingCart()
    this.fetchData()
    this.fetchDataUserDirection2()
  },
  methods: {
    ...mapActions(['fetchShopping']),
    methodShoppingCart () {
      fetchShoppingCart().then((response) => {
        this.shoppingCart = response.data
        if (this.shoppingCart.product_count === 0) {
          router.push('/')
        }
      }).catch((error) => {
        console.error('Error al recuperar datos', error)
      })
    },
    submit () {
      this.loading = true
      this.$refs.elementRef.submit()
      fetchCreateOrders()
        .then(() => {
          this.$message.success('Pedido realizado correctamente')
          this.active = 2
        })
        .catch(() => {
          this.$message.error('Error al crear el pedido')
        })
    },
    tokenCreated (token) {
      setTimeout(() => {
        fetchPaymentProcess({ token: token, total: this.shoppingCart.total })
          .then((response) => {
            this.$message.success('Pago realizado correctamente')
            this.paymentStatus = response.data.success
            this.loading = false
          })
          .catch(() => {
            this.paymentStatus = false
            this.loading = false
            this.$message.error('Error al realizar el pago')
          })
      }, 1000)
    },
    validateExpiryDate (rule, value, callback) {
      const regex = /^(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})$/
      if (!regex.test(value)) {
        callback(new Error('Por favor introduce la fecha en formato MM/YY'))
      } else {
        const [month, year] = value.split('/')
        const currentYear = new Date().getFullYear() % 100
        const currentMonth = new Date().getMonth() + 1

        if (parseInt(year, 10) < currentYear || (parseInt(year, 10) === currentYear && parseInt(month, 10) < currentMonth)) {
          callback(new Error('La tarjeta ha expirado'))
        } else {
          callback()
        }
      }
    },
    submitFormDirection (form) {
      if (this.userDirectionData.direction !== null && this.userDirectionData.direction !== '') {
        this.$refs[form].validate((valid) => {
          if (valid) {
            fetchUserEditDirection(this.userDirectionData)
              .then(() => {
                this.$message.success('Cambios guardados correctamente')
                this.next()
              })
              .catch(() => {
                this.$message.error('Error al guardar los cambios. Por favor, inténtalo de nuevo.')
              })
          } else {
            this.$message.error('Por favor, completa correctamente el formulario.')
            return false
          }
        })
      } else {
        this.active = 0
        this.$message.error('Por favor, completa correctamente el formulario.')
      }
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
    next () {
      if (this.active === 3) {
        this.active = 0
      } else if (this.active === 2) {
        this.active += 1
      } else {
        if (Object.values(this.userDirectionData).some(value => value === null || value === '')) {
          this.active = 0
          this.$message.error('Error, debe  rellenar el formulario por favor')
        } else {
          this.active++
        }
      }
    },
    goBack () {
      router.push('/shoppingCart')
    },
    goBackIndex () {
      router.push('/user/orders')
    },
    open1 () {
      this.$notify({
        title: 'Success',
        message: 'This is a success message',
        type: 'success'
      })
    }
  }
}
</script>
<style scoped>
stripe-element-card-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stripe-element-card {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 80px;
  margin-bottom: 10px;
}
.pay-button {
  margin-top: 10px;
}

.content {
  margin-top: 12%;
  margin-bottom: 12%;
  padding-left: 50px;
  padding-right: 50px;
}

.creditCard {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: 260px;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  margin-bottom: 10px;
  background-color: #00BAB4;
}

.tarjeta .creditCard .logo-marca {
text-align: right;
min-height: 50px;
}

.tarjeta .creditCard .logo-marca img {
width: 100%;
height: 100%;
object-fit: cover;
max-width: 80px;
}

.creditCard .chip {
width: 100%;
margin-right: 80%;
max-width: 50px;
}

.creditCard .grupo .label {
font-size: 15px;
color: #ffffff;
margin-bottom: 10px;
}

.creditCard .grupo .numero,
.creditCard .grupo .nombre,
.creditCard .grupo .expiracion {
color: #ffffff;
font-size: 17px;
text-transform: uppercase;
}

.creditCard .flexbox {
display: flex;
justify-content: space-between;
margin-bottom: 10px;
}
</style>
