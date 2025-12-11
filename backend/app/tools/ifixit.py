import requests

IFIXIT_BASE = "https://www.ifixit.com/api/2.0"

class IFixitTool:
    def __init__(self):
        self.session = requests.Session()

    def search_device(self, query: str):
        """
        Convert user query to iFixit device title
        """
        url = f"{IFIXIT_BASE}/search/{query}?filter=device"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        return self._cleanup_search_device(data)

    def list_guides(self, device_title: str):
        """
        List all guides for a given device
        """
        url = f"{IFIXIT_BASE}/wikis/CATEGORY/{device_title}"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        return self._cleanup_list_guides(data)

    def get_guide_details(self, guide_id: str):
        """
        Fetch step-by-step instructions + images for a guide
        """
        url = f"{IFIXIT_BASE}/guides/{guide_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        data = resp.json()
        return self._cleanup_guide_details(data)

    # ------------------ CLEANUP FUNCTIONS ------------------ #
    def _cleanup_search_device(self, data):
        """
        Return only device titles
        """
        results = data.get("results", [])
        devices = [d["title"] for d in results if "title" in d]
        return devices

    def _cleanup_list_guides(self, data):
        """
        Return only guide titles + guide IDs
        """
        guides = []
        for item in data.get("wikis", []):
            if "title" in item and "id" in item:
                guides.append({"title": item["title"], "id": item["id"]})
        return guides

    def _cleanup_guide_details(self, data):
        """
        Return only steps text + image URLs
        """
        cleaned_steps = []
        steps = data.get("steps", [])
        for step in steps:
            cleaned_steps.append({
                "heading": step.get("heading", ""),
                "body": step.get("body", ""),
                "images": [img.get("url") for img in step.get("images", []) if "url" in img]
            })
        return {
            "title": data.get("title", ""),
            "summary": data.get("summary", ""),
            "steps": cleaned_steps
        }
