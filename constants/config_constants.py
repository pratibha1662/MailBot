import os
from dotenv import load_dotenv
load_dotenv('.env', override=True)

scopes = os.getenv("SCOPES")

email_app_auth = os.getenv("EMAIL_APP_AUTH")