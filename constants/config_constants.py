import os
from dotenv import load_dotenv
load_dotenv('.env', override=True)

sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("PASSWORD")
scopes = os.getenv("SCOPES")

token_file_path = os.getenv("OAUTH_TOKEN_FILE_PATH")
email_app_auth = os.getenv("EMAIL_APP_AUTH")