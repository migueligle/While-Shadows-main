<template>
  <div>
    <div class="menu-container">
      <el-menu
        class="menu"
        mode="horizontal"
        background-color="#333"
        text-color="#fff"
      >
        <el-menu-item class="div-logo">
          <router-link to="/">
            <img src="@/assets/ISOTIPO_SIN_FONDO.png" alt="Logo" class="logo" />
          <span class="titulo">WHILE SHADOWS</span>
        </router-link>
        </el-menu-item>
        <el-menu-item class="center_item">
  <el-input v-model="searchQuery" placeholder="Buscar">
    <template #append>
      <el-button @click="SearchProduct" icon="el-icon-search"></el-button>
    </template>
  </el-input>
</el-menu-item>
        <div class="left_item">
          <el-menu-item v-if="this.token" index="2"  @click="scrollToTop">
            <router-link to="/user">
              <i class="el-icon-user-solid"></i>
            </router-link>
          </el-menu-item>
          <el-menu-item index="1" v-else>
            <el-button @click="dialogVisible = true">Login</el-button>
          </el-menu-item>
          <el-menu-item index="3"  @click="scrollToTop"> <router-link to="/products">Productos</router-link></el-menu-item>
          <el-menu-item index="4"  @click="scrollToTop"> <router-link to="/categories">Categorías</router-link></el-menu-item>
          <el-menu-item v-if="token" index="5"  @click="scrollToTop">
            <el-badge :value="productCount" class="item">
              <router-link to="/shoppingCart">
                <i class="el-icon-shopping-cart-1"></i>
              </router-link>
            </el-badge>
          </el-menu-item>
          <el-menu-item index="6" @click="scrollToTop">
            <router-link to="/contact">Contacto</router-link>
            </el-menu-item>
          <el-menu-item v-if="isStaff" index="7"  @click="scrollToTop">
            <router-link to="/admin">Administración</router-link>
          </el-menu-item>
        </div>
      </el-menu>
    </div>
    <div class="content">
      <el-dialog
        title="Login"
        :visible="dialogVisible"
        @update:visible="updateDialogVisible"
        @before-close="dialogVisible = false"
        width="40%"
        :close-on-click-modal="false"
      >
        <div class="m-3 text-center">
          <el-link
            href="https://element-plus.org/en-US/"
            :underline="false"
            class="m-0"
          >
            <img
              src="@/assets/LOGO_CORTO.png"
              class="block"
              alt="While Shadows"
              width="120"
              height="40"
            />
          </el-link>
        </div>
        <el-form label-position="top">
          <el-form-item label="Email">
            <el-input v-model="email" size="large" />
          </el-form-item>
          <el-form-item class="inputPass" label="Password" prop="pass">
            <el-input :type="showPassword ? 'text' : 'password'" v-model="password" size="large" >
              <template #append>
              <el-button class="buttonPass" icon="el-icon-view" @click="viePassword()"></el-button>
            </template>
            </el-input>
          </el-form-item>
          <div class="flex justify-between mb-2">
            <el-checkbox v-model="checked">Acuérdate de mi </el-checkbox><br><br>
            <el-link type="primary" @click="goRecoverpass">¿Has olvidado tu contraseña?</el-link><br><br>
          </div>
          <span tag="p" class="text-[#868e96]">
            ¿No tienes una cuenta?
            <el-link type="primary" @click="goSignUp">Regístrate</el-link><br><br>
          </span>
          <br />
          <el-button type="primary" size="large" class="w-full" @click="login()">Sign in</el-button>
        </el-form>
      </el-dialog>
    </div>

  </div>
</template>

<script>
/* eslint-disable */
import { fetchUserlogin } from '@/api/login'
import router from '@/router'
import { jwtDecode  }from 'jwt-decode'
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'navbarMenu',
  computed: {
    ...mapGetters(['getShoppingCart']),
    productCount() {
      return this.getShoppingCart.product_count
    }
  },
  data () {
    return {
      showPassword: false,
      isFooterVisible: false,
      ShoppingCart: {
        product_count: 0
      },
      searchQuery: '',
      dialogVisible: false,
      user_name: false,
      token:localStorage.getItem('color') ? localStorage.getItem('color'): false,
      isStaff:false,
      form: {},
      id: '',
      token: '',
      loginResponse: {},
      loginError: '',
      email: '',
      password: '',
      checked: false
    }
  },
  methods: {
    ...mapActions(['fetchShopping']),
    viePassword () {
      if (this.showPassword === false) {
        this.showPassword = true
      } else {
        this.showPassword = false
      }
    },
    goSignUp(){
      router.push('/signUp')

      this.dialogVisible = false
    },
    goRecoverpass(){
      router.push('/RecoverPassword')

      this.dialogVisible = false
    },
    SearchProduct () {
      router.push({ path: '/products', query: { nameSearch: this.searchQuery }})
    },
    scrollToTop () {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    },
    updateDialogVisible (value) {
      this.dialogVisible = value
    },
    async login () {
      try {
        let post = {
          email: this.email,
          password: this.password
        }

        const response = await fetchUserlogin(post)

        if (response && response.access) {
          try {
            this.$message.success('inicio de sesión satisfactorio')
            const decodedToken = jwtDecode(response.access)
            this.isStaff = decodedToken.is_staff
            this.id=decodedToken.id
            localStorage.setItem('id', this.id)
            if (this.isStaff===true){
              localStorage.setItem('isStaff', this.isStaff)
            }
          } catch (error) {
          console.error(error);
          }
          localStorage.setItem('color', response.access)
          this.token = localStorage.getItem('color')
          this.loginResponse = response.access
          this.user_name = true
          this.dialogVisible = false
          if (this.checked==true){
            localStorage.setItem('email', this.email)
            localStorage.setItem('password', this.password)
          }
        } else {
          this.$message.error('Error: el correo o la contraseña son erroneos')
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$message.error('usuario o contraseña incorrecta')
        } else if (error.response && error.response.status === 500) {
          this.$message.error('Error inesperado')
        } else {
          this.$message.error('Error: el correo o la contraseña son erroneos')
        }
      }
    }
  },
  mounted () {
    const storedToken = localStorage.getItem('color')
    if (storedToken) {
      this.token = storedToken
      const decodedToken = jwtDecode(storedToken)
    this.isStaff = decodedToken.is_staff
    }
    const email = localStorage.getItem('email')
    const pass = localStorage.getItem('password')
    if (email && pass) {
      this.email = email
      this.password=pass
    }
    this.$store.dispatch('fetchShopping')
  }
}
</script>

<style scoped>
@font-face {
  font-family: "Zeniq Nano";
  src: url('@/assets/fonts/Zeniq Nano.otf');
}
.titulo{
  font-family: "Zeniq Nano";
  color: #00BAB4;
  font-size:large;
}
.content {
  margin-top: 100px;

}
.menu-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}
.div-logo {
  max-width: 10%;
}
.div-logo:hover {
  background-color: #333333 !important;
}
.menu {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  padding: 10px;
}
.logo {
  height: auto;
  width: 60%;
  min-width: 20%;
  margin-right: 45px;
}
.left_item {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  margin-right: 25px;
  margin-left: 40%;
}
.center_item {
  flex-grow: 1;
  margin-left: 20%;
  margin-right: 10%;
  width: 100%;
  max-width: 300px;
}
.center_item:hover{
  flex-grow: 1;
  background-color: #333333!important;
  margin-left: 20%;
  margin-right: 10%;
  width: 100%;
  max-width: 300px;
}
.image {
  width: 100%;
  display: block;
}
a {
  text-decoration: none;
  color: black;
}
.text {
  text-align: center;
}
@media screen and (max-width: 768px) {
  .content {
    padding: 10px;
  }
  .carrusel {
    margin-top: 60px;
  }

  .body-style {
    padding: "10px";
  }
  .container-wrapper {
    padding: 5px;
  }
}
.footer-a {
  color: #fff;
  justify-content: right;
  padding-left: 70%;
}
a {
  color: #fff;
}
.product {
  color: black;
}
@media screen and (max-width: 768px) {
  .menu {
    text-align: center;
  }

  .menu-container {
    padding: 10px;
  }
    .logo {
    margin-right: 0;
  }

  .menu-container {
    padding: 10px;
  }
}

</style>
