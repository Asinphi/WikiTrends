<template>
  <PageContainer>
    <div class="search-container">
      <h1 class="search-title">Search Page</h1>
      <form class="search-form" @submit.prevent="handleSubmit">
        <input class="search-input" type="search" v-model="searchQuery" placeholder="Search" aria-label="Search">
        <button class="search-button" type="submit">Search</button>
      </form>
      <p v-if="displayedSearchQuery" class="search-query-display">
      You searched for: 
      <a :href ="'http://en.wikipedia.org/wiki/' + displayedSearchQuery">{{ displayedSearchQuery }}</a>

      <div v-if="articles.length > 0">{{ articles[0].title }}</div>

      </p>
    </div>
    <br>
    <ClientOnly>
      <Graph :width="graphWidth" :margin-left="graphMarginLeft" v-if="displayedSearchQuery"/>
    </ClientOnly>
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

const pageContainerWidth = process.browser ? window.innerWidth * 0.7: 0;
const graphWidth = pageContainerWidth * 0.7;
const graphMarginLeft = pageContainerWidth * 0.1;
const graphMarginRight = pageContainerWidth * 0.15;

// Define a reactive variable for storing the search query
const searchQuery = ref('');
const displayedSearchQuery = ref('');


// Function to handle form submission
const handleSubmit = async () => {
  
  if (searchQuery.value.trim() !== '') {

    // Implement search functionality here, e.g., redirect to search results page
    console.log('Search for:', searchQuery.value.trim());
    displayedSearchQuery.value = searchQuery.value.trim();

    try {
      // Call backend API to get top three articles
      const { data } = await axios.get(`http://127.0.0.1:5000/searches?search=${searchQuery.value.trim()}`);
      articles.value = data;
    } catch (error) {
      console.error('Error fetching search:', error);
      console.error('Error details:', error.toJSON()); 
      alert('An error occurred while searching.');
    }
  } else {
    alert('Please enter a search query');
  }
};

</script>

