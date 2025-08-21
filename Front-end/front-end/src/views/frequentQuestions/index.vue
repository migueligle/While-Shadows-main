<template>
    <div class="content"  v-loading="loading">
    <div>
      <el-page-header class="page-header" @back="goBack" title="Volver" content="Preguntas frecuentes">
      </el-page-header>
    </div>
    <h2>Preguntas frecuentes</h2>
    <el-divider></el-divider>
    <el-collapse v-model="activeName" accordion>
        <el-collapse-item title="¿Cuáles son los métodos de pago aceptados en While Shadows?" name="1">
            <div>
                En While Shadows, aceptamos tarjetas de crédito/débito (Visa, Mastercard, American Express).
            </div>
        </el-collapse-item>
        <el-collapse-item title="¿Cuánto tiempo tarda en llegar mi pedido?" name="2">
            <div>
                El tiempo de entrega varía según tu ubicación. normalmente, los
                pedidos dentro del país se entregan en un plazo de 1-15 días hábiles, mientras que los pedidos
                internacionales pueden tardar entre 10 y 30 días hábiles. Te proporcionaremos un número de seguimiento
                para que puedas rastrear tu pedido en tiempo real.
            </div>
        </el-collapse-item>
        <el-collapse-item title="¿Puedo devolver un producto si no estoy satisfecho?" name="3">
            <div>
                Sí, aceptamos devoluciones dentro de un plazo de 30 días a partir de la fecha de entrega del producto,
                siempre y cuando el artículo esté en su estado original y sin usar.
            </div>
        </el-collapse-item>
        <el-collapse-item title="¿Ofrecen garantía en sus productos?" name="4">
            <div>
                Sí, todos nuestros productos están respaldados por una garantía de 24 meses a partir de la fecha de
                compra. Esta garantía cubre defectos de fabricación y problemas relacionados con el funcionamiento del
                producto. Si experimentas algún problema no dudes en ponerte en contacto con el equipo de atención al cliente.
            </div>
        </el-collapse-item>
        <el-collapse-item
            title="¿Cómo puedo ponerme en contacto con el servicio de atención al cliente de While Shadows?" name="5">
            <div>
                Puedes ponerte en contacto con nuestro equipo de atención al cliente de varias formas: mediante correo
                electrónico a WhileShadows@gmail.com, a través de nuestro formulario de contacto en el sitio web o a traves de llamada telefónica ha nuestro equipo de atención al cliente
            </div>
        </el-collapse-item>
        <el-collapse-item title="¿Qué medidas toman para proteger la privacidad y seguridad de mis datos personales?"
            name="6">
            <div>
                En While Shadows, nos tomamos muy en serio la privacidad y seguridad de tus datos personales.
                por lo que no haremos un uso indebido de tus datos, para mas info consulta nuestras políticas de seguridad y cookies
            </div>
        </el-collapse-item>
    </el-collapse>
    </div>
</template>
<script>
import router from '@/router'
export default {
  name: 'userWhile',
  data () {
    return {
    loading: false,
    activeName: '1'
    }
  },
  methods: {
    goBack () {
      router.push('/')
    },
  }
}
</script>
<style scoped>
.content {
  margin-top: 40px;
  padding-left: 200px;
  padding-right: 200px;
  margin-bottom: 290px;

}
</style>
