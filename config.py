import os
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Config:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")  # Default to gpt-3.5-turbo if not set
        self.temperature = os.getenv("TEMPERATURE", 0.7)  # Default to 0.7 if not set decimal.Decimal(os.getenv("TEMPERATURE", 0))  # Default to 0.7 if not set
        self.token_limit = int(os.getenv("TOKEN_LIMIT", 4096))  # Default to 4096 if not set



