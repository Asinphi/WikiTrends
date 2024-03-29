<template>
  <img class="logo" alt="Temp logo" src="./assets/logo.png">
  <div class="navbar">
    <router-link to="/">Home</router-link>
    <router-link to="/trending">Trending</router-link>
    <router-link to="/search">Search</router-link>
    <router-link to="/long-lost-articles">Long Lost Articles</router-link>
  </div>
  <nuxt-page />
</template>

<script>
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.logo {
  display: block;
  margin: 0 auto;
}

.navbar {
  display: flex;
  margin: 0 auto;
  width: 80%;
  height: 50px;
  justify-content: space-around;
}
</style>
