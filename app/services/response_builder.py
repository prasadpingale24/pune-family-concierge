from app.services.intent_service import Intent, IntentType
from app.data.pune_data import PUNE_DATA
from app.schemas.internal import BotResponse

class ResponseBuilder:
    @staticmethod
    def build(intent: Intent) -> BotResponse:
        reply = ""
        data = {}

        if intent.type == IntentType.RESTAURANT_SEARCH:
            area = intent.area or "fc road"
            restaurants = PUNE_DATA["restaurants"].get(area, [])
            data = {"restaurants": restaurants, "area": area}
            
            if not restaurants:
                reply = f"I couldn't find any specific veg restaurants in {area} right now. You can try FC Road or Baner!"
            else:
                reply = f"🏠 *Veg Restaurants in {area.title()}*:\n\n"
                for i, res in enumerate(restaurants, 1):
                    reply += f"{i}. *{res['name']}*\n   ✨ Specialty: {res['specialty']}\n   ⭐ Rating: {res['rating']}\n\n"

        elif intent.type == IntentType.FAMOUS_FOOD:
            area = intent.area or "fc road"
            foods = PUNE_DATA["famous_food"].get(area, [])
            data = {"famous_foods": foods, "area": area}
            
            if not foods:
                reply = f"I'm not sure what's famous in {area} yet. But you should definitely try the Bun Maska at Goodluck Cafe!"
            else:
                reply = f"😋 *Famous Foods in {area.title()}*:\n\n"
                for food in foods:
                    reply += f"• {food}\n"

        elif intent.type == IntentType.OCCASION_SUGGESTION:
            occ = intent.occasion or "birthday"
            tips = PUNE_DATA["occasions"].get(occ, [])
            data = {"suggestions": tips, "occasion": occ}
            
            reply = f"🎉 *Suggestions for {occ.title()}*:\n\n"
            for tip in tips:
                reply += f"✅ {tip}\n"

        else:
            reply = "Namaste! 🙏 I'm your Pune Family Concierge.\n\nI can help you find *veg restaurants*, *famous food*, or *occasion suggestions* in Pune.\n\nTry asking: 'Veg restaurants in Baner' or 'What is famous in FC Road?'"
            data = {}

        return BotResponse(
            reply=reply.strip(),
            intent=intent.type.value,
            data=data
        )
