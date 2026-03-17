from app.services.intent_service import Intent, IntentType
from app.data.pune_data import PUNE_DATA
from app.schemas.internal import BotResponse

class ResponseBuilder:
    @staticmethod
    def build(intent: Intent) -> BotResponse:
        if intent.type == IntentType.RESTAURANT_SEARCH:
            area = intent.area or "fc road" # Default to FC Road if not specified
            restaurants = PUNE_DATA["restaurants"].get(area, [])
            
            if not restaurants:
                return BotResponse(reply=f"I couldn't find any specific veg restaurants in {area} right now. You can try FC Road or Baner!")
                
            reply = f"🏠 *Veg Restaurants in {area.title()}*:\n\n"
            for i, res in enumerate(restaurants, 1):
                reply += f"{i}. *{res['name']}*\n   ✨ Specialty: {res['specialty']}\n   ⭐ Rating: {res['rating']}\n\n"
            return BotResponse(reply=reply.strip())

        elif intent.type == IntentType.FAMOUS_FOOD:
            area = intent.area or "fc road"
            foods = PUNE_DATA["famous_food"].get(area, [])
            
            if not foods:
                return BotResponse(reply=f"I'm not sure what's famous in {area} yet. But you should definitely try the Bun Maska at Goodluck Cafe!")
                
            reply = f"😋 *Famous Foods in {area.title()}*:\n\n"
            for food in foods:
                reply += f"• {food}\n"
            return BotResponse(reply=reply.strip())

        elif intent.type == IntentType.OCCASION_SUGGESTION:
            occ = intent.occasion or "birthday"
            tips = PUNE_DATA["occasions"].get(occ, [])
            
            reply = f"🎉 *Suggestions for {occ.title()}*:\n\n"
            for tip in tips:
                reply += f"✅ {tip}\n"
            return BotResponse(reply=reply.strip())

        else:
            return BotResponse(reply="Namaste! 🙏 I'm your Pune Family Concierge.\n\nI can help you find *veg restaurants*, *famous food*, or *occasion suggestions* in Pune.\n\nTry asking: 'Veg restaurants in Baner' or 'What is famous in FC Road?'")
