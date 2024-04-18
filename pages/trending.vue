<template>
  <PageContainer>
    <row>
      <div class="timerange-container">
        <h1 class="timerange-title">Trending Page</h1>
        <p>Enter a date between 04-16-2023 and 04-16-2024, in format: MM-DD-YYYY:</p>
        <form class="timerange-form" @submit.prevent="handleSubmit">
          <input class="timerange-input" type="search" v-model="timeQuery" placeholder="Date" aria-label="timeQuery">
          <button class="timerange-button" type="submit">Search</button>
        </form>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
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
  align-items: flex-end;
  gap: 1rem;
}

.first-place {
  text-align: center;
  color: white;
  font-size: 1.5em;
  padding: 2.5%;
  height: 300px;
  width: 250px;
  background: linear-gradient(145deg, #ffd700, #ffec8b);
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  align-self: flex-end;
  border-radius: 10px;
}

.second-place {
  text-align: center;
  color: white;
  font-size: 1.5em;
  padding: 2.5%;
  height: 175px;
  width: 250px;
  background: linear-gradient(145deg, #c0c0c0, #f0f0f0);
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  align-self: flex-end;
  border-radius: 10px;
}

.third-place {
  text-align: center;
  color: white;
  font-size: 1.5em;
  padding: 2.5%;
  height: 100px;
  width: 250px;
  background: linear-gradient(145deg, #cd7f32, #e9b96e);
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  align-self: flex-end;
  border-radius: 10px;
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
import { ref } from 'vue';
import axios from 'axios';
import { parseDate } from 'chrono-node';

const timeQuery = ref('');
const displayedTimeQuery = ref('');
const articles = ref([]);
const errorMessage = ref('');

const handleSubmit = async () => {
  const input = timeQuery.value.trim();
  if (input) {
    const parsedDate = parseDate(input);
    const startDate = new Date('04-16-2023');
    const endDate = new Date('04-16-2024');

    if (parsedDate && parsedDate >= startDate && parsedDate <= endDate) {
      const formattedDate = formatDate(parsedDate);
      displayedTimeQuery.value = formattedDate;
      try {
        const { data } = await axios.get(`http://127.0.0.1:5000/top-three-articles?date=${formattedDate}`);
        articles.value = data;
        errorMessage.value = ''; // Clear any previous error message
      } catch (error) {
        errorMessage.value = 'Oops! It seems our digital athletes dropped the baton. Please try fetching articles again later.';
      }
    } else {
      errorMessage.value = '🏅 Unfortunately, your date did not qualify for the time range Olympics. Please enter a date between 04-16-2023 and 04-16-2024.';
    }
  } else {
    errorMessage.value = '🎉 And the "No Date Entered" event... goes to... you! Please enter a date to start the race.';
  }
};

const formatDate = (date) => {
  const monthNames = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
  const day = date.getDate();
  const monthIndex = date.getMonth();
  const year = date.getFullYear().toString().slice(-2);
  return `${day}-${monthNames[monthIndex]}-${year}`;
};
</script>