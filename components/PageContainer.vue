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
  font-family: "Inter var experimental", Inter var, Inter, ui-sans-serif, system-ui, sans-serif;
  padding: 20px;
  margin-top: 50px;
  @include media-breakpoint-up(lg) {
    background-color: #c9cfe5;
    margin-left: 15%;
    margin-right: 15%;
    border-radius: 15px;
  }

  p {
    font-size: 1.4rem;
  }
}
</style>