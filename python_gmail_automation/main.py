from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import base64

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])

    if not messages:
        print('No new messages.')
    else:
        message_count = 0
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = msg['payload']['headers']
            for values in email_data:
                name = values['name']
                if name == 'From':
                    from_name = values['value']
                    if 'parts' in msg['payload']:
                        for part in msg['payload']['parts']:
                            if part['mimeType'] == 'text/plain':
                                data = part['body']["data"]
                                byte_code = base64.urlsafe_b64decode(data)
                                text = byte_code.decode("utf-8")
                                print(f"Message {message_count} from {from_name}: {text}")
                                message_count += 1
                    else:
                        data = msg['payload']['body']["data"]
                        byte_code = base64.urlsafe_b64decode(data)
                        text = byte_code.decode("utf-8")
                        print(f"Message {message_count} from {from_name}: {text}")
                        message_count += 1


if __name__ == '__main__':
    main()
