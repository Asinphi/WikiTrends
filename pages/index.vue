<script setup lang="ts">

import PageContainer from "~/components/PageContainer.vue";

</script>

<template>
  <PageContainer>
    <h1>About</h1>
    <p>
      wikiTrends is a web-based application utilizing the Wikipedia API (MediaWiki) 
      alongside the Pageview API to gather article information based upon user input for 2023-2024. 
      The trending page returns the top 3 trending articles for any date 
      set by user in the past year, the search page allows a user to search by a keyword for an article 
      and returns the view statistics for the given keyword if found in the database, 
      the "long lost article" page returns a random article with a view count lower than 1.
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