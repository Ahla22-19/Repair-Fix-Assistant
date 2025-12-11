import requests

class WebSearchTool:
    def __init__(self):
        self.session = requests.Session()

    def search(self, query: str):
        """
        Perform a simple web search (fallback)
        """
        # For hackathon: using DuckDuckGo HTML scrape
        url = f"https://duckduckgo.com/html/?q={query}"
        resp = self.session.get(url)
        resp.raise_for_status()
        # Minimal extraction: return raw HTML for now
        return resp.text
