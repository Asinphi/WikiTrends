<script setup lang="ts">

import PageContainer from "~/components/PageContainer.vue";
</script>

<template>
  <PageContainer>
    <h1>About</h1>
    <p>
      wikiTrends is a web-based application utilizing the Wikipedia API (MediaWiki) 
      alongside the Pageview API to gather article information based upon user input. 
      The trending page returns the top 3 trending articles for the day (or any date 
      set by user), the search page allows a user to search by a keyword for an article 
      and returns the view statistics for the given keyword, the "long lost article" 
      page returns a random article older than 10 years that has a low view count.
      <br>
    </p>
    <h1>Languages</h1>
    <p>
      Front-end: JavaScript using a Nuxt.js framework bundled with Vue.js & D3.js rendering 
      library Back-end: Python using a FastAPI framework APIs: Wikipedia MediaWiki & Pageview 
      API Database: Oracle SQL Developer
    </p>
  </PageContainer>
</template>

<style scoped>

</style>