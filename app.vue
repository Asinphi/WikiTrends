<template>
  <!--<img class="logo" alt="Temp logo" src="./assets/logo.png">-->
  <h1 class="logo"><span class="logo__w">&#xe02f;</span>Trends</h1>
  <div class="navbar">
    <NavbarBtn to="/">Home</NavbarBtn>
    <NavbarBtn to="/trending">Trending</NavbarBtn>
    <NavbarBtn to="/search">Search</NavbarBtn>
    <NavbarBtn to="/long-lost-articles">Long Lost Articles</NavbarBtn>
  </div>
  <nuxt-page />
</template>

<script>
</script>

<style lang="scss">
@font-face {
  font-family: "Linux Libertine";
  src: url("assets/fonts/LinLibertine_R.ttf") format("truetype");
}

@keyframes
glow {
  from {
    text-shadow: 0 0 15px #397595;
  }
  to {
    text-shadow: 0 0 10px #7fb6ad, 0 0 20px #166fb8;
  }
}

.logo {
  text-align: center;
  font-family: "Linux Libertine", serif;
  margin: 1rem 0;
  cursor: default;
  animation: glow 1s ease-in-out infinite alternate;
  @include media-breakpoint-up(lg) {
    font-size: 18rem;
  }

  @include media-breakpoint-down(lg) {
    font-size: 8rem;
  }

  @include media-breakpoint-down(sm) {
    font-size: 4rem;
  }

  &__w {
    color: #3498db;
    @include media-breakpoint-up(lg) {
      font-size: 12rem;
    }
  }
}

body {
  background-color: #e0dcd8;
  font-family: "Linux Libertine", Avenir, Helvetica, Arial, sans-serif;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.navbar {
  display: flex;
  margin: 0 auto;
  @include media-breakpoint-up(md) {
    width: 80%;
  }
  @include media-breakpoint-down(md) {
    width: 95%;
  }
  height: 50px;
  justify-content: space-around;
  background-color: #2c3e50;
  border-radius: 25px;
  border: #4b83cc 4px solid;
}
</style>
