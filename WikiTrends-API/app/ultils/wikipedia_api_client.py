import aiohttp

class WikipediaAPIClient:
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    
    async def get_article_info(self, article_title):
        params = {
            "action": "query",
            "prop": "info|categories",
            "titles": article_title,
            "format": "json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params) as response:
                data = await response.json()
                return self._parse_article_info(data)
    
    def _parse_article_info(self, data):
        pages = data["query"]["pages"]
        page_id = next(iter(pages))
        page_data = pages[page_id]
        
        article_info = {
            "title": page_data["title"],
            "post_date": page_data.get("touched", ""),
            "last_updated": page_data.get("touched", ""),
            "categories": [category["title"] for category in page_data.get("categories", [])]
        }
        
        return article_info