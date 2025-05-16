import os
from dotenv import load_dotenv
load_dotenv('.env', override=True)

scopes = os.getenv("SCOPES")

email_app_auth = os.getenv("EMAIL_APP_AUTH")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv("GEMINI_MODEL")