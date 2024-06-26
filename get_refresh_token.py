from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import json
import os

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_credentials():
    client_secrets_file = "googleAPI.json"
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
    creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())
    print("Credentials saved to token.json")

    return creds

if __name__ == "__main__":
    creds = get_credentials()
    print("Refresh Token:", creds.refresh_token)
