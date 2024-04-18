<template>
  <PageContainer>
    <h1>🔍 Unearth a Hidden Gem 💎</h1>
    <p>Embark on a treasure hunt through Wikipedia's forgotten pages! 📜</p>
    <p>Discover a random article from the past year that has been "lost" due to a view count lower than 100.</p>
    <form class="article-form" @submit.prevent="handleSubmit">
      <button class="article-button" type="submit">🗺️ Start the Quest! 🧭</button>
    </form>
    <div v-if="article.title" class="article-container">
      <h2>🎉 Eureka! You've Found a Lost Treasure! 🎉</h2>
      <a :href="'https://en.wikipedia.org/wiki/' + article.title" target="_blank" class="article-link">
        {{ article.title }}
      </a>
      <p v-if="!categoryError">Click here to discover what category your treasure belongs to:</p>
      <p v-else>Throughout Heaven and Earth, I alone am the honored one.</p>
      <button @click="getCategory(article.title)">🗺️ Reveal Category 🗺️</button>
      <div v-if="category" class="category-container">
        <h3>A Glimpse into the Realm:</h3>
        <a :href="category.category_link" target="_blank" class="category-link">{{ category.category_name }}</a>
        <p v-if="category.parent_category">In the Kingdom of: {{ category.parent_category }}</p>
      </div>
      <div v-if="categoryError" class="category-container">
        <img :src="gojoImage" alt="Gojo Satoru Honored One Pose" class="gojo-image">
        <h3>I Alone Am the Honored One</h3>
        <p>This article stands solitary in its splendor, much like Gojo Satoru's unrivaled presence.</p>
      </div>
    </div>
  </PageContainer>
</template>


<style scoped>
.page-container {
  text-align: center;
  margin-top: 50px;
}

.article-button {
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

.article-button:hover {
  background-color: #166fb8;
}

.title {
  text-align: center;
}

p {
  text-align: center;
  align-items: center;
}

.article-container {
  margin-top: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.article-link {
  font-size: 1.2em;
  color: #397595;
  text-decoration: none;
  transition: color 0.3s ease;
}

.article-link:hover {
  color: #166fb8;
}

.category-container {
  margin-top: 20px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
}
.category-link {
  color: #397595;
  text-decoration: none;
  transition: color 0.3s ease;
}

.category-link:hover {
  color: #166fb8;
}
.gojo-image {
  max-width: 40%;
  height: auto;
  margin-top: 20px;
}
</style>


<<script setup>
import { ref } from 'vue';
import axios from 'axios';

// Define reactive variables for storing the article, category, categoryError, and Gojo's image URL
const article = ref('');
const category = ref(null);
const categoryError = ref(false);
const gojoImage = ref('https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/b15ec0a6-b9f4-4188-815f-6db9ac169cb3/dfa6ty4-62c3b32f-1a5b-4bd4-b902-db7f32353af0.png/v1/fit/w_750,h_1208,q_70,strp/gojo_satoru___the_honored_one_by_itzzazure_dfa6ty4-375w-2x.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MjA2MiIsInBhdGgiOiJcL2ZcL2IxNWVjMGE2LWI5ZjQtNDE4OC04MTVmLTZkYjlhYzE2OWNiM1wvZGZhNnR5NC02MmMzYjMyZi0xYTViLTRiZDQtYjkwMi1kYjdmMzIzNTNhZjAucG5nIiwid2lkdGgiOiI8PTEyODAifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.DEFV5W0-cfcxAbgmRTdFUgcoaYNlRdrXiRtHDSrNXYw'); // URL of Gojo
// Function to handle form submission
const handleSubmit = async () => {
  try {
    const { data } = await axios.get(`http://127.0.0.1:5000/long-lost-article`);
    article.value = data;
    category.value = null; // Reset category and error state on new submission
    categoryError.value = false;
  } catch (error) {
    console.error('Error fetching long lost article:', error);
    alert('Oops! The treasure map seems to be missing. Please try again later.');
  }
};

const getCategory = async (articleTitle) => {
  try {
    const { data } = await axios.get(`http://127.0.0.1:5000/categories/${encodeURIComponent(articleTitle)}`);
    category.value = data;
    categoryError.value = false; // Reset the error state on successful fetch
  } catch (error) {
    console.error('Error fetching category:', error);
    category.value = null; 
    categoryError.value = true; // Set the error state to true
  }
};
</script>