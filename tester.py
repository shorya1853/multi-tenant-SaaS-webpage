import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_messages():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    try:
        # Replace 'me' with the actual user ID or 'me' to denote the authenticated user
        user_id = 'me'
        messages = service.users().messages().list(userId=user_id).execute()
        
        if 'messages' in messages:
            for message in messages['messages']:
                msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
                print(f"Message ID: {msg['id']}")
                print(f"Snippet: {msg['snippet']}")
                # Process further as needed

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    get_messages()
