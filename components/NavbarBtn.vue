<script setup lang="ts">
defineProps(["to"]);
</script>

<template>
  <router-link :to="to" class="navbar-btn"><slot /></router-link>
</template>

<style scoped lang="scss">
.navbar-btn {
  display: block;
  background-color: #2c3e50;
  color: #ecaa35;
  @include media-breakpoint-up(md) {
    font-size: 1.5rem;
  }
  @include media-breakpoint-down(md) {
    @include media-breakpoint-up(sm) {
      font-size: 1.2rem;
    }
    @include media-breakpoint-down(sm) {
      font-size: 1rem;
    }
  }
  font-family: Inter var experimental, Inter var, Inter, ui-sans-serif, system-ui, sans-serif;
  font-weight: 500;
  text-align: center;
  padding-top: 8px;
  padding-bottom: 5px;
  border: none;
  border-radius: 5px;
  text-decoration: none;
  transition: color 0.2s;

  &:hover {
    color: #eae6e4;
  }
}
</style>