<template>
   <div class="footer">
      <el-col :span="8" style="margin-top: 20px">
        <div class="container-wrapper">
          <el-col>
            <div>
              <img
                src="@/assets/LOGO CORTO SIN FONDO.png"
                alt="Logo"
                style="width: 15%; min-width: 15%; display: flex; justify-content: left;"
              />
            </div>
            <br />
          </el-col>
          <el-col :span="8">
            <h4>Sobre Nosotros</h4>
            <ul class="ul-footer">
              <li  @click="scrollToTop"><router-link to="/frequentQuestions" style=" text-decoration: none; color: white;" >Preguntas frecuentes</router-link></li>
              <li  @click="scrollToTop"><router-link to="/contact" style=" text-decoration: none; color: white;" >Contacto</router-link></li>
              <li  @click="scrollToTop"><router-link to="/Politics" style=" text-decoration: none; color: white;" >Políticas de privacidad y cookies</router-link></li>
            </ul>
          </el-col>
          <el-col :span="8">
            <h4>Usuarios</h4>
            <ul class="ul-footer">
              <li  @click="scrollToTop"><router-link to="/RecoverPassword" style=" text-decoration: none; color: white;">Recuperar Contraseña</router-link></li>
            </ul>
          </el-col>
          <el-col :span="8">
            <h4>Productos</h4>
            <ul class="ul-footer">
              <li  @click="scrollToTop"><router-link to="/products" style=" text-decoration: none; color: white;">Productos</router-link></li>
              <li  @click="scrollToTop"><router-link to="/categories" style=" text-decoration: none; color: white;" >Categorías</router-link></li>
            </ul>
          </el-col>
          <div class="container">
            <el-col> <p class="text">© 2023-2024 While Shadows</p></el-col>
          </div>
        </div>
      </el-col>
    </div>
</template>
<script>
export default {
  name: 'footerNav',
  data () {
    return {
    }
  },
  methods: {
    scrollToTop () {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      })
    }
  }
}
</script>
<style scoped>
template{
  margin: 0;
}
li{
  list-style:none;
}
.container-wrapper {
  background-color: rgba(51, 51, 51, 0.6);
  color: #fff;
  padding: 10px;
  height: 350px;
  text-decoration: none;
  list-style:none;
  width: 100vw;
  margin-bottom: 0;
  margin-left: 0;
  margin: 0 !important;
  box-sizing: border-box;
}
@media screen and (max-width: 768px) {
  .container-wrapper {
    padding: 5px;
  }
}
  @media screen and (max-width: 768px) {
  ul {
    flex-direction: column;
  }

  li {
    width: 100%;
  }
}
li {
  width: 100%;
  margin: 5px 0;
}
.ul-footer{
  list-style-type: none;
  display: flex;
  flex-wrap: wrap;
  flex-direction: column;
  padding: 0;
}
.footer-a{
  color: #fff;
  justify-content: right;
  padding-left: 70%;

}
</style>
