import aiohttp
import pandas as pd

class WikipediaAPIClient:
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    
    async def get_articles(self, limit=5000):
        params = {
            "action": "query",
            "list": "allpages",
            "aplimit": 500000,  
            "apfrom": "",
            "format": "json"
        }
        
        articles = []
        while len(articles) < limit:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.BASE_URL, params=params) as response:
                    data = await response.json()
                    articles.extend([article["title"] for article in data["query"]["allpages"]])
                    
                    if "continue" in data:
                        params["apfrom"] = data["continue"]["apcontinue"]
                    else:
                        break
        
        return articles[:limit]
    
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
                if "query" in data and "pages" in data["query"]:
                    pages = data["query"]["pages"]
                    if pages:
                        page_id = next(iter(pages))
                        page_data = pages[page_id]
                        return self._parse_article_info(page_data)
                print(f"No information found for article: {article_title}")
                return None
    
    def _parse_article_info(self, page_data):
        if "title" not in page_data:
            print(f"No title found for page: {page_data}")
            return None

        article_info = {
            "title": page_data["title"],
            "post_date": page_data.get("touched", ""),
            "last_updated": page_data.get("touched", ""),
            "categories": [
                {
                    "category_name": category["title"],
                    "category_link": f"https://en.wikipedia.org/wiki/{category['title'].replace(' ', '_')}"
                }
                for category in page_data.get("categories", [])
            ]
        }

        return article_info
    
    async def get_article_pageviews(self, article_title, start_date, end_date):
        endpoint = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article_title}/daily/{start_date}/{end_date}"
        
        headers = {
            'User-Agent': 'School Project',
            'Accept': 'application/json',
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    df = pd.DataFrame(data['items'])
                    df = df.rename(columns={
                        "timestamp": "view_date",
                        "views": "view_count"
                    })
                    return df
                else:
                    print(f"No response from API. Return Code: {response.status}")
                    return None
