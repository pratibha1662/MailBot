from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
from constants import config_constants

scopes = config_constants.scopes.split(",")

def get_oauth_creds(creds= None):    
    if creds:
        creds = Credentials.from_authorized_user_info(creds, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            config_constants.email_app_auth, scopes
            )
        
        creds = flow.run_local_server(port=0)
    return creds