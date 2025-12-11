from langgraph import Agent
from app.tools.ifixit import IFixitTool
from app.tools.web_search import WebSearchTool
from langgraph import SQLiteSaver

class RepairAgent(Agent):
    def __init__(self):
        super().__init__()
        # Optional: Persistent saver using SQLite
        saver = SQLiteSaver(db_path="./repair_fix.db")
        self.set_saver(saver)

        self.ifixit = IFixitTool()
        self.web_search = WebSearchTool()

    def handle_query(self, user_query: str):
        # Step 1: Search device
        devices = self.ifixit.search_device(user_query)
        if not devices:
            # fallback to web search
            return self.web_search.search(user_query)
        
        # Step 2: Get guides for the first device
        guides = self.ifixit.list_guides(devices[0])
        if not guides:
            return self.web_search.search(user_query)
        
        # Step 3: Get details of first guide
        guide_details = self.ifixit.get_guide_details(guides[0]["id"])
        return guide_details
