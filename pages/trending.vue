<script setup lang="ts">

</script>

<template>
  <PageContainer>

    <div class="page-container">
      <div class="second-place">
        Second
      </div>

      <div class="first-place">
        First
      </div>

      <div class="third-place">
        Third
      </div>
    </div>
    
    
  </PageContainer>
</template>

<style scoped>
.page-container {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: flex-end; /* Align items at the bottom */
}

.first-place {
  height: 300px;
  width: 200px;
  background-color: aliceblue;
  align-self: flex-end; /* Align to the bottom */
}

.second-place {
  height: 175px;
  width: 200px;
  background-color: green;
  align-self: flex-end; /* Align to the bottom */
}

.third-place {
  height: 100px;
  width: 200px;
  background-color: red;
  align-self: flex-end; /* Align to the bottom */
}
</style>
