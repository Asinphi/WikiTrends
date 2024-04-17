<script>
// api.js
import axios from 'axios';
import { BASE_URL } from './config';

export default {
  getLongLostArticle() {
    return axios.get(`${BASE_URL}/long-lost-article`);
  },
  createUserSearch(searchTerm) {
    return axios.post(`${BASE_URL}/user-search`, { searchTerm });
  },
  getTopThreeArticles(date) {
    return axios.get(`${BASE_URL}/top-three-articles`, {
      params: { date }
    });
  }
};

</script>