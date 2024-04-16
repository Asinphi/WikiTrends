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
      <!-- <a :href ="displayedSearchQuery">{{ displayedSearchQuery }}</a> -->
      <a :href ="displayedSearchQuery">{{ displayedSearchQuery }}</a>
      </p>
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


<script setup lang="ts"> //setup 
import { ref, watch } from 'vue';
import axios from 'axios'// Define a reactive variable for storing the search query
const searchQuery = ref('');
const displayedSearchQuery = ref('')// Function to handle form submission
const handleSubmit = async () => {
  if (searchQuery.value.trim() !== '') {
    // Implement search functionality here, e.g., redirect to search results page
    // const {data} = await $fetch('http://127.0.0.1:5000/api/search')
    let {data} = await axios.get('http://127.0.0.1:5000/api/search')
    window.console.log('Search for:', searchQuery.value.trim());
    // window.console.log('Message recieved: ', JSON.stringify(data.value))
    window.console.log('Message recieved: ', data)

    // displayedSearchQuery.value = JSON.stringify(data.value)
    displayedSearchQuery.value = data
    // displayedSearchQuery.value = searchQuery.value.trim();
  } else {
    alert('Please enter a search query');
  }
};
</script>
