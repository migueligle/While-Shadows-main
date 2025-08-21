<template>
  <div class="content">
    <el-page-header class="page-header" @back="goBack" title="Volver" content="Políticas">
    </el-page-header>
    <div class="privacy-policy">
      <h2>Política de Privacidad de While Shadows</h2>
      <p>
        En While Shadows, nos comprometemos a proteger y respetar tu privacidad. Esta Política de Privacidad explica de que manera recogemos tus datos , usamos y la  protegemos.
      </p>
      <h3>Información que recogemos:</h3>
      <p>
        <strong>Información que nos proporcionas directamente:</strong> Cuando te registras en nuestro sitio web, realizas una compra o te comunicas con nosotros por cualquier motivo, podemos recopilar información personal como tu nombre, dirección de correo electrónico, dirección postal, número de teléfono y detalles de pago.
      </p>
      <h3>Uso de la información:</h3>
      <ul>
        <li>realizar tus pedidos y proporcionarte los productos o servicios que has solicitado.</li>
        <li>Comunicarnos contigo sobre tu cuenta, pedidos y cualquier problema relacionado con nuestros servicios.</li>
        <li>Mejorar y personalizar tu experiencia en nuestro sitio web.</li>
      </ul>
      <h3>Divulgación de la información:</h3>
      <p>
        No compartimos tu información personal con terceros, excepto en las siguientes circunstancias:
        <ul>
          <li>Con proveedores de servicios.</li>
          <li>Cuando sea necesario para cumplir con la ley</li>
          <li>En caso de que While Shadows sea comprada por.. o fusionada con otra empresa, tu información personal puede ser pasada a los nuevos propietarios.</li>
        </ul>
      </p>
      <h3>Cookies:</h3>
      <p>
        Utilizamos cookies y tecnologías similares para recopilar información sobre cómo utilizas nuestro sitio web y mejorar tu experiencia. Puedes configurar tu navegador para que rechace todas las cookies o te avise cuando se envíe una cookie. Sin embargo, si bloqueas las cookies, es posible que no puedas acceder a ciertas partes de nuestro sitio web.
      </p>
      <p>
        Al utilizar nuestro sitio web o proporcionarnos tu información personal, aceptas la recopilación, uso y transmisión  de tu información de acuerdo con esta Política de Privacidad.
      </p>
      <p>
        Si tienes alguna pregunta o duda sobre nuestra Política de Privacidad o nuestras prácticas de privacidad, no dudes en contactarnos en <a href="mailto:WhileShadows@gmail.com">WhileShadows@gmail.com</a>.
      </p>
    </div>

  </div>
</template>

<script>
import router from '@/router'
export default {
  name: 'PoliticsWhile',
  data () {
    return {
      currentDate: new Date()
    }
  },
  methods: {
    logout () {
      localStorage.clear()
      router.push('/')
      window.location.reload()
    },
    goBack () {
      router.push('/')
    }
  }
}
</script>

<style scoped>
.content {
  margin-top: 150px;
  padding-left: 200px;
  padding-right: 200px;

}
.privacy-policy {
  font-family: Arial, sans-serif;
  line-height: 1.6;
}

.privacy-policy h2 {
  font-size: 1.5em;
  margin-bottom: 10px;
}

.privacy-policy h3 {
  font-size: 1.2em;
  margin-bottom: 5px;
}

.privacy-policy p {
  margin-bottom: 10px;
}

.privacy-policy ul {
  margin-bottom: 10px;
  margin-left: 20px;
}

.privacy-policy a {
  color: blue;
}
ul {
    list-style: none;
}
</style>
