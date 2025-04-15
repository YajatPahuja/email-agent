from serpapi import GoogleSearch
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class SearchTool:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")

    def search(self, query: str, num_results: int = 3) -> List[Dict[str, str]]:
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": num_results
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get('organic_results', [])
        
        return [
            {
                "title": result.get("title"),
                "link": result.get("link"),
                "snippet": result.get("snippet", "No snippet available.")
            }
            for result in organic_results[:num_results]
        ]
    
tool = SearchTool()
results = tool.search("John Doe site:linkedin.com")

for idx, res in enumerate(results, 1):
    print(f"{idx}. {res['title']}")
    print(f"   {res['link']}")
    print(f"   {res['snippet']}\n")
