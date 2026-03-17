from enum import Enum
from typing import Optional
from app.schemas.internal import UserMessage

class IntentType(Enum):
    RESTAURANT_SEARCH = "restaurant_search"
    FAMOUS_FOOD = "famous_food"
    OCCASION_SUGGESTION = "occasion_suggestion"
    UNKNOWN = "unknown"

class Intent:
    def __init__(self, type: IntentType, area: Optional[str] = None, occasion: Optional[str] = None):
        self.type = type
        self.area = area
        self.occasion = occasion

class IntentDetector:
    @staticmethod
    def detect(user_message: UserMessage) -> Intent:
        text = user_message.message.lower()
        
        # Simple keyword detection
        areas = ["baner", "fc road", "camp"]
        occasions = ["birthday", "anniversary"]
        
        found_area = next((area for area in areas if area in text), None)
        found_occasion = next((occ for occ in occasions if occ in text), None)
        
        if "famous" in text or "what is" in text:
            return Intent(IntentType.FAMOUS_FOOD, area=found_area)
        
        if found_occasion:
            return Intent(IntentType.OCCASION_SUGGESTION, occasion=found_occasion)
            
        if "restaurant" in text or "food" in text or found_area:
            return Intent(IntentType.RESTAURANT_SEARCH, area=found_area)
            
        return Intent(IntentType.UNKNOWN)
