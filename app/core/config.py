import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Pune Family Concierge Bot"
    API_V1_STR: str = "/webhook"
    
settings = Settings()
