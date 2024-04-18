<template>
  <PageContainer>
    <div class="search-container">
      <h1 class="search-title">Search Page</h1>
      <form class="search-form" @submit.prevent="handleSubmit">
        <input class="search-input" type="search" v-model="searchQuery" placeholder="Search" aria-label="Search">
        <button class="search-button" type="submit">Search</button>
      </form>
      <div v-if="articles.length > 0">
        <div v-for="(article, index) in articles" :key="index">
          <h2>{{ article.article.title }}</h2>
          <ClientOnly>
            <Graph :width="graphWidth" :margin-left="graphMarginLeft" :article="article" />
          </ClientOnly>
        </div>
      </div>
    </div>
  </PageContainer>
</template>


<style scoped>
/* Scoped CSS for this component */
.search-container {
  text-align: center;
  margin-top: 50px;
}

.search-title {
  font-size: 2em;
  margin-bottom: 20px;
  color: #333;
}

.search-form {
  display: flex;
  justify-content: center;
}

.search-input {
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 5px;
  font-size: 1em;
  width: 300px;
}

.search-button {
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

.search-button:hover {
  background-color: #166fb8;
}

.search-query-display {
  margin-top: 20px;
  font-size: 1.2em;
}
</style>


<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';

const pageContainerWidth = process.browser ? window.innerWidth * 0.7 : 0;
const graphWidth = pageContainerWidth * 0.7;
const graphMarginLeft = pageContainerWidth * 0.1;
const graphMarginRight = pageContainerWidth * 0.15;

// Define a reactive variable for storing the search query
const searchQuery = ref('');
const displayedSearchQuery = ref('');
const articles = ref([]);

// Function to handle form submission
const handleSubmit = async () => {
  if (searchQuery.value.trim() !== '') {
    displayedSearchQuery.value = searchQuery.value.trim();
    try {
      const response = await axios.get(`http://127.0.0.1:5000/searches/${searchQuery.value.trim()}`);
      articles.value = response.data;
    } catch (error) {
      console.error('Error fetching search:', error);
      alert('An error occurred while searching.');
    }
  } else {
    alert('Please enter a search query');
  }
};
</script>