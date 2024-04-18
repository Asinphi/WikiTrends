<script setup lang="ts">

</script>

<template>
  <PageContainer>
    <h1>Long Lost Article</h1>
    <p>Discover a random article from the past year that has been "lost" due to a view count lower than 100</p>
    <button class="article-button" type="submit">Find an Article</button>  
    <!-- Make call to grab the data -->
  </PageContainer>
</template>

<style scoped>
.page-container {
  text-align: center;
  margin-top: 50px;
}

.article-button {
  margin-left: 10px;
  padding: 10px 20px;
  border: 2px solid #e0dcd8;
  border-radius: 5px;
  background-color: #397595;
  color: #fff;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.article-button:hover {
  background-color: #166fb8;
}

.title {
  text-align: center;
}

p {
  text-align: center;
  align-items: center;
}
</style>