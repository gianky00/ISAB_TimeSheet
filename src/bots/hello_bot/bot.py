from src.bots.base.base_bot import BaseBot
from typing import List, Dict, Any

class HelloBot(BaseBot):
    @property
    def name(self) -> str:
        """Name of the bot."""
        return "Hello Bot"

    @property
    def description(self) -> str:
        """Description of the bot."""
        return "Un semplice bot che saluta."

    def run(self, data: List[Dict[str, Any]]) -> bool:
        """Main execution logic."""
        self.log("CIAO")
        return True
