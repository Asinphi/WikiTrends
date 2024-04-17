<template>
  <PageContainer>
    <div class="timerange-container">
      <h1 class="timerange-title">Trending Page</h1>
      <p>Enter a date between 04-16-2023 and 04-16-2024, in format: MM-DD-YYYY:</p>
      <form class="timerange-form" @submit.prevent="handleSubmit">
        <input class="timerange-input" type="search" v-model="timeQuery" placeholder="Date" aria-label="timeQuery">
        <button class="timerange-button" type="submit">Search</button>
      </form>
      <p v-if="displayedTimeQuery" class="time-query-display">{{ displayedTimeQuery }}</p>
    </div>

    <div class="page-container">
      <div class="second-place">
        Second
        <!-- Article in second place here: -->
        <div v-if="articles.length > 1">{{ articles[1].title }}</div>
      </div>

      <div class="first-place">
        First
        <!-- Article in first place here: -->
        <div v-if="articles.length > 0">{{ articles[0].title }}</div>
      </div>

      <div class="third-place">
        Third
        <!-- Article in third place here: -->
        <div v-if="articles.length > 2">{{ articles[2].title }}</div>
      </div>
    </div>
  </PageContainer>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';

// Define a reactive variable for storing the time range query
const timeQuery = ref('');
const displayedTimeQuery = ref('');
const articles = ref([]);

// Function to handle form submission
const handleSubmit = async () => {
  if (timeQuery.value.trim() !== '') {
    const enteredDate = new Date(timeQuery.value.trim());
    const startDate = new Date('04-16-2023');
    const endDate = new Date('04-16-2024');

    // Check if the entered date is within the specified range
    if (enteredDate >= startDate && enteredDate <= endDate && !isNaN(enteredDate.getTime())) {
      displayedTimeQuery.value = timeQuery.value.trim();

      // Format the date as required by the backend
      const formattedDate = formatDate(enteredDate);

      try {
        // Call backend API to get top three articles
        const { data } = await axios.get(`http://127.0.0.1:5000/top-three-articles?date=${formattedDate}`);
        articles.value = data;
      } catch (error) {
        console.error('Error fetching top three articles:', error);
        alert('An error occurred while fetching the top three articles.');
      }
    } else {
      alert('Please enter a date between 04-16-2023 and 04-16-2024 in the format: MM-DD-YYYY');
    }
  } else {
    alert('Please enter a date.');
  }
};

// Function to format the date as required by the backend
const formatDate = (date) => {
  const monthNames = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
  const day = date.getDate();
  const monthIndex = date.getMonth();
  const year = date.getFullYear().toString().slice(-2);
  return `${day}-${monthNames[monthIndex]}-${year}`;
};
</script>
