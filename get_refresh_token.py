from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(
        'googleAPI.json', SCOPES)
    creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print("Refresh Token:", creds.refresh_token)

if __name__ == "__main__":
    get_credentials()
