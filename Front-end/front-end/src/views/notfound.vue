<template>
  <div class="home">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <el-card shadow="always" class="card">
            <img src="@/assets/mixer.png" alt="">
            <h1>4 0 4</h1><br>
            <h1>Page not found</h1>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView'
}
</script>

<style scoped>
.content {
  margin-top: 2px;
  padding-left: 200px;
  padding-right: 200px;
  margin-bottom: 200px;
}
img {
  opacity: 0.8;
  padding: 0;
}
h1 {
  display: flex;
  justify-content: center;
  font-family: "Zeniq Nano";
  color: #00BAB4;
  opacity: 0.8;
}
.card {
  width: 50%;
  border-radius: 15px;
  text-align: center;
  padding: 20px;
  margin: auto;
}
</style>
