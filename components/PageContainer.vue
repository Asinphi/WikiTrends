<script setup lang="ts">

</script>

<template>
  <div class="page-container">
    <slot />
  </div>
</template>

<style lang="scss">
.page-container {
  display: block;
  flex-direction: column;
  min-height: 40vh;
  font-family: "Cambria";
  padding: 20px;
  margin-top: 20px;
  @include media-breakpoint-up(lg) {
    background-color: #c9cfe5;
    margin-left: 15%;
    margin-right: 15%;
    border-radius: 15px;
  }

  p {
    background-color: #ffffff;
    font-size: 1.5rem;
    padding: 5px;
    border-radius: 15px;
  }

  /* Added so that some text wasn't in same style as p*/
.p2 {
    font-size: 1.25rem;
    padding: 100px;
  }

  /* Added this so rows were possible within the page-container columns*/
.row {
    flex-direction: row;
    align-items: center;
  }

}
</style>