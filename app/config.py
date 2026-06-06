from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    BIBLE_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    class Config:
        env_file = '.env'

    def validate_api_keys(self):
        """Validate that required API keys are present"""
        missing_keys = []
        
        if not self.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        if not self.BIBLE_API_KEY:
            missing_keys.append("BIBLE_API_KEY")
            
        if missing_keys:
            print(f"Warning: Missing API keys: {', '.join(missing_keys)}")
            print("Please create a .env file with the required API keys.")
            return False
        return True

settings = Settings()

# Validate API keys on startup
if not settings.validate_api_keys():
    print("Some API keys are missing. The application may not work properly.")

