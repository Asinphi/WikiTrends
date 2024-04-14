<script setup lang="ts">

</script>

<template>
  <PageContainer>
    <h1 class="title">Long Lost Articles</h1>
    <p>
      Find a lost article by clicking below!
    </p>
    <button class="find-button" type="submit">Find an Article</button>
    <!-- Make call to grab the data -->
  </PageContainer>
</template>

<style scoped>

.title {
  text-align: center;
}

p {
  text-align: center;
  align-items: center;
}

.find-button{
  margin-left: 43%;
  padding: 10px 20px;
  border: 2px solid #e0dcd8;
  border-radius: 5px;
  background-color: #397595;
  color: #fff;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.find-button:hover {
  background-color: #166fb8;
}

</style>