<template>
  <PageContainer>
    <row>
    <div class="timerange-container">
      <h1 class="timerange-title"> Trending Page </h1>
      <p2>
        Enter a date between 04-16-2023 and 04-16-2024, in format: MM-DD-YYYY: 
      </p2>
      <form class="timerange-form" @submit.prevent="handleSubmit">
        <input class="timerange-input" type="search" v-model="timeQuery" placeholder="Date" aria-label="timeQuery">
        <button class="timerange-button" type="submit">Search</button>
      </form>
      <p v-if="displayedTimeQuery" class="time-query-display">
      </p>
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
  width: 250px;
  background-color: rgb(0, 57, 106);
  align-self: flex-end; /* Align to the bottom */
}

.second-place {
  text-align: center;
  color: white;
  font-size: 1.5em;
  padding: 2.5%;
  height: 175px;
  width: 250px;
  background-color: rgb(54, 138, 198);
  align-self: flex-end; /* Align to the bottom */
}

.third-place {
  text-align: center;
  color: white;
  font-size: 1.5em;
  padding: 2.5%;
  height: 100px;
  width: 250px;
  background-color: rgb(116, 182, 221);
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
import axios from 'axios'

// Define a reactive variable for storing the time range query
const timeQuery = ref('');
const displayedTimeQuery = ref('');

// Function to handle form submission
const handleSubmit = async () => {
  if (timeQuery.value.trim() !== '') {
    const enteredDate = new Date(timeQuery.value.trim());
    const startDate = new Date('04-16-2023');
    const endDate = new Date('04-16-2024');

    const enteredMonth = enteredDate.getMonth() + 1;
    const enteredDay = enteredDate.getDate();
    const enteredYear = enteredDate.getFullYear().toString().slice(-2);

    let monthString = '';
    var formattedDate = '';

    // Need for formatting
    switch (enteredMonth) {
      case 1:
        monthString = 'JAN';
        break;
      case 2:
        monthString = 'FEB';
        break;
      case 3:
        monthString = 'MAR';
        break;
      case 4:
        monthString = 'APR';
        break;
      case 5:
        monthString = 'MAY';
        break;
      case 6:
        monthString = 'JUN';
        break;
      case 7:
        monthString = 'JUL';
        break;
      case 8:
        monthString = 'AUG';
        break;
      case 9:
        monthString = 'SEP';
        break;
      case 10:
        monthString = 'OCT';
        break;
      case 11:
        monthString = 'NOV';
        break;
      case 12:
        monthString = 'DEC';
        break;
      default:
        monthString = '';
    }
    formattedDate = enteredDay + '-' + monthString + '-' + enteredYear;


    // Check if the entered date is within the specified range
    if (enteredDate >= startDate && enteredDate <= endDate && !isNaN(enteredDate.getTime())) {
      console.log('Search for time range:', timeQuery.value.trim());
      displayedTimeQuery.value = timeQuery.value.trim();
      console.log("formattedDate", formattedDate)


      // Call backend 
      let {data} = await axios.get('http://127.0.0.1:5000/top-three-articles')
      window.console.log('Search for:', formattedDate);
      window.console.log('Message recieved: ', data)

    } else {
      alert('Please enter a date between 04-16-2023 and 04-16-2024 in the format: MM-DD-YYYY');
    }
  } else {
    alert('Please enter a date.');
  }


  

  
};

</script>
