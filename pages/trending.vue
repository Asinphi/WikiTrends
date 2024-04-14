<script setup lang="ts">

</script>

<template>
  <h1 class="title">Who's got the highest views today?</h1>
  <PageContainer>
    <row>
    <div class="timerange-container">
      <h1 class="timerange-title"> Trending Page </h1>
      <p2>
        Enter a date between 01-15-2001 and the current date, in format: MM-DD-YYYY: 
      </p2>
      <!-- <form class="timerange-form" @submit.prevent="handleSubmit">
        <input class="timerange-input" type="search" v-model="timeQuery" placeholder="Date" aria-label="timeQuery">
        <button class="timerange-button" type="submit">Search</button>
      </form>
      <p v-if="displayedTimeQuery" class="time-query-display">
      </p> -->
    </div>

    <div class="page-container">
      <div class="second-place">
        Second
        <!-- Article in second place here: -->
      </div>

      <div class="first-place">
        First
        <!-- Article in first place here: -->
      </div>

      <div class="third-place">
        Third
        <!-- Article in third place here: -->
      </div>
    </div> 
    </row>
  </PageContainer>
</template>

<style scoped>

/* Time range container formatting: */
.timerange-container {
  text-align: center;
  display: block;
  flex-direction: column;
  font-family: "Cambria";
  padding: 15px;
}

.timerange-title {
  font-size: 2em;
  color: #333;
}

.timerange-form {
  display: flex;
  justify-content: center;
}

.timerange-input {
  padding: 10px;
  border: 2px solid #ddd;
  border-radius: 5px;
  font-size: 1em;
  width: 300px;
}

.page-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: flex-end; /* Align items at the bottom */
  gap: 1rem;
}

.first-place {
  text-align: center;
  color: white;
  font-size: 1.5em;
  padding: 2.5%;
  height: 300px;
  width: 200px;
  background-color: rgb(0, 57, 106);
  align-self: flex-end; /* Align to the bottom */
}

.second-place {
  text-align: center;
  color: white;
  font-size: 1.5em;
  padding: 2.5%;
  height: 175px;
  width: 200px;
  background-color: rgb(54, 138, 198);
  align-self: flex-end; /* Align to the bottom */
}

.third-place {
  text-align: center;
  color: white;
  font-size: 1.5em;
  padding: 2.5%;
  height: 100px;
  width: 200px;
  background-color: rgb(139, 212, 255);
  align-self: flex-end; /* Align to the bottom */
}


.timerange-button {
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



</style>


<script setup>
import { ref, watch } from 'vue';

// Define a reactive variable for storing the time range query
const timeQuery = ref('');
const displayedTimeQuery = ref('');

// Function to handle form submission
const handleSubmit = () => {
  if (timeQuery.value.trim() !== '') {
    // Ensure the correct formatting here! MM-DD-YYY:
    // Implement search functionality here (for the time range specified), e.g., redirect to search results page
    console.log('Search for time range:', timeQuery.value.trim());
    displayedTimeQuery.value = timeQuery.value.trim();
  } else {
    alert('Please enter a time range');
  }
};

</script>