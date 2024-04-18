<template>
  <PageContainer>
    <div class="search-container">
      <h1 class="search-title">Search Page</h1>
      <form class="search-form" @submit.prevent="handleSubmit">
        <input class="search-input" type="search" v-model="searchQuery" placeholder="Search" aria-label="Search">
        <button class="search-button" type="submit">Search</button>
      </form>
      <div v-if="isLoading" class="loading-indicator">
        <div class="spinner"></div>
        <p>Loading...</p>
      </div>
      <div v-else-if="displayedArticles.length > 0" class="graph-grid-container">
        <div class="graph-grid">
          <div v-for="(article, index) in displayedArticles" :key="index" class="graph-item">
            <h3>{{ article.article.title }}</h3>
            <ClientOnly>
              <Graph :width="graphWidth" :margin-left="graphMarginLeft" :article="article"
                @graphClicked="handleGraphClick(article)" />
            </ClientOnly>
          </div>
          <div v-if="displayedArticles.length % 2 !== 0" class="graph-item placeholder"
            v-for="n in 2 - (displayedArticles.length % 2)" :key="`placeholder-${n}`"></div>
        </div>
      </div>
      <div v-if="expandedGraph" class="expanded-graph">
  <ClientOnly>
    <div class="expanded-graph-content">
      <Graph
        :width="800"
        :margin-left="50"
        :article="expandedGraph"
        class="expanded-graph-graph"
      />
      <a
        :href="`http://en.wikipedia.org/wiki/${expandedGraph.article.title}`"
        target="_blank"
        rel="noopener noreferrer"
        class="expanded-graph-link"
      >
        View on Wikipedia
      </a>
    </div>
  </ClientOnly>
</div>
      <div v-else-if="!isLoading && displayedSearchQuery" class="no-results">
        No results found for "{{ displayedSearchQuery }}".
      </div>
    </div>
  </PageContainer>
</template>

<style scoped>
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

.search-button i {
  margin-right: 5px;
}

.search-results {
  margin-top: 30px;
  text-align: left;
}

.search-results ul {
  list-style-type: none;
  padding: 0;
}

.search-results li {
  margin-bottom: 10px;
}

.search-results a {
  color: #397595;
  text-decoration: none;
}

.search-results a:hover {
  text-decoration: underline;
}

.no-results {
  margin-top: 30px;
  font-style: italic;
  color: #777;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.graph-grid-container {
  max-height: 600px;
  width: 100%;
  overflow-y: auto;
}

.graph-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 10px;
}

.graph-item {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.graph-item h3 {
  font-size: 14px;
  margin-bottom: 5px;
}

.placeholder {
  background-color: transparent;
  box-shadow: none;
}

.expanded-graph {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999; /*hehe*/
}


.expanded-graph-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.expanded-graph-link {
  display: block;
  text-align: center;
  margin-top: 10px;
  color: #397595;
  text-decoration: none;
}

.expanded-graph-link:hover {
  text-decoration: underline;
}
</style>

<script setup>
import { ref, watch, computed, onMounted, onUnmounted } from 'vue';
import axios from 'axios';

const pageContainerWidth = process.browser ? window.innerWidth * 0.9 : 0;
const graphWidth = ref(0);
const graphMarginLeft = ref(0);

const calculateGraphDimensions = () => {
  const containerWidth = pageContainerWidth * 0.9;
  graphWidth.value = (containerWidth / 3) - 30; // Reduced width to fit 3 graphs in a row
  graphMarginLeft.value = 15; // Adjusted marginLeft to center the graphs
};

const expandedGraph = ref(null);

const handleGraphClick = (article) => {
  expandedGraph.value = article;
};

const handleDocumentClick = (event) => {
  if (expandedGraph.value && !event.target.closest('.graph-container')) {
    expandedGraph.value = null;
  }
};

const handleKeyDown = (event) => {
  if (event.key === 'Escape' && expandedGraph.value) {
    expandedGraph.value = null;
  }
};

onMounted(() => {
  calculateGraphDimensions();
  window.addEventListener('resize', calculateGraphDimensions);
  document.addEventListener('click', handleDocumentClick);
  document.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('resize', calculateGraphDimensions);
  document.removeEventListener('click', handleDocumentClick);
  document.removeEventListener('keydown', handleKeyDown);
});

const searchQuery = ref('');
const displayedSearchQuery = ref('');
const articles = ref([]);
const isLoading = ref(false);

// Computed property to handle empty articles array
const displayedArticles = computed(() => {
  return articles.value.length > 0 ? articles.value : [];
});



// Function to handle form submission
const handleSubmit = async () => {
  if (searchQuery.value.trim() !== '') {
    displayedSearchQuery.value = searchQuery.value.trim();
    isLoading.value = true; // Set loading state to true

    try {
      const response = await axios.get(`http://127.0.0.1:5000/searches/${searchQuery.value.trim()}`);
      articles.value = response.data;
    } catch (error) {
      console.error('Error fetching search:', error);
      alert('An error occurred while searching.');
    } finally {
      isLoading.value = false; // Set loading state to false
    }
  } else {
    alert('Please enter a search query');
  }
};


</script>